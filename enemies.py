import pygame
from maps_odject import AnimatedDecor
from random import randint


class MainEnemy(AnimatedDecor):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path + '/run')
        self.speed = -randint(3, 6)
        x, y = x + size // 2, y + size
        self.rect = self.image.get_rect(midbottom=(x, y))

    def turn(self):
        '''Меняется направление движения.'''
        self.speed *= -1

    def moving(self):
        self.rect.x += self.speed

    def turn_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, shift):
        super().update(shift)
        self.moving()
        self.turn_image()
