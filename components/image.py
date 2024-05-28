import time

import pygame.image
from components.label import Label


class Image(Label):
    def __init__(self, width, height, windows, x=0, y=0, load="resources/black.png"):
        super().__init__(width=width, height=height, windows=windows, x=x, y=y)
        self.load = load
        self.rect = pygame.Rect(x, y, width, height)
        self.windows = windows
        self.surface = pygame.transform.scale(pygame.image.load(load), (self.rect.width, self.rect.height))

    def draw(self):
        if self.drawable:
            self.windows.blit(self.surface, (self.rect.x, self.rect.y))

    def update_load(self, load):
        self.load = load
        self.surface = pygame.transform.scale(pygame.image.load(load), (self.rect.width, self.rect.height))


class ImageButton(Image):
    def __init__(self, load, width, height, windows, x, y, func, args=()):
        super().__init__(load=load, width=width, height=height, windows=windows, x=x, y=y)
        self.func = func
        self.args = args

    def handle_event(self, event):
        if self.drawable:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.func(*self.args)
