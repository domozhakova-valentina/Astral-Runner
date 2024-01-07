from maps_odject import AnimatedDecor
from sounds import all_sounds


class Explosion(AnimatedDecor):
    def __init__(self, size, x, y, path, k_animate=0.2):
        super().__init__(size, x, y, path, k_animate)
        # звук взрыва
        self.explosion_sound = "sound/explosion.mp3"
        self.start_sound = True # чтобы звук был проигран только один раз

    def animation(self):
        self.play_sound()
        super().animation()
        if self.index_cadre == 0:  # для того чтобы анимация прекратилась когда пройдёт цикл взрыва
            self.start_sound = True
            self.kill()

    def play_sound(self):
        if self.start_sound:
            all_sounds.play_sound(self.explosion_sound)
            self.start_sound = False
