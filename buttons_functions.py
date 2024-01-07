import pygame
from sounds import all_sounds, background_music


class Button:
    def __init__(self, text, action, width, height, color, font, font_size, x, y):
        self.text = text
        self.action = action
        self.font = font
        self.font_size = font_size
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y

    def draw(self, screen):
        # код для рисования кнопки на экране
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        if self.text != '':
            font = pygame.font.SysFont(self.font, self.font_size)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

    def update(self, coords):
        # выполнение функции, соответсвующей кнопке, если кнопка была нажата
        if self.x < coords[0] < self.x + self.width and self.y < coords[1] < self.y + self.height:
            return self.action
        return None

    def change_color(self, color):
        self.color = color


'''Ниже функции кнопок'''


def new_game_action():
    return 'running_levels_map'


def rules_action():
    return 'running_rules'


def options_action():
    return 'running_options'


def menu_action():
    return 'running_menu'


def active_sound(num):
    all_sounds.change_sounds_volume(num)


def active_music(num):
    num = 1 - num
    background_music.change_music_volume(num)


def change_music_loud(num):
    background_music.change_music_volume(num)


def start_level_1():
    return 'running_level_1'


def start_level_2():
    return 'running_level_2'


def start_level_3():
    return 'running_level_3'


def start_level_4():
    return 'running_level_4'


def start_level_5():
    return 'running_level_5'
