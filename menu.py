from buttons_functions import *
from settings import *
import pygame

# создаем список пунктов меню
items = [
    Button("Начать игру", action=new_game_action, width=menu_item_width, height=menu_item_height, color=(0, 150, 0),
           font=font, font_size=font_size, x=450, y=300),
    Button("Правила", action=rules_action, width=menu_item_width, height=menu_item_height, color=(0, 150, 0),
           font=font, font_size=font_size, x=450, y=400),
    Button("Настройки", action=options_action, width=menu_item_width, height=menu_item_height, color=(0, 150, 0),
           font=font, font_size=font_size, x=450, y=500)
]


class Menu:
    def __init__(self, items):
        self.items = items
        self.fon = pygame.image.load('menu/fon.jpg')
        self.music = pygame.mixer.Sound("sound/menu_music.mp3")
        self.channel = pygame.mixer.Channel(0)

    def start_music(self):
        self.channel.play(self.music, loops=-1, fade_ms=5000)

    def stop_music(self):
        self.channel.stop()

    def run(self, event, screen):
        # код для рисования меню на экране
        # self.channel.play(self.music, loops=-1, fade_ms=5000)
        screen.blit(self.fon, (0, 0))
        for item in self.items:
            item.draw(screen)

    def update(self, event):
        # проверка на клик по кнопке. Возвращает либо функцию, соответсвующую кнопке, либо None
        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.items:
                action = item.update(event.pos)
                if action is not None:
                    return action
        return None
