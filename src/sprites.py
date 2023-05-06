from random import random, choice

import pygame

from src.settings import LAYERS, APPLE_POS


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
        self.z = z


class Water(Generic):
    def __init__(self, pos, frames, groups):
        self.frames = frames
        self.frame_index = 0

        super().__init__(pos, self.frames[self.frame_index], groups, LAYERS['water'])

    def animate(self, dt):
        self.frame_index += 5 * dt
        self.frame_index %= len(self.frames)
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)


class WildFlower(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups, LAYERS['main'])
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)


class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration=200):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()


class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add):
        super().__init__(pos, surf, groups)

        self.health = 3 if name == 'Small' else 5
        self.alive = True
        self.stump_surf = pygame.image.load(f'../graphics/stumps/{name.lower()}.png').convert_alpha()

        self.apple_surf = pygame.image.load('../graphics/fruits/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

    def damage(self):
        self.health -= 1
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(random_apple.rect.topleft, random_apple.image, self.groups()[0], LAYERS['fruit'], 200)
            self.player_add('apple')
            random_apple.kill()

    def check_death(self):
        if self.health <= 0:
            Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS['fruit'], 300)
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.player_add('wood')

    def create_fruit(self):
        for x, y in self.apple_pos:
            if random() < 0.2:
                Generic((x + self.rect.left, y + self.rect.top), self.apple_surf,
                        [self.apple_sprites, self.groups()[0]], LAYERS['fruit'])

    def update(self, dt):
        if self.alive:
            self.check_death()
