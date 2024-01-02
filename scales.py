import pygame


class RechargeScale:
    COLOR_OUTLINE = (0, 0, 0)
    COLOR_SCALE = (200, 200, 10)
    SIZE_FONT = 25

    def __init__(self, position, text_color):
        self.x, self.y = position
        self.max_value = 140
        self.value = self.max_value
        self.color_text = text_color

    def update(self):
        if self.value < self.max_value:
            self.value += 0.5

    def permission_shoot(self):
        '''Разрешение на стрельбу'''
        if self.value > self.max_value // 3:
            self.value -= self.max_value // 3
            return True
        return False

    def draw(self, screen):
        word = 'Заряжен:' if self.value >= self.max_value - 1 else 'Перезарядка:'
        # Шрифт
        font = pygame.font.SysFont(None, RechargeScale.SIZE_FONT)
        # Создание текста
        text = font.render(word, True, self.color_text)
        # Отображение текста в центре окна
        text_rect = text.get_rect(topleft=(self.x, self.y))
        screen.blit(text, text_rect)
        new_x = self.x + 10 * RechargeScale.SIZE_FONT // 2  # сдвиг по x
        # рисование самой прямоугольной шкалы
        pygame.draw.rect(screen, RechargeScale.COLOR_SCALE, (new_x, self.y, self.value, 20))
        # Нарисовать контур прямоугольника
        pygame.draw.rect(screen, RechargeScale.COLOR_OUTLINE, (new_x, self.y, self.max_value + 2, 20), 2)
        # рисование отделяющих линий
        pygame.draw.line(screen, RechargeScale.COLOR_OUTLINE, (new_x + self.max_value // 3, self.y),
                         (new_x + self.max_value // 3, self.y + 18), 2)
        pygame.draw.line(screen, RechargeScale.COLOR_OUTLINE, (new_x + self.max_value // 3 * 2, self.y),
                         (new_x + self.max_value // 3 * 2, self.y + 18), 2)

