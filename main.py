import pygame, sys
from settings import *
from data_level import level_0
from level import Level
from menu import Menu, items

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('AstralRunner')
game_state = 'running menu'
scene = menu = Menu(items)
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
    if game_state == 'running_game':
        scene = level
    if game_state == 'running_menu':
        scene = menu
    if game_state == 'running_options':
        pass
    if game_state == 'running_rules':
        pass
    scene.run(event, screen)
    pygame.display.update()
    clock.tick(60)
