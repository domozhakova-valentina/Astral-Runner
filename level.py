import pygame
from settings import tile_size, screen_width, screen_height
from load import import_csv_map, import_folder_images
from maps_odject import StaticTile, AnimatedDecor, Coin
from player import Player


class Level:
    def __init__(self, data_level, screen):
        # общая настройка
        self.display = screen
        self.world_shift = pygame.math.Vector2(0, 0)  # сдвиг мира он нужен для того чтобы прокручевать карту(все объекты её)

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
                            sprite = StaticTile(tile_size, x, y, image, croped=(0, 50))
                        else:
                            sprite = StaticTile(tile_size, x, y, image)
                    elif type == 'coins':
                        sprite = Coin(tile_size, x, y, 'graphics/coins')
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
                        sprite = Player((x, y), self.display, 'graphics/character_animate/', speed=7)
                        self.player.add(sprite)
                        image = pygame.image.load('graphics/character/start.png').convert_alpha()
                        sprite = StaticTile(tile_size, x, y, image)
                        self.start.add(sprite)
                    elif col == '1':
                        image = pygame.image.load('graphics/character/end.png').convert_alpha()
                        sprite = StaticTile(tile_size, x, y, image)
                        self.purpose.add(sprite)

    def horizontal_collisions(self):
        '''Горизонтальные столкновения с картой.'''
        sprite = self.player.sprite
        group_sprites = self.terrain_sprites.sprites() + self.fg_decorations.sprites()
        sprite.rect.x += sprite.direction.x * sprite.speed
        for gs in group_sprites:
            if pygame.sprite.collide_mask(sprite, gs):
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
                    sprite.rect.top = gs.rect.bottom
                    sprite.direction.y = 0
                    sprite.ceiling = True
                elif sprite.direction.y > 0:
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

    def run(self, screen, event):
        '''Запуск уровня!'''
        # местность
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display)
        self.fg_decorations.update(self.world_shift)
        self.fg_decorations.draw(self.display)

        # отображение монет
        self.coins.update(self.world_shift)
        self.coins.draw(self.display)

        # рисование игрока
        self.player.update()
        self.vertical_collisions()
        self.horizontal_collisions()
        self.moving_map()
        self.player.draw(self.display)

        # рисование возрождения и цели - конца
        self.start.update(self.world_shift)
        self.start.draw(self.display)

        self.purpose.update(self.world_shift)
        self.purpose.draw(self.display)

    def update(self, event):
        pass
