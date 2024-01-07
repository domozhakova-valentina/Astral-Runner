import pygame
from settings import screen_width, screen_height


class RisingSubstance(pygame.sprite.Sprite):
    def __init__(self, color, speed):
        super().__init__()

        # Загрузка изображения вещества
        self.image = pygame.Surface([screen_width, screen_height])
        self.image.fill(color)

        # Получение ограничивающего прямоугольника
        self.rect = self.image.get_rect(topleft=(0, screen_height * 2))

        # Задаем скорость подъема
        self.speed = speed
        self.int_speed = 0

    def update(self, shift_y):
        if self.int_speed > 1:
            self.int_speed = 0
        self.int_speed += self.speed
        # Обновляем позицию вещества (поднимаем вверх)
        self.rect = self.image.get_rect(topleft=self.rect.topleft - pygame.math.Vector2(0, int(self.int_speed) - shift_y))
