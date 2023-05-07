import os.path
from random import choice

import pygame
from pytmx import load_pygame

from src.settings import TILE_SIZE, LAYERS, GROW_SPEED
from src.support import import_folder_dict, import_folder


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']


class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil_water']


class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, check_watered):
        super().__init__(groups)
        self.plant_type = plant_type
        self.frames = import_folder(os.path.join('../graphics/fruits', self.plant_type))
        self.soil = soil
        self.check_watered = check_watered

        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[self.plant_type]
        self.harvestable = False

        self.image = self.frames[self.age]
        self.y_offset = -16 if self.plant_type == 'corn' else -8
        self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['ground_plant']

    def grow(self):
        if self.check_watered(self.rect.center):
            self.age = min(self.age + self.grow_speed, self.max_age)
            if int(self.age) > 0:
                self.z = LAYERS['main']
                self.hitbox = self.rect.copy().inflate(-26, -self.rect.height * 0.4)
            self.harvestable = self.age == self.max_age
            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))


class SoilLayer:
    def __init__(self, all_sprites, collision_sprites):
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        self.soil_surf = pygame.image.load('../graphics/soil/o.png')
        self.soil_surfs = import_folder_dict('../graphics/soil/')
        self.water_surfs = import_folder('../graphics/soil_water')

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
                    if self.raining:
                        self.water_all()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x, y = soil_sprite.rect.x // TILE_SIZE, soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W')
                WaterTile(soil_sprite.rect.topleft, choice(self.water_surfs), [self.all_sprites, self.water_sprites])

    def water_all(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')
                    WaterTile((j * TILE_SIZE, i * TILE_SIZE), choice(self.water_surfs),
                              [self.all_sprites, self.water_sprites])

    def remove_water(self):
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def check_watered(self, pos):
        return 'W' in self.grid[pos[1] // TILE_SIZE][pos[0] // TILE_SIZE]

    def plant_seed(self, target_pos, seed):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x, y = soil_sprite.rect.x // TILE_SIZE, soil_sprite.rect.y // TILE_SIZE
                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    Plant(seed, [self.all_sprites, self.plant_sprites, self.collision_sprites], soil_sprite, self.check_watered)

    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()

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

                    SoilTile((j * TILE_SIZE, i * TILE_SIZE), self.soil_surfs[tile_type],
                             [self.all_sprites, self.soil_sprites])
