import pygame
from pytmx import load_pygame

from src.settings import TILE_SIZE, LAYERS
from src.support import import_folder_dict


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']


class SoilLayer:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        self.soil_surf = pygame.image.load('../graphics/soil/o.png')
        self.soil_surfs = import_folder_dict('../graphics/soil/')

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        ground = pygame.image.load('../graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame('../data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if 'F' in cell:
                    x, y = i * TILE_SIZE, j * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x, y = rect.x // TILE_SIZE, rect.y // TILE_SIZE
                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if 'X' in cell:
                    t = 'X' in self.grid[i - 1][j]
                    r = 'X' in row[j + 1]
                    b = 'X' in self.grid[i + 1][j]
                    l = 'X' in row[j - 1]

                    tile_type = 'o'

                    if t and r and b and l:
                        tile_type = 'x'

                    if t and not (r and b and l):
                        tile_type = 'b'
                    if r and not (b and l and t):
                        tile_type = 'l'
                    if b and not (l and t and r):
                        tile_type = 't'
                    if l and not (t and r and b):
                        tile_type = 'r'

                    if r and l and not (t and b):
                        tile_type = 'lr'
                    if t and b and not (l and r):
                        tile_type = 'tb'

                    if t and r and not (b and l):
                        tile_type = 'bl'
                    if r and b and not (l and t):
                        tile_type = 'tl'
                    if b and l and not (t and r):
                        tile_type = 'tr'
                    if l and t and not (r and b):
                        tile_type = 'br'

                    if t and r and b and not l:
                        tile_type = 'tbr'
                    if r and b and l and not t:
                        tile_type = 'lrt'
                    if b and l and t and not r:
                        tile_type = 'tbl'
                    if l and t and r and not b:
                        tile_type = 'lrb'

                    SoilTile((j * TILE_SIZE, i * TILE_SIZE), self.soil_surfs[tile_type], [self.all_sprites, self.soil_sprites])
