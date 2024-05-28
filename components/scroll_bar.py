import pygame.rect


class ScrollBar:
    def __init__(self, x, y, width, height, color, page, head_color):
        from components.head import Head
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.color = color
        self.page = page
        self.drawable = False
        self.scroll_head = Head(width=self.rect.width, height=0.08 * self.rect.height, x=self.rect.x, y=self.rect.y,
                                bar_size=self.rect.height, initial_position=self.rect.y, color=head_color, windows=page.windows)

    def draw(self):
        if self.drawable:
            pygame.draw.rect(self.page.windows, self.color, self.rect)
            self.scroll_head.draw()




