import pygame, sys
from settings import *
from data_level import level_0, level_1, level_2, level_3
from level import Level
from menu import Menu, items
from game_over import Game_over, buttons
from options import Options, options_items
from sounds import sounds_list, music_list, background_music, all_sounds
from levels_map import Levels_Map, levels

pygame.init()
pygame.mixer.set_num_channels(20)  # устанавливаем больше звуковых каналов
for elem in sounds_list:  # добавление всех звуков
    all_sounds.add_sound(elem)

for elem in music_list:  # добавление всей музыки
    background_music.add_music(elem)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('AstralRunner')
scene = menu = Menu(items)
menu.start_music()
# game_over = Game_over(buttons)
# options = Options(options_items)
# level_0 = Level(coins_data.pickle, screen)
# level_1 = Level(data_level_1.pickle, screen)
# level_2 = Level(data_level_2.pickle, screen)
# level_3 = Level(data_level_3.pickle, screen)
# levels_map = Levels_Map(levels)
clock = pygame.time.Clock()

game_states = {
    'running_levels_map': Levels_Map(levels),
    'running_rules': Menu(items),
    'running_options': Options(options_items),
    'running_menu': Menu(items),
    'running_level_1': Level(level_0, screen),
    'running_level_2': Level(level_1, screen),
    'running_level_3': Level(level_2, screen),
    'running_level_4': Level(level_3, screen),
    'running_level_5': Level(level_0, screen),
    'game_over': Game_over(buttons)
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        change = scene.update(event)
        if change is not None:
            scene.stop_music()
            scene = game_states[change()]
            scene.start_music()
    scene.run(event, screen)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
