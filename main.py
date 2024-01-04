import pygame, sys
from settings import *
from data_level import level_0
from level import Level
from menu import Menu, items
from game_over import Game_over, buttons
from options import Options, options_items

pygame.init()
pygame.mixer.set_num_channels(100)  # устанавливаем больше звуковых каналов
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('AstralRunner')
game_state = 'running menu'
scene = menu = Menu(items)
menu.start_music()
game_over = Game_over(buttons)
options = Options(options_items)
level = Level(level_0, screen)  # создание уровня
clock = pygame.time.Clock()

while True:
    screen.fill('grey')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        change = scene.update(event)
        if change is not None:
            game_state = change()
            scene.stop_music()
            if game_state == 'running_game':
                scene = level
            if game_state == 'running_menu':
                scene = menu
            if game_state == 'running_options':
                scene = options
            if game_state == 'running_rules':
                pass
            if game_state == 'game_over':
                scene = game_over
            scene.start_music()
    scene.run(event, screen)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)
