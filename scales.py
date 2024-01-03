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
        # Отображение текста
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


class HealthBar:
    SIZE_FONT = 25
    COLOR_OUTLINE = (255, 255, 255)

    def __init__(self, position, k_width, height, max_health, text_color, flag_frame_text=True,
                 color_scale=(0, 255, 0)):
        self.color_scale = color_scale
        self.x, self.y = position
        self.k_width = k_width
        self.width = self.k_width * max_health
        self.height = height
        self.max_health = max_health
        self.health = max_health
        self.color_text = text_color
        self.flag_frame_text = flag_frame_text
        if self.flag_frame_text:  # нужно для того чтобы у жизней монстров не было рамки
            self.word = 'Здоровье:'
            self.new_x = self.x + len(self.word) * HealthBar.SIZE_FONT // 2  # сдвиг по x
            self.outline_points = [(self.new_x, self.y), (self.new_x + self.width, self.y),
                                   (self.new_x + self.width - self.height, self.y + self.height),
                                   (self.new_x - 20, self.y + self.height)]
        else:
            self.new_x = self.x

    def draw(self, screen):
        # Рассчитываем ширину зеленой полоски, чтобы отображать текущее здоровье
        self.width = self.k_width * self.health
        points = [(self.new_x, self.y), (self.new_x + self.width, self.y),
                  (self.new_x + self.width - self.height, self.y + self.height),
                  (self.new_x - self.height, self.y + self.height)]
        pygame.draw.polygon(screen, self.color_scale, points)
        if self.flag_frame_text:
            # Шрифт
            font = pygame.font.SysFont(None, HealthBar.SIZE_FONT)
            # Создание текста
            text = font.render(self.word, True, self.color_text)
            # Отображение текста
            text_rect = text.get_rect(topleft=(self.x, self.y))
            screen.blit(text, text_rect)
        if self.flag_frame_text:  # нужно для того чтобы у жизней монстров не было рамки
            pygame.draw.polygon(screen, HealthBar.COLOR_OUTLINE, self.outline_points, 2)

    def change_health(self, damage):
        '''Изменяет и отслеживает уровень здоровья.'''
        self.health -= damage
        if self.health <= 0:
            return True
        return False
