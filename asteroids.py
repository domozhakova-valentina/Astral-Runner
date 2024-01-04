import pygame
from random import randint
from maps_odject import AnimatedDecor
from settings import screen_width, screen_height


class Asteroid(AnimatedDecor):
    def __init__(self, size, path, k_animate=0.2):
        self.size = size
        x = randint(20, screen_width - 20)
        super().__init__(size, x, -size, path, k_animate)
        self.speed_x_y = randint(-2 , 2), randint(4, 10)  # генерация скорости астероида

    def update(self, shift):
        # изменение координат
        self.rect.x += self.speed_x_y[0]
        self.rect.y += self.speed_x_y[1]
        super().update(shift)
        if self.rect.y - self.speed_x_y[1] - self.size > screen_height:
            self.kill()
