import pygame

from src.settings import LAYERS


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


class Tree(Generic):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)
