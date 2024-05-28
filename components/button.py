import pygame

from .label import Label


class Button(Label):
    def __init__(self, width, height, color, func, windows, text, page, args=(), x=0, y=0, text_color=(0, 0, 0), font_size=21):
        super().__init__(x=x, y=y, width=width, height=height, color=color, text_color=text_color, windows=windows,
                         text=text, font_size=font_size)
        self.func = func
        self.args = args
        self.page = page
        self.clickable_while_not_drawable = False

    def handle_event(self, event):
        if self.drawable or self.clickable_while_not_drawable:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.func(*self.args)
