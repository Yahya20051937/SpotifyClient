import pygame


class VerticalBorder:
    def __init__(self, x, y, width, height, color, windows):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.windows = windows
        self.components = self.get_components()
        self.drawable = True

    def get_components(self):
        components = []
        for i in range(int(self.height)):
            components.append(pygame.Rect(self.x, self.y + i, self.width, 1))
        return components

    def draw(self):
        if self.drawable:
            for component in self.components:
                pygame.draw.rect(self.windows, self.color, component)


class HorizontalBorder(VerticalBorder):
    def get_components(self):
        components = []
        for i in range(int(self.width)):
            components.append(pygame.Rect(self.x + i, self.y, 1, self.height))
        return components
