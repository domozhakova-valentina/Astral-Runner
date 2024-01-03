from buttons_functions import *
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


class Game_over:
    def __init__(self, buttons):
        self.buttons = buttons
        self.size = (screen_width, screen_height)
        self.fon = pygame.image.load('game_over/fon1.jpg')
        self.fon = pygame.transform.scale(self.fon, self.size)

    def run(self, event, screen):
        # код для рисования на экране
        screen.blit(self.fon, (0, 0))
        for button in self.buttons:
            button.draw(screen)

    def update(self, event):
        # проверка на клик по кнопке. Возвращает либо функцию, соответсвующую кнопке, либо None
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                action = button.update(event.pos)
                if action is not None:
                    return action
        return None
