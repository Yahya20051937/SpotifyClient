from components.singer_component import SingerComponent


class PlaylistComponent(SingerComponent):
    def __init__(self, spotify_object, x, box_y, box_height, width, height, windows, client, index, font_size, color):
        super().__init__(spotify_object, x, box_y, box_height, width, height, windows, client, index, font_size, color)
        from components.button import Button
        from components.image import ImageButton
        self.play_button = ImageButton(load="resources/play_button.png", width=0.1 * self.width,
                                       height=0.6 * self.height, windows=windows,
                                       x=self.x + 0.85 * self.width, y=self.y + self.height * 0.2,
                                       func=self.play)
        self.browse_playlist_button = Button(width=self.label.rect.width * 0.7, height=self.label.rect.height,
                                             color=self.label.color,
                                             x=self.label.rect.x + self.label.rect.width*0.2, y=self.label.rect.y, text_color=self.label.text_color,
                                             text=
                                             self.label.text, page=client.current_page,
                                             func=self.add_playlist_songs_to_box, windows=windows)
        self.browse_playlist_button.drawable = True
        self.sub_components.append(self.browse_playlist_button)
        self.sub_components.append(self.play_button)
        self.sub_components.append(self.sub_label)

        self.sub_label.text = "playlist"

    def add_playlist_songs_to_box(self):
        self.client.current_playlist = self.spotify_object
        self.client.current_mode = "playlist"
        box = self.client.current_page.box
        box.clear()
        playlist = self.spotify_object
        for song in playlist.songs:
            box.add_component(spotify_object=song)

    def play(self):
        from entity.stream import Stream
        self.client.streaming = False
        playlist = self.spotify_object
        self.client.stream_active = True
        for song in reversed(playlist.songs):
            print(song.name)
            stream = Stream(audio=song, starting_time=0)
            self.client.streaming_queue.appendleft(stream)

    def update_vertical_position(self, y):
        self.y = y
        self.y = y
        self.image.rect.y = self.y + self.height * 0.1
        self.label.rect.y = self.y + 0.1 * self.height
        self.sub_label.rect.y = self.y + self.height * 0.9
        self.play_button.rect.y = self.y + self.height * 0.2
        self.image.rect.y = self.y + self.height * 0.1
        self.browse_playlist_button.rect.y = self.y + 0.1 * self.height
        self.play_button.rect.y = self.y + self.height * 0.2
        self.sub_label.rect.y = self.y + self.height * 0.9
        if self.y < self.box_y or self.y > self.box_y + self.box_height:
            self.make_elements_drawable(False)
        else:
            self.make_elements_drawable(True)


class SubPlaylistComponent(SingerComponent):
    def __init__(self, func, args, spotify_object, x, box_y, box_height, width, height, windows, client, index,
                 font_size, color,
                 ):
        super().__init__(spotify_object, x, box_y, box_height, width, height, windows, client, index, font_size, color)
        from components.button import Button
        self.sub_label.drawable = False
        self.func = func
        self.args = args
        self.add_or_remove_to_playlist_button = Button(width=self.label.rect.width, height=self.label.rect.height,
                                                       color=self.label.color, x=self.label.rect.x, y=self.label.rect.y,
                                                       text_color=self.label.text_color, func=func, args=args,
                                                       page=self.client.current_page, text="", windows=windows)
        self.add_or_remove_to_playlist_button.drawable = False
        self.add_or_remove_to_playlist_button.clickable_while_not_drawable = True
        self.sub_components.append(self.add_or_remove_to_playlist_button)

    def update_vertical_position(self, y):
        self.y = y
        self.image.rect.y = self.y + self.height * 0.1
        self.label.rect.y = self.y + 0.1 * self.height
        self.add_or_remove_to_playlist_button.rect.y = self.y + 0.1 * self.height
        self.image.rect.y = self.y + self.height * 0.1
        if self.y < self.box_y or self.y > self.box_y + self.box_height:
            self.make_elements_drawable(False)
        else:
            self.make_elements_drawable(True)
        self.add_or_remove_to_playlist_button.drawable = False
        self.sub_label.drawable = False
