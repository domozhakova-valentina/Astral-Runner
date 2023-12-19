import pygame, sys
from settings import *
from level import Level
from data_level import level_0

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('AstralRunner')
level = Level(level_0, screen)  # создание уровня
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('grey')
    level.run()  # обновление картинки уровня
    pygame.display.update()
    clock.tick(60)
