import pygame
from .label import Label


class Entry(Label):
    def __init__(self, width, height, color, windows,text_color=(0, 0, 0), font_size=24, text="", _max=99
                , x=0, y=0):
        super().__init__(x=x, y=y, width=width, height=height, color=color, text_color=text_color, windows=windows,
                         text=text, font_size=font_size)
        self.max = _max
        self.rect_center = pygame.Rect(self.rect.center[0], self.rect.center[1], self.rect.width, self.rect.height)
        self.active = False

    def handle_event(self, event, page):
        if self.drawable:
            if event.type == pygame.MOUSEBUTTONDOWN:
                rect = self.rect
                if rect.collidepoint(event.pos):
                    if page.active_entry is self:
                        page.active_entry = None
                        self.active = False
                    else:
                        page.active_entry = self
                        self.active = True
            elif event.type == pygame.KEYDOWN and page.active_entry == self:

                if event.key == pygame.K_BACKSPACE:
                    if len(str(self.text)) > 0:
                        if len(self.text) > 1:
                            self.text = self.text[:-1]
                        else:
                            self.text = ""
                else:
                    try:
                        self.text += str(event.unicode)
                    except Exception:
                        pass
