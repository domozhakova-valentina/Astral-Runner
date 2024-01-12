from buttons_functions import *
from menu import Menu
from settings import *

buttons1 = [
    Button("Меню", action=menu_action, width=menu_item_width * 1.3, height=menu_item_height * 1.3,
           color=(255, 255, 255),
           font=font, font_size=font_size, x=120, y=400),
    Button("Следующий уровень", action=new_game_action, width=menu_item_width * 1.3, height=menu_item_height * 1.3,
           color=(255, 255, 255),
           font=font, font_size=font_size, x=750, y=400),
    Button("ВЫ ПОБЕДИЛИ!", action=None, width=game_over_width * 1.25, height=game_over_height * 1.25,
           color=(255, 255, 255),
           font=font, font_size=font_size * 2, x=290, y=100)
]


class Win(Menu):
    def __init__(self, items, coins):
        super().__init__(items=buttons1)
        self.coins = Button(f"Количество монет: {coins} ", action=None, width=menu_item_width, height=menu_item_height,
                            color=(255, 255, 255), font=None, font_size=font_size // 2, x=850, y=680)
        buttons1.append(self.coins)
        self.items = buttons1
        self.size = (screen_width, screen_height)
        self.fon = pygame.image.load('game_over/fon2.jpg')
        self.fon = pygame.transform.scale(self.fon, self.size)
        self.sound = 'sound/win.wav'
