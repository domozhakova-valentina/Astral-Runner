import pygame
from load import import_folder_images


class MainTile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))  # установка тайла в левом верхнем углу

    def update(self, x_shift):
        self.rect.x += x_shift


class StaticTile(MainTile):
    def __init__(self, size, x, y, image_surface):
        super().__init__(size, x, y)
        self.image = image_surface


class AnimatedDecor(MainTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.cadres = import_folder_images(path)
        self.index_cadre = 0
        self.image = self.cadres[self.index_cadre]

    def animation(self):
        self.index_cadre += 0.2  # увеличение индекса кадра для перелистования на новый
        if self.index_cadre > len(self.cadres):  # возвращение к началу кадров
            self.index_cadre = 0
        self.image = self.cadres[int(self.index_cadre)]

    def update(self, x_shift):
        self.animation()
        super().update(x_shift)


class Coin(AnimatedDecor):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        x, y = x + size // 2, y + size // 2
        self.rect = self.image.get_rect(center=(x, y))
