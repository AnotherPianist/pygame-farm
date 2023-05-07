import pygame
from pytmx import load_pygame

from src.settings import TILE_SIZE, LAYERS


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
                    SoilTile((j * TILE_SIZE, i * TILE_SIZE), self.soil_surf, [self.all_sprites, self.soil_sprites])
