import pygame
from maps_odject import AnimatedDecor


class Explosion(AnimatedDecor):
    def __init__(self, size, x, y, path, k_animate=0.2):
        super().__init__(size, x, y, path, k_animate)

    def animation(self):
        super().animation()
        if self.index_cadre == 0:  # для того чтобы анимация прекратилась когда пройдёт цикл взрыва
            self.kill()



