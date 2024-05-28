import base64
import io

import pygame


class MediaPlayer:
    def __init__(self, x, y, width, height, windows, page):
        from components.functions import get_borders
        from components.image import ImageButton, Image
        from components.label import Label
        from components.streaming_bar import StreamingBar
        from components.volume_bar import VolumeBar
        from entity.time import Time

        self.song = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.windows = windows
        self.page = page
        self.current_time = Time(0)
        self.full_time = Time(0)
        self.active = False
        self.paused = False
        self.borders = get_borders(self.x, self.y, self.width, self.height, self.windows, color=(29, 185, 84))

        self.pause_play_button = ImageButton(load="resources/pause.png", x=self.x + self.width * 0.45,
                                             y=self.y + self.height * 0.1,
                                             width=0.1 * self.width, height=0.3 * self.height, func=self.pause,
                                             windows=self.windows)
        self.next_button = ImageButton(load="resources/next.png", x=self.x + self.width * 0.56, y=self.pause_play_button.rect.y, width=
                                       self.pause_play_button.rect.width, height=self.pause_play_button.rect.height, func=self.next, windows=windows)

        self.song_image = Image(width=self.width * 0.17, height=self.height * 0.35, x=self.x + self.width * 0.05,
                                y=self.y + self.height * 0.1, windows=windows)

        self.song_name_label = Label(x=self.song_image.rect.x + self.song_image.rect.width * 0.35,
                                     y=self.song_image.rect.y * 1.1,
                                     width=self.song_image.rect.width * 0.3,
                                     height=0.05 * self.height, windows=windows, text_color=(29, 185, 84),
                                     color=(0, 0, 0), font_size=12
                                     )

        self.artist_name_label = Label(
            x=self.song_name_label.rect.x + self.song_name_label.rect.width * 0.4,
            y=self.song_name_label.rect.y * 1.01, width=self.song_name_label.rect.width * 0.2,
            height=self.height * 0.25, windows=windows,
            text_color=(28, 185, 84), color=(0, 0, 0), font_size=10)

        self.streaming_bar = StreamingBar(width=0.5 * self.width, height=0.01 * self.height,
                                          x=self.x + self.width * 0.27, y=self.song_name_label.rect.y,
                                          pre_color=(192, 192, 192), post_color=(29, 185, 84), windows=windows,
                                          client=page.client)
        self.volume_bar = VolumeBar(width=0.15 * self.width, height=0.01 * self.height, x=self.width * 0.80,
                                    y=self.pause_play_button.rect.y * 1.05, client=page.client,
                                    inf_color=(28, 185, 84), sup_color=(192, 192, 192), windows=windows)

        self.current_time_label = Label(width=0.1 * self.streaming_bar.width, height=0.25 * self.height, font_size=12,
                                        x=self.streaming_bar
                                        .x, y=(self.streaming_bar.y * 1.01), text=str(self.current_time),
                                        windows=self.windows,
                                        color=
                                        (0, 0, 0), text_color=(29, 185, 84))
        self.full_time_label = Label(width=0.1 * self.streaming_bar.width, height=0.25 * self.height, font_size=12,
                                     x=self.streaming_bar
                                     .x + self.streaming_bar.width * 0.9, y=(self.streaming_bar.y * 1.01),
                                     windows=self.windows,
                                     color=
                                     (0, 0, 0), text_color=(29, 185, 84))

        self.components = [b for b in self.borders] + [self.song_image, self.song_name_label, self.artist_name_label,
                                                       self.streaming_bar, self.pause_play_button,
                                                       self.current_time_label,
                                                       self.full_time_label, self.volume_bar, self.next_button
                                                       ]

        self.streamed_bytes = 0

        self.make_elements_drawable_(False)
        self.add_components_to_page()

    def activate(self, song, starting_time):
        self.current_time = starting_time
        self.streamed_bytes = song.bit_rate * starting_time.get_seconds_value() * 0.125
        self.streaming_bar.current_time = self.current_time
        self.active = True
        self.song = song
        self.full_time_label.text = str(self.song.time)
        self.song_image.surface = pygame.transform.scale(
            pygame.image.load(io.BytesIO(base64.b64decode(song.image_bytes))),
            (self.song_image.rect.width, self.song_image.rect.height))
        self.song_name_label.text = song.name
        self.artist_name_label.text = song.singer.name
        self.streaming_bar.get_components(song=song)

        self.make_elements_drawable_(True)

    def make_elements_drawable_(self, boolean: bool):
        for component in self.components:
            component.drawable = boolean

    def add_components_to_page(self):
        for component in self.components:
            self.page.components.append(component)

    def update(self):
        from entity.time import Time
        if self.active:
            self.current_time = Time(self.streamed_bytes / (self.song.bit_rate * 0.125))
            self.streaming_bar.current_time = self.current_time
            self.streaming_bar.head.rect.x = self.streaming_bar.x + self.current_time.get_seconds_value() * (
                        self.streaming_bar.width / self.song.time.get_seconds_value())

            self.current_time_label.text = str(self.current_time)
            self.streaming_bar.head.update_horizontal_position()
            self.volume_bar.volume_head.update_horizontal_position()

    def pause(self):
        self.pause_play_button.update_load("resources/play_button.png")
        self.page.client.stream_paused = True
        self.pause_play_button.func = self.play

    def play(self):
        self.pause_play_button.update_load("resources/pause.png")
        self.page.client.stream_paused = False
        self.pause_play_button.func = self.pause

    def next(self):
        self.page.client.streaming = False
        if len(self.page.client.streaming_queue) == 0:
            self.page.client.stream_active = False
            self.make_elements_drawable_(False)

