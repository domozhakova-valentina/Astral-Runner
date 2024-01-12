from buttons_functions import *
from menu import Menu
from settings import *

buttons = [
    Button("Начать заново", action=new_game_action, width=menu_item_width, height=menu_item_height,
           color=(255, 255, 255),
           font=font, font_size=font_size, x=150, y=400),
    Button("Меню", action=menu_action, width=menu_item_width, height=menu_item_height, color=(255, 255, 255),
           font=font, font_size=font_size, x=750, y=400),
    Button("GAME OVER", action=None, width=game_over_width, height=game_over_height, color=(255, 255, 255),
           font=font, font_size=font_size * 2, x=350, y=100)
]


class Game_over(Menu):
    def __init__(self, items):
        super().__init__(items=buttons)
        self.items = buttons
        self.size = (screen_width, screen_height)
        self.fon = pygame.image.load('game_over/fon1.jpg')
        self.fon = pygame.transform.scale(self.fon, self.size)
        self.sound = 'sound/game over.mp3'
