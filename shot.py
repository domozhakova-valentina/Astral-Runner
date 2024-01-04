import pygame
from load import import_folder_images
from sounds import all_sounds


class Missile(pygame.sprite.Sprite):
    def __init__(self, path, obj, speed, max_c):
        super().__init__()
        self.cadres = import_folder_images(path)
        self.index = 0  # индекс изображения в кадрах
        self.image = self.cadres[0]
        self.object = obj  # тот кто стреляет
        self.speed = speed  # скорость полёта пули
        self.rect = self.image.get_rect(center=self.get_position())
        self.max_counter = max_c
        self.counter = 0

        # звук выстрела
        self.shot_sound = "sound/shot.wav"

    def get_position(self):
        '''Координаты с учётом всех смещений.'''
        if self.object.face_right:
            self.x = self.object.rect.x + self.object.image.get_size()[1] - 25
            self.speed = abs(self.speed)
        else:
            self.x = self.object.rect.x
            self.speed *= -1 if self.speed > 0 else 1
        y = self.object.rect.y + self.object.image.get_size()[1] // 2 - 15
        return self.x, y

    def setting_position(self, shift):
        if self.index > len(self.cadres) - 1:
            # снаряд летит
            self.image = self.cadres[-1]
            self.rect.x += self.speed + shift[0]
            self.rect.y += shift[1]
        else:
            # это анимация вспышки из ствола оружия
            self.index += 0.2
            self.image = self.cadres[int(self.index)]
            self.rect.center = self.get_position()

    def update(self, shift):
        # звук стрельбы
        if self.counter == 0:
            all_sounds.play_sound(self.shot_sound)

        # нужно, чтобы ограничить дальность стрельбы
        if self.counter < self.max_counter:
            self.counter += 1
        else:
            self.kill()
        self.setting_position(shift)
