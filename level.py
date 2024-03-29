from random import randrange
import pickle

import pygame
from settings import screen_width, screen_height
from load import import_csv_map, import_folder_images, import_folder_folder
from maps_odject import StaticTile, CuttingObject, Coin, MainTile, MobileTile
from player import Player
from dust_particle import Particle
from enemies import MainEnemy
from scales import RechargeScale, HealthBar
from explosions import Explosion
from sounds import all_sounds, background_music
from asteroids import Asteroid
from rising_matter import RisingSubstance


class Level:
    PATH_EXP = 'graphics/explosions/1'

    def __init__(self, data_level, screen):
        # Шрифт
        font = pygame.font.SysFont(None, 40)
        # Создание текста
        self.text = font.render('Убейте всех монстров и доберитесь до блока end!!!', True,
                                data_level['color_text_scale'])
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
        self.PATH_ASTEROID = data_level['PATH_ASTEROID']
        self.PATH_EXR_ASTEROID = data_level['PATH_EXR_ASTEROID']
        self.damage_asteroid = data_level['damage_asteroid']
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

        # создание движущих плиток, если они есть
        if 'limitations_tiles' in data_level.keys() and 'mobile_tiles' in data_level.keys():
            limitations_map = import_csv_map(data_level['limitations_tiles'])
            self.limitations_tiles = self.create_tiles_group(limitations_map, 'limitations tiles', data_level)
            tiles_map = import_csv_map(data_level['mobile_tiles'])
            self.mobile_tiles = self.create_tiles_group(tiles_map, 'mobile tiles', data_level)
        else:
            self.limitations_tiles = pygame.sprite.Group()
            self.mobile_tiles = pygame.sprite.Group()

        # создание поднимающегося вещества, если оно предусмотрено
        self.substance = pygame.sprite.GroupSingle()
        if 'color_rising_substance' in data_level.keys():
            sprite = RisingSubstance(data_level['color_rising_substance'], speed=0.3)
            self.substance.add(sprite)

        # музыка
        self.music = "sound/game_music.mp3"

        # звук приземления
        self.land_sound = 'sound/jump.ogg'

        # звук повреждения игрока
        self.damage_sound = 'sound/damage.mp3'

        # флаги проигрыша и выигрыша
        self.end_flag = False
        self.win_flag = False

        # имя уровня для хранения информации о монетах
        self.level_name = data_level['level_name']

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
                        folder = data['obstacles_folder']
                        if folder.split('/')[-1] == 'thorns':
                            speed_animate = 0.05
                        else:
                            speed_animate = 0.3
                        sprite = CuttingObject(self.tile_size, x, y, folder, speed_animate)
                    elif type == 'limitations enemy' or type == 'limitations tiles':
                        sprite = MainTile(self.tile_size, x, y)
                    elif type == 'enemy':
                        folder = import_folder_folder('graphics/enemies')
                        path = folder[int(col)]  # берём по индификатуру из списка путей папок путь папки монстра
                        if col in ('0', '3', '4'):
                            sprite = MainEnemy(self.tile_size, x, y, path)
                        elif col in ('1', '2'):
                            sprite = MainEnemy(self.tile_size, x, y, path, health=30, direction=1)
                        elif col == '5':
                            sprite = MainEnemy(self.tile_size, x, y, path, health=50, direction=1, speed=7)
                    elif type == 'mobile tiles':
                        surfaces = import_folder_images(data['terrain_folder'])
                        image = surfaces[int(col)]  # берём по индификатуру из списка изображение
                        sprite = MobileTile(self.tile_size, x, y, image)
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
            all_sounds.play_sound(self.land_sound)  # звук падения

    def horizontal_collisions(self):
        '''Горизонтальные столкновения с картой.'''
        sprite = self.player.sprite
        group_sprites = self.terrain_sprites.sprites() + self.fg_decorations.sprites() + self.mobile_tiles.sprites()
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
        group_sprites = self.terrain_sprites.sprites() + self.fg_decorations.sprites() + self.mobile_tiles.sprites()
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
        if mid_x < screen_width / 2 and dir_x < 0:
            self.world_shift.x = sprite.CONST_SPEED
            sprite.speed = 0
        elif mid_x > screen_width - (screen_width / 2) and dir_x > 0:
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

    def tile_reverse(self):
        '''Определяет столкновение с ограничениями и разворачивает плитку.'''
        for tile in self.mobile_tiles.sprites():
            sprite_collision = pygame.sprite.spritecollide(tile, self.limitations_tiles, False)
            if sprite_collision:
                tile.turn()

    def collision_missile_player(self):
        '''Столкновения снаряда с монстрами и препятствиями.'''
        enemy = self.enemies.sprites()
        limitations = self.terrain_sprites.sprites() + self.fg_decorations.sprites() +\
                      self.obstacles.sprites() + self.mobile_tiles.sprites()
        group_limitations = pygame.sprite.Group()
        group_limitations.add(limitations)
        missiles = self.player.sprite.missiles

        collisions = pygame.sprite.groupcollide(missiles, group_limitations, False,
                                                False)  # столкновение групп спрайтов снарядов и объектов карты

        for missile, limitations in collisions.items():
            for limitation in limitations:
                if pygame.sprite.collide_mask(missile,
                                              limitation):  # для того чтобы проверять, что спрайты столкнулись изображениями
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
        sprites = self.enemies.sprites() + self.obstacles.sprites() + self.asteroids.sprites()  # спрайты от которых игрок, может, получит урон
        for sprite in sprites:
            if pygame.sprite.collide_mask(player, sprite):
                all_sounds.play_sound(self.damage_sound)
                if sprite in self.asteroids.sprites():  # от астероидов
                    damage = self.damage_asteroid
                    x, y = sprite.rect.topleft
                    sprite.kill()
                    explosion_sprite = Explosion(128, x, y, self.PATH_EXR_ASTEROID, k_animate=0.5)
                    self.explosions.add(explosion_sprite)
                elif sprite in self.enemies.sprites():
                    damage = 2
                else:
                    damage = 1
                if self.healh_scale.change_health(damage):  # изменяется шкала здоровья
                    # если здоровье закончилось, то игрок умирает
                    self.end_flag = True

        if self.substance.sprite:
            # столкновение с веществом
            if pygame.sprite.collide_mask(player, self.substance.sprite):
                player.gravity += 0.02
                if self.healh_scale.change_health(1):  # изменяется шкала здоровья
                    # если здоровье закончилось, то игрок умирает
                    player.kill()
                    self.end_flag = True
            else:
                player.gravity = player.CONST_GRAVITY
            # если весь экран в веществе
            if self.substance.sprite.rect.y <= 0:
                player.kill()
                self.end_flag = True

    def collision_with_coins(self):
        sprite = self.player.sprite
        size_font = 32
        for coin in self.coins:
            if pygame.sprite.collide_mask(coin, sprite):
                all_sounds.play_sound(self.coin_sound)  # звук сбора монет
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
            with open("levels_data/coins_data.pickle", "rb") as file:
                coins_data = pickle.load(file)
            if int(self.counter_coins) > int(coins_data[self.level_name]):
                coins_data[self.level_name] = self.counter_coins
            with open(f"levels_data/coins_data.pickle", "wb") as file:
                pickle.dump(coins_data, file)
            self.win_flag = True

    def generation_asteroids(self):
        '''Генерируются рандомно астероиды в соответствие с коэффициентом.'''
        for n in range(self.k_generation_asteroid):
            r = randrange(10001)
            if r == 10:
                asteroid = Asteroid(128, self.PATH_ASTEROID, k_animate=0.1)
                self.asteroids.add(asteroid)
        self.asteroids.update(self.world_shift)
        self.asteroids.draw(self.display)

    def collision_with_asteroids(self):
        limitations_sprites = self.terrain_sprites.sprites() + self.fg_decorations.sprites() +\
                              self.obstacles.sprites() + self.mobile_tiles.sprites()
        group_limitations = pygame.sprite.Group()
        group_limitations.add(limitations_sprites)
        collisions = pygame.sprite.groupcollide(self.asteroids, group_limitations, False,
                                                False)  # столкновение групп спрайтов астероидов и объектов карты

        for asteroid, limitations in collisions.items():
            for limitation in limitations:
                if pygame.sprite.collide_mask(asteroid,
                                              limitation):  # для того чтобы проверять, что спрайты столкнулись изображениями
                    x, y = asteroid.rect.topleft
                    explosion_sprite = Explosion(128, x, y, self.PATH_EXR_ASTEROID, k_animate=0.5)
                    self.explosions.add(explosion_sprite)
                    asteroid.kill()

    def check_fall(self):
        if self.player.sprite.falling_check():
            self.end_flag = True

    def initial_text(self):
        '''Текст приветствие.'''
        if self.counter_coins == 0:
            # Отображение текста
            text_rect = self.text.get_rect(center=(screen_width // 2, screen_height // 7))
            self.display.blit(self.text, text_rect)

    def run(self, screen, event):
        '''Запуск уровня!'''
        # рисование фона
        self.display.blit(self.background_image, (0, 0))

        # обработка столкновения снаряда player's
        self.collision_missile_player()

        # обновление всего
        self.terrain_sprites.update(self.world_shift)
        self.fg_decorations.update(self.world_shift)
        self.limitations_tiles.update(self.world_shift)
        self.limitations_enemy.update(self.world_shift)
        self.mobile_tiles.update(self.world_shift)
        self.enemies.update(self.world_shift)
        self.tile_reverse()
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
        self.substance.update(self.world_shift[1])

        # рисование пуль
        self.player.sprite.missiles.draw(self.display)

        # местность
        self.terrain_sprites.draw(self.display)
        self.fg_decorations.draw(self.display)
        self.mobile_tiles.draw(self.display)

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

        self.collision_with_asteroids()  # столкновения объектов карты с астероидами
        # генерация астероидов и отображение их
        self.generation_asteroids()

        # отображение поднимающегося вещества
        self.substance.draw(self.display)

        # обработка столкновения с монетами
        self.collision_with_coins()

        # рисование шкалы относящихся к нему текст
        self.missile_scale.draw(self.display)
        self.healh_scale.draw(self.display)

        # проверка(прошёл игрок уровень)
        self.win_player()

        # отображение текста
        self.initial_text()

        # проверка на падение в бездну
        self.check_fall()

        # обработка урона
        self.player_kill()

    def update(self, event):
        pass

    def start_music(self):
        background_music.play_music(self.music)

    def stop_music(self):
        background_music.stop_music(self.music)
