import pygame, sys
from settings import *
from data_level import level_0, level_1, level_2, level_3, level_4
from level import Level
from menu import Menu, items
from game_over import GameOver
from win import Win
from options import Options, options_items
from sounds import sounds_list, music_list, background_music, all_sounds
from levels_map import Levels_Map, levels, button_actions

pygame.init()
pygame.mixer.set_num_channels(20)  # устанавливаем больше звуковых каналов
for elem in sounds_list:  # добавление всех звуков
    all_sounds.add_sound(elem)

for elem in music_list:  # добавление всей музыки
    background_music.add_music(elem)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('AstralRunner')
game_state = 'running menu'
scene = menu = Menu(items)
menu.start_music()
game_over = GameOver(items, 0)
win = Win(items, 0)
options = Options(options_items)
levels_map = Levels_Map(levels, button_actions)
level = Level(level_0, screen)
clock = pygame.time.Clock()
while True:
    if level.end_flag:
        scene.stop_music()
        all_sounds.play_sound(game_over.sound)
        scene = GameOver(items, level.counter_coins)
        level.end_flag = False
    if level.win_flag:
        scene.stop_music()
        all_sounds.play_sound(win.sound)
        scene = Win(items, level.counter_coins)
        level.win_flag = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        change = scene.update(event)
        if change is not None:
            game_state = change()
            scene.stop_music()
            if game_state == 'running_menu':
                scene = menu
            if game_state == 'running_level_1':
                level = Level(level_0, screen)
                scene = level
            if game_state == 'running_level_2':
                level = Level(level_1, screen)
                scene = level
            if game_state == 'running_level_3':
                level = Level(level_2, screen)
                scene = level
            if game_state == 'running_level_4':
                level = Level(level_3, screen)
                scene = level
            if game_state == 'running_level_5':
                level = Level(level_4, screen)
                scene = level
            if game_state == 'running_options':
                scene = options
            if game_state == 'running_rules':
                pass
            if game_state == 'running_levels_map':
                scene = levels_map
            scene.start_music()
    scene.run(event, screen)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
