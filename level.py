import sys
from random import randrange

import pygame
from settings import screen_width, screen_height
from load import import_csv_map, import_folder_images, import_folder_folder
from maps_odject import StaticTile, CuttingObject, Coin, MainTile
from player import Player
from dust_particle import Particle
from enemies import MainEnemy
from scales import RechargeScale, HealthBar
from explosions import Explosion
from sounds import all_sounds, background_music
from asteroids import Asteroid


class Level:
    PATH_EXP = 'graphics/explosions/1'
    PATH_ASTEROID = 'graphics/animate_asteroid/'
    PATH_EXR_ASTEROID = 'graphics/explosions/2'

    def __init__(self, data_level, screen):
        # общая настройка
        self.display = screen
        self.world_shift = pygame.math.Vector2(0,
                                               0)  # сдвиг мира он нужен для того чтобы прокручевать карту(все объекты её)
        self.tile_size = data_level['tile size']
        self.load_scales(data_level['color_text_scale'])  # инициализируются и создаются различные шкалы игрока
        self.background_image = pygame.image.load(data_level['background'])
        self.damage_player = data_level['damage player']
        self.counter_coins = 0
        self.coin_image = pygame.image.load('graphics/coins/0.png')
        self.k_generation_asteroid = data_level['asteroid_generation_coefficient']
        self.asteroids = pygame.sprite.Group()

        # спрайты взрывов
        self.explosions = pygame.sprite.Group()

        # игрока
        player_map = import_csv_map(data_level['player'])
        self.player = pygame.sprite.GroupSingle()
        self.purpose = pygame.sprite.GroupSingle()
        self.start = pygame.sprite.GroupSingle()
        self.x = None
        self.load_player(player_map, data_level['gravity_player'])

        # настройка рельефа местности(плиток)
        terrain_map = import_csv_map(data_level['terrain'])
        self.terrain_sprites = self.create_tiles_group(terrain_map, 'terrain', data_level)

        # различные декорации которые выступают как препятствия
        decorations_map = import_csv_map(data_level['decorations'])
        self.fg_decorations = self.create_tiles_group(decorations_map, 'decorations', data_level)

        # монеты
        coins_map = import_csv_map(data_level['coins'])
        self.coins = self.create_tiles_group(coins_map, 'coins', data_level)

        # звук сбора монет
        self.coin_sound = "sound/get_coin.wav"
        all_sounds.add_sound(self.coin_sound)

        # режущие препятствия
        cutting_object_map = import_csv_map(data_level['obstacles'])
        self.obstacles = self.create_tiles_group(cutting_object_map, 'obstacles', data_level)

        # пыль от ног игрока
        self.particles_dust_sprite = pygame.sprite.GroupSingle()

        # невидимые ограничения для врагов
        limitations_enemy_map = import_csv_map(data_level['limitations_enemy'])
        self.limitations_enemy = self.create_tiles_group(limitations_enemy_map, 'limitations enemy', data_level)

        # враги
        enemies_map = import_csv_map(data_level['enemies'])
        self.enemies = self.create_tiles_group(enemies_map, 'enemy', data_level)

        # музыка
        self.music = "sound/game_music.mp3"

        # звук приземления
        self.land_sound = 'sound/jump.ogg'

        # звук повреждения игрока
        self.damage_sound = 'sound/damage.mp3'

    def create_tiles_group(self, map, type, data):
        '''Создаёт группы спрайтов карты в соответствии с типом объекта.'''
        all_group = pygame.sprite.Group()
        sprite = None
        for row_ind, row in enumerate(map):
            for col_ind, col in enumerate(row):
                if col != '-1':
                    x = col_ind * self.tile_size
                    y = row_ind * self.tile_size
                    if type in ('terrain', 'decorations'):
                        surfaces = import_folder_images(data['terrain_folder'])
                        image = surfaces[int(col)]  # берём по индификатуру из списка изображение
                        if type == 'decorations':
                            sprite = StaticTile(self.tile_size, x, y, image, croped=(10, 50))
                        else:
                            sprite = StaticTile(self.tile_size, x, y, image)
                    elif type == 'coins':
                        sprite = Coin(self.tile_size, x, y, 'graphics/coins')
                    elif type == 'obstacles':
                        sprite = CuttingObject(self.tile_size, x, y, data['obstacles_folder'], 0.3)
                    elif type == 'limitations enemy':
                        sprite = MainTile(self.tile_size, x, y)
                    elif type == 'enemy':
                        folder = import_folder_folder('graphics/enemies')
                        path = folder[int(col)]  # берём по индификатуру из списка путей папок путь папки монстра
                        sprite = MainEnemy(self.tile_size, x, y, path)
                    if sprite is not None:
                        all_group.add(sprite)
        return all_group

    def load_player(self, map, gravity):
        '''Загрузка игрока, места возрождения, цели до которой он должен добраться.'''
        for row_ind, row in enumerate(map):
            for col_ind, col in enumerate(row):
                if col != '-1':
                    x = col_ind * self.tile_size
                    y = row_ind * self.tile_size
                    if col == '0':
                        sprite = Player((x, y), self.display, 'graphics/character_animate/', self.jump_dust,
                                        permission_shoot=self.missile_scale.permission_shoot, speed=7, gravity=gravity)
                        self.player.add(sprite)
                        image = pygame.image.load('graphics/character/start.png').convert_alpha()
                        sprite = StaticTile(self.tile_size, x, y, image)
                        self.start.add(sprite)
                    elif col == '1':
                        image = pygame.image.load('graphics/character/end.png').convert_alpha()
                        sprite = StaticTile(self.tile_size, x, y, image)
                        self.purpose.add(sprite)

    def load_scales(self, color_text):
        self.missile_scale = RechargeScale((10, 10), color_text)
        self.healh_scale = HealthBar((10, 40), 1.8, 20, Player.HEALTH, color_text)

    def jump_dust(self, x_y):
        '''Записывает частицы прыжка в текущие частицы вертикального движения.'''
        if self.player.sprite.face_right:
            x_y += pygame.math.Vector2(7, -10)
        else:
            x_y += pygame.math.Vector2(-7, -10)
        dust_sprite = Particle(x_y, 'jump')
        self.particles_dust_sprite.add(dust_sprite)

    def before_player_on_ground(self):
        '''Нужен для распознания был ли игрок на земле до применения вертикальной коллизии.'''
        self.flag_ground = True if self.player.sprite.ground else False

    def land_dust(self):
        '''Эффект частиц пыли при падение игрока на поверхность.'''
        if self.player.sprite.ground and not self.flag_ground and not self.particles_dust_sprite.sprites():
            dust_sprite = Particle(self.player.sprite.rect.midbottom - pygame.math.Vector2(0, 15), 'land')
            self.particles_dust_sprite.add(dust_sprite)
            all_sounds.play_sound(self.land_sound) # звук падения

    def horizontal_collisions(self):
        '''Горизонтальные столкновения с картой.'''
        sprite = self.player.sprite
        group_sprites = self.terrain_sprites.sprites() + self.fg_decorations.sprites()
        sprite.rect.x += sprite.direction.x * sprite.speed
        for gs in group_sprites:
            if gs.rect.colliderect(sprite.rect):
                if sprite.direction.x < 0:
                    sprite.rect.left = gs.rect.right
                    sprite.left = True
                    self.x = sprite.rect.left
                if sprite.direction.x > 0:
                    sprite.rect.right = gs.rect.left
                    sprite.right = True
                    self.x = sprite.rect.right
            if sprite.left and (sprite.rect.left < self.x or sprite.direction.x >= 0):
                sprite.left = False
            if sprite.right and (sprite.rect.right > self.x or sprite.direction.x <= 0):
                sprite.right = False

    def vertical_collisions(self):
        '''Вертикальные столкновения с картой.'''
        sprite = self.player.sprite
        group_sprites = self.terrain_sprites.sprites() + self.fg_decorations.sprites()
        sprite.gravitation()
        for gs in group_sprites:
            if gs.rect.colliderect(sprite.rect):
                if sprite.direction.y < 0:
                    sprite.rect.top = gs.rect.bottom + 8  # +8 убирает баг с перекрытием из-за анимации
                    sprite.direction.y = 0
                    sprite.ceiling = True
                if sprite.direction.y > 0:
                    sprite.rect.bottom = gs.rect.top
                    sprite.direction.y = 0
                    sprite.ground = True
        if sprite.ground and sprite.direction.y != 0:
            sprite.ground = False
        if sprite.ceiling and sprite.direction.y > 0:
            sprite.ceiling = False

    def moving_map(self):
        '''Прокручивание экрана.'''
        sprite = self.player.sprite
        mid_x, dir_x, mid_y, dir_y = sprite.rect.centerx, sprite.direction.x, sprite.rect.centery, sprite.direction.y
        if mid_x < screen_width / 3 and dir_x < 0:
            self.world_shift.x = sprite.CONST_SPEED
            sprite.speed = 0
        elif mid_x > screen_width - (screen_width / 3) and dir_x > 0:
            self.world_shift.x = -sprite.CONST_SPEED
            sprite.speed = 0
        else:
            self.world_shift.x = 0
            sprite.speed = sprite.CONST_SPEED
        if mid_y > screen_height - (screen_height / 4) and dir_y < 0:
            self.world_shift.y = -4
        elif mid_y < screen_height / 4 and dir_y > 0:
            self.world_shift.y = 2
        elif (screen_height / 2 - screen_height / 10) < mid_y < (screen_height / 2 + screen_height / 10):
            self.world_shift.y = 0
        elif (screen_height / 2 - screen_height / 10) > mid_y:
            self.world_shift.y = 3
        else:
            self.world_shift.y = -6

    def enemy_reverse(self):
        '''Определяет столкновение с ограничениями и разворачивает врага.'''
        for enemy in self.enemies.sprites():
            sprite_collision = pygame.sprite.spritecollide(enemy, self.limitations_enemy, False)
            if sprite_collision:
                enemy.turn()

    def collision_missile_player(self):
        '''Столкновения снаряда с монстрами и препятствиями.'''
        enemy = self.enemies.sprites()
        limitations = self.terrain_sprites.sprites() + self.fg_decorations.sprites() + self.obstacles.sprites()
        missiles = self.player.sprite.missiles

        for sprite in limitations:  # переборка объектов карты
            for missile in missiles:
                if pygame.sprite.collide_mask(missile, sprite):
                    self.generate_explosion(missile)
                    missile.kill()
        for sprite in enemy:  # переборка врагов
            if 0 < sprite.rect.topleft[0] < screen_width and 0 < sprite.rect.topleft[1] < screen_height:
                sprite.health_scale.draw(self.display)  # рисование шкалы здоровья врага
            for missile in missiles:
                if pygame.sprite.collide_mask(missile, sprite):
                    self.generate_explosion(missile)
                    if sprite.health_scale.change_health(self.damage_player):  # снимаются жизни у врага
                        sprite.kill()
                    missile.kill()

    def generate_explosion(self, missile):
        if missile.speed < 0:
            x, y = missile.rect.topleft - pygame.math.Vector2(22, 0)  # координаты левого верхнего угла снаряда + сдвиг
        else:
            x, y = missile.rect.topright - pygame.math.Vector2(22,
                                                               0)  # координаты правого верхнего угла снаряда + сдвиг
        self.explosion_sprite = Explosion(64, x, y, Level.PATH_EXP, k_animate=0.3)
        self.explosions.add(self.explosion_sprite)

    def player_kill(self):
        player = self.player.sprite
        sprites = self.enemies.sprites() + self.obstacles.sprites()  # спрайты от которых игрок, может, получит урон
        for sprite in sprites:
            if pygame.sprite.collide_mask(player, sprite):
                all_sounds.play_sound(self.damage_sound)
                if self.healh_scale.change_health(2 if sprite in self.enemies.sprites()
                                                  else 1):  # изменяется шкала здоровья
                    # если здоровье закончилось, то игрок умирает
                    player.kill()
                    sys.exit()

    def collision_with_coins(self):
        sprite = self.player.sprite
        size_font = 32
        for coin in self.coins:
            if pygame.sprite.collide_mask(coin, sprite):
                all_sounds.play_sound(self.coin_sound) # звук сбора монет
                coin.kill()
                self.counter_coins += 1
        self.display.blit(self.coin_image, (screen_width - self.coin_image.get_width(), 0))
        # Шрифт
        font = pygame.font.SysFont(None, size_font)
        # Создание текста
        text = font.render(str(self.counter_coins), True, (0, 0, 250))
        # Отображение текста
        text_rect = text.get_rect(topleft=(screen_width -
                                           len(str(self.counter_coins)) *
                                           size_font // 2 - self.coin_image.get_width(), 6))
        self.display.blit(text, text_rect)

    def win_player(self):
        '''Проверяет выиграл ли прошёл ли игрок уровень.'''
        player = self.player.sprite
        end = self.purpose.sprite
        if pygame.sprite.collide_mask(player, end) and not self.enemies.sprites():
            print('Win')
            sys.exit()

    def generation_asteroids(self):
        '''Генерируются рандомно астероиды в соответствие с коэффициентом.'''
        for n in range(self.k_generation_asteroid):
            r = randrange(10001)
            if r == 10:
                asteroid = Asteroid(128, Level.PATH_ASTEROID, k_animate=0.1)
                self.asteroids.add(asteroid)
        self.asteroids.update(self.world_shift)
        self.asteroids.draw(self.display)

    def collision_with_asteroids(self):
        limitations_sprites = self.terrain_sprites.sprites() + self.fg_decorations.sprites() + self.obstacles.sprites()
        player_sprite = self.player.sprite
        asteroids = self.asteroids.sprites()

        for sprite in asteroids:
            if pygame.sprite.collide_mask(player_sprite, sprite):
                # игрок умирает
                player_sprite.kill()
                sys.exit()

        for sprite in limitations_sprites:
            for asteroid in asteroids:
                if pygame.sprite.collide_mask(asteroid, sprite):
                    x, y = asteroid.rect.center
                    asteroid.kill()
                    self.explosion_sprite = Explosion(128, x, y, Level.PATH_EXR_ASTEROID, k_animate=0.5)
                    self.explosions.add(self.explosion_sprite)

    def run(self, screen, event):
        '''Запуск уровня!'''
        # рисование фона
        self.display.blit(self.background_image, (0, 0))

        # обработка урона
        self.player_kill()

        # обработка столкновения снаряда player's
        self.collision_missile_player()

        # обновление всего
        self.terrain_sprites.update(self.world_shift)
        self.fg_decorations.update(self.world_shift)
        self.limitations_enemy.update(self.world_shift)
        self.enemies.update(self.world_shift)
        self.enemy_reverse()
        self.coins.update(self.world_shift)
        self.start.update(self.world_shift)
        self.purpose.update(self.world_shift)
        self.particles_dust_sprite.update(self.world_shift)
        self.obstacles.update(self.world_shift)
        self.player.update()
        self.explosions.update(self.world_shift)
        self.player.sprite.missiles.update(self.world_shift)
        self.missile_scale.update()

        # рисование пуль
        self.player.sprite.missiles.draw(self.display)

        # местность
        self.terrain_sprites.draw(self.display)
        self.fg_decorations.draw(self.display)

        # про врагов
        self.enemies.draw(self.display)

        # отображение монет
        self.coins.draw(self.display)

        # рисование игрока
        self.before_player_on_ground()
        self.vertical_collisions()
        self.land_dust()
        self.horizontal_collisions()
        self.moving_map()
        self.player.draw(self.display)

        # рисование возрождения и цели - конца
        self.start.draw(self.display)
        self.purpose.draw(self.display)

        # отображение пыли
        self.particles_dust_sprite.draw(self.display)

        # рисование режущих препятствий
        self.obstacles.draw(self.display)

        # рисование взрыва
        self.explosions.draw(self.display)

        # обработка столкновения с монетами
        self.collision_with_coins()

        self.collision_with_asteroids()  # столкновения всего с астероидами
        # генерация астероидов и отображение их
        self.generation_asteroids()

        # рисование шкалы относящихся к нему текст
        self.missile_scale.draw(self.display)
        self.healh_scale.draw(self.display)

        # проверка(прошёл игрок уровень)
        self.win_player()

    def update(self, event):
        pass

    def start_music(self):
        background_music.play_music(self.music)

    def stop_music(self):
        background_music.stop_music(self.music)
