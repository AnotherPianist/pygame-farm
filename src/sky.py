from random import randint, choice

import pygame

from src.settings import LAYERS, SCREEN_HEIGHT, SCREEN_WIDTH
from src.sprites import Generic
from src.support import import_folder


class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)

    def display(self, dt):
        for i, value in enumerate(self.end_color):
            self.start_color[i] = max(self.end_color[i], self.start_color[i] - 2 * dt)
        self.full_surf.fill(self.start_color)
        self.display_surface.blit(self.full_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class Drop(Generic):
    def __init__(self, pos, surf, groups, z, moving):
        super().__init__(pos, surf, groups, z)

        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt):
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('../graphics/rain/drops')
        self.rain_floor = import_folder('../graphics/rain/floor')
        self.floor_w, self.floor_h = pygame.image.load('../graphics/world/ground.png').get_size()

    def create_floor(self):
        Drop((randint(0, self.floor_w), randint(0, self.floor_h)), choice(self.rain_floor), self.all_sprites,
             LAYERS['rain_floor'], False)

    def create_drops(self):
        Drop((randint(0, self.floor_w), randint(0, self.floor_h)), choice(self.rain_drops), self.all_sprites,
             LAYERS['rain_drops'], True)

    def update(self):
        self.create_floor()
        self.create_drops()
