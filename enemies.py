import pygame
from maps_odject import AnimatedDecor
from scales import HealthBar
from random import randint


class MainEnemy(AnimatedDecor):
    def __init__(self, size, x, y, path, health=20):
        super().__init__(size, x, y, path + '/run')
        self.speed = -randint(3, 6)
        self.health = health
        x, y = x + size // 2, y + size
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.health_scale = HealthBar((0, 0), 2, 6, health,
                                      '', flag_frame_text=False,
                                      color_scale=(250, 0, 0))  # создание шкалы здоровья

    def turn(self):
        '''Меняется направление движения.'''
        self.speed *= -1

    def moving(self):
        self.rect.x += self.speed

    def turn_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def coordinate_scale(self):
        return self.rect.topleft - pygame.math.Vector2(0, 10)

    def update(self, shift):
        super().update(shift)
        self.moving()
        self.turn_image()
        self.health_scale.new_x, self.health_scale.y = self.coordinate_scale()  # переопределение координат шкалы здоровья
