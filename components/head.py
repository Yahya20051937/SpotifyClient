import pygame.rect


class Head:
    def __init__(self, width, height, windows, x, y, color, bar_size, initial_position):
        self.initial_position = initial_position
        self.bar_size = bar_size
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.windows = windows
        self.color = color
        self.clicked = False
        self.position_updated = False
        self.drawable = True
        self.initial_y = y

    def draw(self):
        if self.drawable:
            pygame.draw.rect(self.windows, self.color, self.rect)

    def update_horizontal_position(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.x <= pygame.mouse.get_pos()[0] <= self.rect.x + self.rect.width and self.rect.y <= \
                    pygame.mouse.get_pos()[1] <= self.rect.y + self.rect.height:
                self.clicked = True
            else:
                if self.clicked:
                    mouse_x_position = pygame.mouse.get_pos()[0]
                    if self.initial_position <= mouse_x_position <= self.initial_position + self.bar_size:
                        self.rect.x = mouse_x_position
                        self.position_updated = True
        else:
            self.clicked = False

    def update_vertical_position(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.x <= pygame.mouse.get_pos()[0] <= self.rect.x + self.rect.width and self.rect.y <= \
                    pygame.mouse.get_pos()[1] <= self.rect.y + self.rect.height:
                self.clicked = True
            else:
                if self.clicked:
                    mouse_y_position = pygame.mouse.get_pos()[1]
                    if self.initial_position <= mouse_y_position <= self.initial_position + self.bar_size - self.rect.height:
                        self.rect.y = mouse_y_position
                        self.position_updated = True
        else:
            self.clicked = False

    def get_y_variation_percentage(self):
        """
        self.initial_y + (self.bar_size - self.rect.height) - self.initial_y - > 100%
        self.rect.y - self.initial_y -> ?
        :return:
        """
        return (self.rect.y - self.initial_y) / (
                    self.bar_size - self.rect.height)


