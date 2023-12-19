import pygame
from settings import tile_size
from load import import_csv_map, import_folder_images
from maps_odject import StaticTile, AnimatedDecor, Coin


class Level:
    def __init__(self, data_level, screen):
        # общая настройка
        self.display = screen
        self.world_shift = -3  # сдвиг мира он нужен для того чтобы прокручевать карту(все объекты её)

        # игрока
        player_map = import_csv_map(data_level['player'])
        self.designations_players = self.create_tiles_group(player_map, 'player')

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
                        sprite = StaticTile(tile_size, x, y, image)
                    elif type == 'coins':
                        sprite = Coin(tile_size, x, y, 'graphics/coins')
                    elif type == 'player':
                        image = pygame.image.load(['graphics/character/start.png',
                                                   'graphics/character/end.png'][int(col)]).convert_alpha()
                        sprite = StaticTile(tile_size, x, y, image)
                    all_group.add(sprite)
        return all_group

    def run(self):
        '''Запуск уровня!'''
        # местность
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display)
        self.fg_decorations.update(self.world_shift)
        self.fg_decorations.draw(self.display)

        # отображение монет
        self.coins.update(self.world_shift)
        self.coins.draw(self.display)

        # рисование возрождения и цели - конца
        self.designations_players.update(self.world_shift)
        self.designations_players.draw(self.display)
