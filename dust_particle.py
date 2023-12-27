import pygame
from load import import_folder_images


class Particle(pygame.sprite.Sprite):
    JUMP_PATH = 'graphics/character_animate/particles_character/jump'
    LAND_PATH = 'graphics/character_animate/particles_character/land'

    def __init__(self, pos, type_movement):
        super().__init__()
        self.index_cadre = 0
        self.an_speed = 0.5
        if type_movement == 'land':
            self.cadres = import_folder_images(Particle.LAND_PATH)
        elif type_movement == 'jump':
            self.cadres = import_folder_images(Particle.JUMP_PATH)
        self.image = self.cadres[self.index_cadre]
        self.rect = self.image.get_rect(center=pos)

    def animation(self):
        self.index_cadre += self.an_speed
        if self.index_cadre >= len(self.cadres):
            self.kill()  # после прокручевания всех кадров эффект частиц пропадает
        else:
            self.image = self.cadres[int(self.index_cadre)]

    def update(self, shift):
        self.animation()
        self.rect.topleft += shift
