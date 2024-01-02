import pygame
from settings import tile_size, screen_width, screen_height
from load import import_csv_map, import_folder_images, import_folder_folder
from maps_odject import StaticTile, CuttingObject, Coin, MainTile
from player import Player
from dust_particle import Particle
from enemies import MainEnemy
from scales import RechargeScale
from explosions import Explosion


class Level:
    PATH_EXP = 'graphics/explosions/1'

    def __init__(self, data_level, screen):
        # общая настройка
        self.display = screen
        self.world_shift = pygame.math.Vector2(0, 0)  # сдвиг мира он нужен для того чтобы прокручевать карту(все объекты её)
        self.load_scales(data_level['color_text_scale'])  # инициализируются и создаются различные шкалы
        self.background_image = pygame.image.load(data_level['background'])

        # спрайты взрывов
        self.explosions = pygame.sprite.Group()

        # игрока
        player_map = import_csv_map(data_level['player'])
        self.player = pygame.sprite.GroupSingle()
        self.purpose = pygame.sprite.GroupSingle()
        self.start = pygame.sprite.GroupSingle()
        self.x = None
        self.load_player(player_map)

        # настройка рельефа местности(плиток)
        terrain_map = import_csv_map(data_level['terrain'])
        self.terrain_sprites = self.create_tiles_group(terrain_map, 'terrain')

        # различные декорации которые выступают как препятствия
        decorations_map = import_csv_map(data_level['decorations'])
        self.fg_decorations = self.create_tiles_group(decorations_map, 'decorations')

        # монеты
        coins_map = import_csv_map(data_level['coins'])
        self.coins = self.create_tiles_group(coins_map, 'coins')

        # режущие препятствия
        cutting_object_map = import_csv_map(data_level['obstacles'])
        self.obstacles = self.create_tiles_group(cutting_object_map, 'obstacles')

        # пыль от ног игрока
        self.particles_dust_sprite = pygame.sprite.GroupSingle()

        # невидимые ограничения для врагов
        limitations_enemy_map = import_csv_map(data_level['limitations_enemy'])
        self.limitations_enemy = self.create_tiles_group(limitations_enemy_map, 'limitations enemy')

        # враги
        enemies_map = import_csv_map(data_level['enemies'])
        self.enemies = self.create_tiles_group(enemies_map, 'enemy')

    def create_tiles_group(self, map, type):
        '''Создаёт группы спрайтов карты в соответствии с типом объекта.'''
        all_group = pygame.sprite.Group()
        for row_ind, row in enumerate(map):
            for col_ind, col in enumerate(row):
                if col != '-1':
                    x = col_ind * tile_size
                    y = row_ind * tile_size
                    if type in ('terrain', 'decorations'):
                        surfaces = import_folder_images('graphics/tirrein')
                        image = surfaces[int(col)]  # берём по индификатуру из списка изображение
                        if type == 'decorations':
                            sprite = StaticTile(tile_size, x, y, image, croped=(10, 50))
                        else:
                            sprite = StaticTile(tile_size, x, y, image)
                    elif type == 'coins':
                        sprite = Coin(tile_size, x, y, 'graphics/coins')
                    elif type == 'obstacles':
                        sprite = CuttingObject(tile_size, x, y, 'graphics/obstacles/cutting_disc', 0.3)
                    elif type == 'limitations enemy':
                        sprite = MainTile(tile_size, x, y)
                    elif type == 'enemy':
                        folder = import_folder_folder('graphics/enemies')
                        path = folder[int(col)]  # берём по индификатуру из списка путей папок путь папки монстра
                        sprite = MainEnemy(tile_size, x, y, path)
                    all_group.add(sprite)
        return all_group

    def load_player(self, map):
        '''Загрузка игрока, места возрождения, цели до которой он должен добраться.'''
        for row_ind, row in enumerate(map):
            for col_ind, col in enumerate(row):
                if col != '-1':
                    x = col_ind * tile_size
                    y = row_ind * tile_size
                    if col == '0':
                        sprite = Player((x, y), self.display, 'graphics/character_animate/', self.jump_dust,
                                        permission_shoot=self.missile_scale.permission_shoot, speed=7)
                        self.player.add(sprite)
                        image = pygame.image.load('graphics/character/start.png').convert_alpha()
                        sprite = StaticTile(tile_size, x, y, image)
                        self.start.add(sprite)
                    elif col == '1':
                        image = pygame.image.load('graphics/character/end.png').convert_alpha()
                        sprite = StaticTile(tile_size, x, y, image)
                        self.purpose.add(sprite)

    def load_scales(self, color_text):
        self.missile_scale = RechargeScale((10, 10), color_text)

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
            if pygame.sprite.spritecollide(enemy, self.limitations_enemy, False):
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
            for missile in missiles:
                if pygame.sprite.collide_mask(missile, sprite):
                    self.generate_explosion(missile)
                    sprite.kill()
                    missile.kill()

    def generate_explosion(self, missile):
        if missile.speed < 0:
            x, y = missile.rect.topleft - pygame.math.Vector2(22, 0)  # координаты левого верхнего угла снаряда + сдвиг
        else:
            x, y = missile.rect.topright - pygame.math.Vector2(22, 0) # координаты правого верхнего угла снаряда + сдвиг
        self.explosion_sprite = Explosion(64, x, y, Level.PATH_EXP, k_animate=0.3)
        self.explosions.add(self.explosion_sprite)

    def run(self, screen, event):
        '''Запуск уровня!'''
        # рисование фона
        self.display.blit(self.background_image, (0, 0))

        # обработка столкновения снаряда player's
        self.collision_missile_player()

        # обновление всего
        self.terrain_sprites.update(self.world_shift)
        self.fg_decorations.update(self.world_shift)
        self.limitations_enemy.update(self.world_shift)
        self.enemy_reverse()
        self.enemies.update(self.world_shift)
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

        # рисование шкалы перезарядки и относящейся к нему текст
        self.missile_scale.draw(self.display)

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

    def update(self, event):
        pass
