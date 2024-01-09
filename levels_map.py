from buttons_functions import *
from settings import *
from sounds import background_music
import pygame
import pickle
from load import import_folder_images

# создаем список пунктов меню
levels = [
    Button("Меню", action=menu_action, width=100, height=50, color=(0, 150, 0),
           font=None, font_size=30, x=10, y=10),
    Button("Level 1", action=start_level_1, width=menu_item_width, height=menu_item_height, color=(0, 150, 0),
           font=font, font_size=font_size, x=500, y=300, image='menu/levels_photo/lava_planet.png'),
    Button("Level 2", action=None, width=menu_item_width, height=menu_item_height, color=(150, 150, 150),
           font=font, font_size=font_size, x=850, y=300, image='menu/levels_photo/mars_planet.png'),
    Button("Level 3", action=None, width=menu_item_width, height=menu_item_height, color=(150, 150, 150),
           font=font, font_size=font_size, x=150, y=600, image='menu/levels_photo/ice planet_1.png'),
    Button("Level 4", action=None, width=menu_item_width, height=menu_item_height, color=(150, 150, 150),
           font=font, font_size=font_size, x=500, y=600, image='menu/levels_photo/swamp_planet.png'),
    Button("Level 5", action=None, width=menu_item_width, height=menu_item_height, color=(150, 150, 150),
           font=font, font_size=font_size, x=850, y=600, image='menu/levels_photo/planet_5.png')
]

button_actions = [start_level_2, start_level_3, start_level_4, start_level_5]


class Levels_Map:
    def __init__(self, items, button_actions):
        self.items = items
        self.fon = pygame.image.load('menu/fon.jpg')
        self.music = "sound/menu_music.mp3"
        self.button_actions = button_actions

    def start_music(self):
        background_music.play_music(self.music)

    def stop_music(self):
        background_music.stop_music(self.music)

    def run(self, event, screen):
        # код для рисования на экране
        screen.blit(self.fon, (0, 0))

        with open("levels_data/coins_data.pickle", "rb") as file:
            coins_data = pickle.load(file)
            coins = [coins_data["level_0"], coins_data["level_1"], coins_data["level_2"], coins_data["level_3"],
                     coins_data["level_4"]]

        text = ['Ваши монеты',
                f'Level 1: {coins_data["level_0"]}',
                f'Level 2: {coins_data["level_1"]}',
                f'Level 3: {coins_data["level_2"]}',
                f'Level 4: {coins_data["level_3"]}',
                f'Level 5: {coins_data["level_4"]}']

        text_coord = 150
        font = pygame.font.Font(None, 30)
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            text_rect = string_rendered.get_rect()
            text_coord += 10
            text_rect.top = text_coord
            text_rect.x = 150
            text_coord += text_rect.height
            screen.blit(string_rendered, text_rect)

        for i in range(len(self.items)):
            if i >= 2 and int(coins[i - 2]) >= 23:
                self.items[i].change_color((0, 150, 0))
                self.items[i].change_action(self.button_actions[i - 2])
            self.items[i].draw(screen)

    def update(self, event):
        # проверка на клик по кнопке. Возвращает либо функцию, соответсвующую кнопке, либо None
        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.items:
                action = item.update(event.pos)
                if action is not None:
                    return action
        return None
