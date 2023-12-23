import pygame


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


'''Ниже функции кнопок'''


def new_game_action():
    return 'running_game'


def rules_action():
    return 'running_rules'


def options_action():
    return 'running_options'
