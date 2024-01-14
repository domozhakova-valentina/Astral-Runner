from buttons_functions import *
from menu import Menu
from settings import *

use = ['Цель: последовательно пройти все уровни.',
       'Для прохождения уровня нужно дойти до финиша, сохранив очки жизней,',
       'собрав необходимое количество монет и убив всех монстров.']

coins_info = ['Необходимое количество монет:', '  Для перехода на второй уровень - 16/16', '  Для перехода на третий - 25/30',
              '  Для перехода на четвёртый - 30/35', '  Для перехода на пятый - 20/20']

controls = ['Управление:', "  Влево и вправо - по стрелочкам", "  Прыжок - пробел", '  Стрельба - клавиша "С"']

items = [
    Button("Правила игры", action=None, width=menu_item_width, height=menu_item_height,
           color=(166, 202, 240), font=font, font_size=font_size, x=450, y=50),
    Button("Меню", action=menu_action, width=menu_item_width * 0.5, height=menu_item_height,
           color=(0, 150, 0), font=font, font_size=font_size, x=50, y=50)
]

items1 = [Button(use, action=None, width=1000, height=menu_item_height * 3.1,
                 color=(166, 202, 240), font=font, font_size=35, x=70, y=200),
          Button(coins_info, action=None, width=550, height=menu_item_height * 4.3,
                 color=(166, 202, 240), font=font, font_size=35, x=70, y=415),
          Button(controls, action=None, width=450, height=menu_item_height * 4.3,
                 color=(166, 202, 240), font=font, font_size=35, x=650, y=415)
          ]


class Rules(Menu):
    def __init__(self):
        super().__init__(items=items)
        self.items1 = items1

    def run(self, event, screen):
        # код для рисования на экране
        screen.blit(self.fon, (0, 0))
        for item in self.items:
            item.draw(screen)
        for item in self.items1:
            item.draw1(screen)
