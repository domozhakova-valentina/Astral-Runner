import pygame
from buttons_functions import *


class Slider:
    '''Отвечает за громкость'''

    def __init__(self, x, y, w, h, action, text):
        self.circle_x = x + w // 2
        self.slider_rect = pygame.Rect(x, y, w, h)
        self.volume = int((x + w // 2 - self.slider_rect.x) / float(self.slider_rect.w) * 100)
        self.value_x = x + w + 20
        self.value_y = y + h // 2
        self.text = text
        self.text_x = x
        self.text_y = y - 50
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.slider_rect)
        pygame.draw.circle(screen, (255, 240, 255), (self.circle_x, (self.slider_rect.h / 2 + self.slider_rect.y)),
                           self.slider_rect.h * 1.5)

        # записываем значение на слайдере справа
        font = pygame.font.SysFont(None, 30)
        value = font.render(str(self.volume), 1, (0, 0, 0))
        screen.blit(value, (self.value_x, self.value_y))

        # записываем название слайдера сверху
        text = font.render(self.text, 1, (0, 0, 0))
        screen.blit(text, (self.text_x, self.text_y))

    def update_volume(self, x):
        if x < self.slider_rect.x:
            self.volume = 0
        elif x > self.slider_rect.x + self.slider_rect.w:
            self.volume = 100
        else:
            self.volume = int((x - self.slider_rect.x) / float(self.slider_rect.w) * 100)

    def on_slider_hold(self, x, y):
        if ((x - self.circle_x) * (x - self.circle_x) + (y - (self.slider_rect.y + self.slider_rect.h / 2)) * (
                y - (self.slider_rect.y + self.slider_rect.h / 2))) \
                <= (self.slider_rect.h * 1.5) * (self.slider_rect.h * 1.5):
            return True
        else:
            return False

    def handle_event(self, x):
        if x < self.slider_rect.x:
            self.circle_x = self.slider_rect.x
        elif x > self.slider_rect.x + self.slider_rect.w:
            self.circle_x = self.slider_rect.x + self.slider_rect.w
        else:
            self.circle_x = x
        self.update_volume(x)

    def update(self, coords):
        if self.on_slider_hold(coords[0], coords[1]):
            x, y = pygame.mouse.get_pos()
            self.handle_event(x)
            self.action(self.volume / 100)
        return None


class Toggle:
    '''Выполняет действие и меняет иконки при нажатии'''

    def __init__(self, text, action, image_names, x, y):
        self.action = action
        self.text = text
        self.images = []
        for elem in image_names:
            im = pygame.image.load(f'menu/{elem}')
            self.images.append(im)
        self.image = self.images[0]
        self.image_count = 0
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def draw(self, screen):
        # код для рисования кнопки на экране
        font = pygame.font.SysFont(None, 30)
        text = font.render(self.text, 1, (0, 0, 0))
        screen.blit(text, (self.x + self.rect.width + 20, self.y + self.rect.height // 2))
        screen.blit(self.image, (self.x, self.y))

    def update(self, coords):
        # выполнение функции, соответсвующей кнопке, если кнопка была нажата
        if self.x < coords[0] < self.x + self.rect.width and self.y < coords[1] < self.y + self.rect.height:
            if self.image_count < len(self.images) - 1:
                self.image = self.images[self.image_count + 1]
                self.image_count += 1
            else:
                self.image = self.images[0]
                self.image_count = 0
            self.action()
        return None


options_items = [Slider(300, 600, 500, 20, change_music_loud, 'Громкость'),
                 Toggle(text='Музыка', action=active_music, image_names=['music_is.jpg', 'music_not.jpg'], x=300,
                        y=200),
                 Toggle(text='Фоновые звуки', action=active_sound, image_names=['sound_is.jpg', 'sound_not.jpg'], x=300,
                        y=400),
                 Button("Меню", action=menu_action, width=100, height=50, color=(0, 150, 0),
                        font=None, font_size=30, x=10, y=10)]


class Options:
    def __init__(self, items):
        self.items = items
        self.music = "sound/menu_music.mp3"

    def run(self, event, screen):
        # код для рисования меню на экране
        screen.fill('grey')
        for item in self.items:
            item.draw(screen)

    def update(self, event):
        # проверка на клик по кнопке. Возвращает либо функцию, соответсвующую кнопке, либо None
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            action = options_items[0].update(event.pos)
            if action is not None:
                return action
        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.items:
                action = item.update(event.pos)
                if action is not None:
                    return action
        return None

    def start_music(self):
        background_music.play_music(self.music)

    def stop_music(self):
        background_music.stop_music(self.music)
