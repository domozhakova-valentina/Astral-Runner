import pygame
from load import import_folder_images
from random import randint


class MainTile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))  # установка тайла в левом верхнем углу

    def update(self, shift):
        self.rect.topleft += shift


class StaticTile(MainTile):
    def __init__(self, size, x, y, image_surface, croped=(0, 0)):
        super().__init__(size, x, y)
        if croped != (0, 0):
            # обрезается изображение
            self.image = image_surface.subsurface((croped[0], croped[1],
                                                   size - 2 * croped[0], size - croped[1]))
        else:
            self.image = image_surface
        self.rect = self.image.get_rect(topleft=(x + croped[0] // 2, y + croped[1]))


class MobileTile(StaticTile):
    def __init__(self, size, x, y, image_surface):
        super().__init__(size, x, y, image_surface)
        self.speed = -randint(3, 5)

    def turn(self):
        '''Меняется направление движения.'''
        self.speed *= -1

    def moving(self):
        self.rect.x += self.speed

    def update(self, shift):
        super().update(shift)
        self.moving()


class AnimatedDecor(MainTile):
    def __init__(self, size, x, y, path, k_animate=0.2):
        super().__init__(size, x, y)
        self.cadres = import_folder_images(path)
        self.index_cadre = 0
        self.image = self.cadres[self.index_cadre]
        self.k_animate = k_animate

    def animation(self):
        self.index_cadre += self.k_animate  # увеличение индекса кадра для перелистования на новый
        if self.index_cadre >= len(self.cadres):  # возвращение к началу кадров
            self.index_cadre = 0
        self.image = self.cadres[int(self.index_cadre)]

    def update(self, shift):
        self.animation()
        super().update(shift)


class CuttingObject(AnimatedDecor):
    def __init__(self, size, x, y, path, k_animate=0.2):
        super().__init__(size, x, y, path, k_animate)
        x, y = x + size // 2, y + size  # переопределение координат установки изображения
        self.rect = self.image.get_rect(midbottom=(x, y))

    def animation(self):
        super().animation()
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)


class Coin(AnimatedDecor):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        x, y = x + size // 2, y + size // 2  # переопределение координат установки изображения
        self.rect = self.image.get_rect(center=(x, y))
