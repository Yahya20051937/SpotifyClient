import pygame.rect


class VolumeBar:
    MAX_VALUE = 10
    MIN_VALUE = -20

    def __init__(self, x, y, width, height, inf_color, sup_color, windows, client):
        from components.head import Head
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.components = dict()
        self.drawable = False
        self.windows = windows
        self.inf_color = inf_color
        self.sup_color = sup_color
        self.volume_head = Head(width=self.width * 0.02, height=self.height * 5, x=self.x + self.width * 0.5,
                                y=self.y - self.height, bar_size=self.width, color=self.inf_color, windows=
                                windows, initial_position=self.x)
        self.client = client
        self.get_components()

    def get_components(self):
        self.components = dict()
        unit_width = self.width / (VolumeBar.MAX_VALUE - VolumeBar.MIN_VALUE)
        for i in range(VolumeBar.MAX_VALUE - VolumeBar.MIN_VALUE):
            self.components[VolumeBar.MIN_VALUE + i] = pygame.rect.Rect(self.x + i * unit_width, self.y, unit_width,
                                                                        self.height)

    def draw(self):
        if self.drawable:
            for key in self.components.keys():
                if key >= self.client.volume_padding:
                    color = self.sup_color
                else:
                    color = self.inf_color
                pygame.draw.rect(self.windows, color, self.components[key])
            self.volume_head.draw()
            self.volume_head.position_updated = True  # this to fix the head and sound positions
            self.update()

    def update(self):
        if self.volume_head.position_updated:
            self.client.mute = False
            for i in range(VolumeBar.MAX_VALUE - VolumeBar.MIN_VALUE):
                if self.volume_head.rect.colliderect(self.components[VolumeBar.MIN_VALUE + i]):
                    if i == 0:
                        self.client.mute = True
                    else:
                        self.client.volume_padding = VolumeBar.MIN_VALUE + i
                        break
            self.volume_head.position_updated = False
