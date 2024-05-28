import math
import time

import pygame


class Label:
    VEL = 20

    def __init__(self, width, height, windows, color=(250, 250, 250), text_color=(0, 0, 0), font_size=24, text="", x=0, y=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = str(text)
        self.text_color = text_color
        self.windows = windows
        self.font_size = font_size
        self.drawable = True

    def center_x(self):
        self.rect.x = self.windows.get_width() / 2 - (self.rect.width / 2)

    def center_y(self):
        self.rect.y = self.windows.get_height() / 2 - (self.rect.height / 2)

    def center(self):
        self.center_x()
        self.center_y()

    def change_coordinate(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        if self.drawable:
            try:
                pygame.draw.rect(self.windows, self.color, self.rect)
                font = pygame.font.SysFont("calibri", self.font_size)
                text_surface = font.render(str(self.text), True, self.text_color)
                text_rect = text_surface.get_rect(center=self.rect.center)
                self.windows.blit(text_surface, text_rect)
            except KeyboardInterrupt:
                pass

    def move_to(self, position):
        if self.rect.x != _round(position.x):
            self.move_horizontally_to(position)
            return

        if self.rect.y != _round(position.y):
            self.move_vertically_to(position)

    def move_horizontally_to(self, position):
        if self.rect.x > position.x:
            difference = self.rect.x - position.x
            if difference > Label.VEL:
                self.rect.x -= Label.VEL
            else:
                self.rect.x = _round(position.x)
        else:
            difference = position.x - self.rect.x
            if difference > Label.VEL:
                self.rect.x += Label.VEL
            else:
                self.rect.x = _round(position.x)

    def move_vertically_to(self, position):
        if self.rect.y > position.y:
            if self.rect.y - Label.VEL > position.y:
                self.rect.y -= Label.VEL
            else:
                self.rect.y = _round(position.y)

        elif self.rect.y < position.y:
            if self.rect.y + Label.VEL < position.y:
                self.rect.y += Label.VEL
            else:
                self.rect.y = _round(position.y)

    def is_in_position(self, position):
        if self.rect.x == _round(position.x) and self.rect.y == _round(position.y):
            return True
        return False

    def change_size_and_coordinates(self, x, y, width, height):
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height


def _round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)
