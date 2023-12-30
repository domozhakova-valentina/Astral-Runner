import pygame
from load import import_folder_images


class Player(pygame.sprite.Sprite):
    PATH_RUN_DUST = 'graphics/character_animate/particles_character/run/'

    def __init__(self, position, screen, character_path, dust_jump, speed=5):
        super().__init__()
        self.import_character_animations(character_path)

        # про анимацию
        self.index_cadre = 0
        self.an_speed = 0.1  # коэффициент перемотки кадров
        self.image = self.animations['idle'][self.index_cadre]
        self.action = 'idle'

        # физические величины
        self.direction = pygame.math.Vector2(0, 0)
        self.CONST_SPEED = speed
        self.speed = speed
        self.gravity = 0.6
        self.jump_coef = -16
        self.rect = self.image.get_rect(topleft=position)  # установка на позицию
        self.face_right = True
        self.ground = False  # стоит на земле
        self.ceiling = False  # касается потолка
        self.left, self.right = False, False  # касается чего-то справа или слева соответственно

        # про пыль
        self.import_particles_run()
        self.dust_index_cadre = 0
        self.dust_an_speed = 0.15
        self.surface = screen
        self.dust_jump = dust_jump

    def import_particles_run(self):
        self.dustes_run = import_folder_images(Player.PATH_RUN_DUST)

    def animate_run_dust(self):
        '''Анимация частиц пыли из-под ног при беги.'''
        if self.action == 'run' and self.ground:
            self.dust_index_cadre += self.dust_an_speed
            if self.dust_index_cadre > len(self.dustes_run):
                self.dust_index_cadre = 0
            cadre = self.dustes_run[int(self.dust_index_cadre)]
            if self.face_right:
                position = self.rect.bottomleft - pygame.math.Vector2(4, 10)  # смещения пыли прям под ноги
            else:
                position = self.rect.bottomright + pygame.math.Vector2(4, -10)
                cadre = pygame.transform.flip(cadre, True, False)
            self.surface.blit(cadre, position)

    def import_character_animations(self, path):
        self.animations = {'run': None, 'jump': None, 'idle': None}  # словарь с изображениями каждого вида анимации
        for animate in self.animations.keys():
            self.animations[animate] = import_folder_images(path + animate)

    def animation(self):
        '''Выборка нужного кадра героя.'''
        cadres = self.animations[self.action]
        self.index_cadre += self.an_speed
        if self.index_cadre > len(cadres):
            self.index_cadre = 0
        cadre = cadres[int(self.index_cadre)]
        self.image = cadre if self.face_right else pygame.transform.flip(cadre, True, False)
        if self.action == 'idle' and int(self.index_cadre) == 1:  # для удержания игрока стоящим при приседании
            self.rect = self.rect.move(0, 3)
        if self.ground and self.right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.ground and self.left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.ceiling and self.right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.ceiling and self.left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def tracking_action(self):
        if self.direction.y < 0:
            self.action = 'jump'
        elif self.direction.x == 0:
            self.action = 'idle'
        elif self.direction.x != 0:
            self.action = 'run'

    def user_input(self):
        '''Изменение вектора передвижения игрока в соответствии с нажатыми клавишами'''
        input_keys = pygame.key.get_pressed()
        if input_keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.face_right = True
        elif input_keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.face_right = False
        else:
            self.direction.x = 0
        if input_keys[pygame.K_SPACE] and self.ground:
            self.direction.y = self.jump_coef
            self.dust_jump(self.rect.midbottom)

    def gravitation(self):
        '''Изменение положения игрока под действием силы тяжести'''
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.user_input()
        self.animation()
        self.tracking_action()
        self.animate_run_dust()
