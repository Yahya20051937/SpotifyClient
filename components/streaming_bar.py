import pygame.rect


class StreamingBar:
    def __init__(self, x, y, width, height, pre_color, post_color, windows, client):
        from entity.time import Time
        from components.head import Head
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pre_color = pre_color
        self.post_color = post_color
        self.components = []
        self.current_time = Time(0)
        self.client = client
        self.head = Head(x=self.x, y=self.y - self.height, width=self.width * 0.02, height=self.height * 5,
                         color=(0, 250, 0),
                         windows=windows, bar_size=self.width, initial_position=self.x)
        self.windows = windows
        self.drawable = False

    def get_components(self, song):
        self.components = []
        song_time = song.time.get_seconds_value()
        unit_width = self.width / song_time
        for i in range(song_time):
            self.components.append(pygame.rect.Rect(self.x + i * unit_width, self.y, unit_width, self.height))

    def draw(self):
        if self.drawable:
            for i in range(len(self.components)):
                if i > self.current_time.get_seconds_value():
                    pygame.draw.rect(self.windows, self.pre_color, self.components[i])
                else:
                    pygame.draw.rect(self.windows, self.post_color, self.components[i])

            self.head.draw()
            self.update()

    def update(self):
        from entity.stream import Stream
        if self.head.position_updated and not pygame.mouse.get_pressed()[0]:
            unit_width = self.width / self.client.current_stream.audio.time.get_seconds_value()
            target_second = int((self.head.rect.x - self.x) / unit_width)
            stream = Stream(audio=self.client.current_stream.audio, starting_time=target_second)
            self.client.streaming = False
            self.client.streaming_queue.appendleft(stream)
            self.head.position_updated = False
