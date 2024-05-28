import time

from components.singer_component import SingerComponent


class SongComponent(SingerComponent):
    def __init__(self, spotify_object, x, box_y, box_height, width, height, windows, client, index, font_size, color):
        from components.image import ImageButton
        from components.label import Label
        from components.widget import Widget
        from components.box import Box
        super().__init__(spotify_object, x, box_y, box_height, width, height, windows, client, index, font_size, color)
        self.sub_label.text = "song"

        self.play_button = ImageButton(load="resources/play_button.png", width=0.1 * self.width,
                                       height=0.6 * self.height, windows=windows,
                                       x=self.x + 0.85 * self.width, y=self.y + self.height * 0.2,
                                       func=self.play)

        self.song_duration_label = Label(x=self.x + 0.7 * self.width, y=self.sub_label.rect.y,
                                         width=self.sub_label.rect.width, font_size=12,
                                         height=self.sub_label.rect.height,
                                         text=str(self.spotify_object.time), windows=windows, color=(29, 185, 84),
                                         text_color=(0, 0, 0))
        self.widget = Widget(x=self.x + self.width * 0.65, y=self.y, width=self.width * 0.3,
                             height=self.height,
                             buttons_dicts=[
                                 {"text": "Add to Playlist", "func": self.display_playlists, "args": ("add",)},
                                 {"text": "Remove from Playlist", "func": self.display_playlists,
                                  "args": ("remove",)},
                                 {"text": "Add to queue", "func": self.add_to_queue, "args": ()},
                                 {"text": "Show metrics", "func": self.show_metrics, "args": ()}],
                             page=self.client.current_page,
                             windows=self.windows)
        self.activate_widget_button = ImageButton(x=(self.play_button.rect.x + self.play_button.rect.width) * 1.02,
                                                  y=self.play_button.rect.y + self.play_button.rect.height * 0.5,
                                                  width=0.02 * self.width, height=0.1 * self.height,
                                                  windows=windows, func=self.client.current_page.box.set_active_widget,
                                                  args=(self.widget,), load="resources/dot.png")

        self.playlists_box = Box(x=self.widget.x - self.widget.width * 0.7, y=self.widget.y,
                                 width=self.widget.width * 0.6,
                                 height=self.widget.height * 0.8, color=(64, 64, 64), page=self.client.current_page,
                                 windows=self.windows, font_size=10, max_size=3, head_width_percentage=0.1,
                                 head_color=(250, 0, 0))
        self.widget.box = self.playlists_box

        self.widget.make_elements_drawable(False)

        if self.client.is_song_liked(song=spotify_object):
            func = self.dislike
            load = 'resources/dislike.png'
        else:
            func = self.like
            load = 'resources/like.png'

        self.like_dislike_button = ImageButton(load=load, width=0.1 * self.width,
                                               height=0.5 * self.height,
                                               x=self.song_duration_label.rect.x, y=self.play_button.rect.y,
                                               func=func,
                                               windows=windows)

        self.nb_streams_label = Label(x=self.sub_label.rect.x * 0.95, y=self.like_dislike_button.rect.y,
                                      width=self.song_duration_label.rect.width,
                                      height=self.song_duration_label.rect.height, font_size=10, windows=windows,
                                      text=f"{spotify_object.nb_streams} stream", color=self.sub_label.color,
                                      text_color=(0, 0, 0))
        self.nb_likes_label = Label(x=self.sub_label.rect.x * 0.95,
                                    y=(self.nb_streams_label.rect.y + self.nb_streams_label.rect.height) * 1.02,
                                    width=self.song_duration_label.rect.width * 0.85,
                                    height=self.song_duration_label.rect.height, font_size=10, windows=windows,
                                    text=f"{spotify_object.nb_likes} like", color=self.sub_label.color,
                                    text_color=(0, 0, 0))
        self.nb_likes_label.drawable = False
        self.nb_streams_label.drawable = False

        self.sub_components.append(self.play_button)
        self.sub_components.append(self.song_duration_label)
        self.sub_components.append(self.like_dislike_button)
        self.sub_components.append(self.activate_widget_button)
        self.sub_components.append(self.widget)
        self.sub_components.append(self.nb_streams_label)
        self.sub_components.append(self.nb_likes_label)
        self.sub_components += [b for b in self.widget.buttons]
        self.sub_components.append(self.playlists_box.scroll_bar)

    def activate_widget(
            self):  # when this button is clicked we make the elements in the widget drawable, deactivate both the play and like buttons, and set the current active widget
        self.widget.make_elements_drawable(True)
        self.like_dislike_button.drawable = False
        self.play_button.drawable = False
        self.activate_widget_button.args = (None,)

    def deactivate_widget(self):
        self.like_dislike_button.drawable = True
        self.play_button.drawable = True
        self.update_vertical_position(y=self.y)
        self.widget.make_elements_drawable(boolean=False)
        self.playlists_box.clear()
        self.activate_widget_button.args = (self.widget,)
        self.playlists_box.scroll_bar.drawable = False

    def play(self):
        from entity.stream import Stream
        self.client.streaming = False
        stream = Stream(audio=self.spotify_object, starting_time=0)
        self.client.streaming_queue.appendleft(stream)
        self.client.stream_active = True

    def like(self):
        self.like_dislike_button.update_load("resources/dislike.png")
        self.like_dislike_button.func = self.dislike
        self.client.send_add_remove_song_to_playlist_request(song=self.spotify_object,
                                                             playlist=self.client.liked_songs_playlist,
                                                             add_or_remove="add")

    def dislike(self):
        self.like_dislike_button.update_load("resources/like.png")
        self.like_dislike_button.func = self.like
        self.client.send_add_remove_song_to_playlist_request(song=self.spotify_object,
                                                             playlist=self.client.liked_songs_playlist,
                                                             add_or_remove="remove")

    def update_like_button(self, client):
        if self.spotify_object.id in [s.id for s in client.liked_songs_playlist.songs]:
            self.like_dislike_button.update_load("resources/dislike.png")
            self.like_dislike_button.func = self.dislike
        else:
            self.like_dislike_button.update_load("resources/like.png")
            self.like_dislike_button.func = self.like

    def add_to_queue(self):
        from entity.stream import Stream
        self.playlists_box.clear()
        self.client.stream_active = True
        self.client.streaming_queue.append(Stream(audio=self.spotify_object, starting_time=0))

    def show_metrics(self):
        self.widget.buttons[-1].text = "Hide metrics"
        self.widget.buttons[-1].func = self.hide_metrics
        self.get_updated()
        self.nb_likes_label.drawable = True
        self.nb_streams_label.drawable = True

    def hide_metrics(self):
        self.widget.buttons[-1].text = "Show metrics"
        self.widget.buttons[-1].func = self.show_metrics
        self.nb_likes_label.drawable = False
        self.nb_streams_label.drawable = False

    def display_playlists(self, add_or_remove="add"):
        self.playlists_box.clear()
        for playlist in self.client.playlists:
            valid = False
            if add_or_remove == "add":
                if self.spotify_object.id not in [song.id for song in playlist.songs]:
                    valid = True
            if add_or_remove == "remove":
                if self.spotify_object.id in [song.id for song in playlist.songs]:
                    valid = True
            if valid:
                self.playlists_box.add_component(spotify_object=playlist, cls=playlist.__class__.SUBCOMPONENT_CLASS,
                                                 args=(self.remove_or_add_to_playlist,
                                                       (playlist, add_or_remove)))
            # args = (func, (song, playlist, add_or_remove))

    def remove_or_add_to_playlist(self, playlist, add_or_remove):
        send_request = False
        if add_or_remove == "add":
            if self.spotify_object.id not in [s.id for s in playlist.songs]:
                send_request = True
        else:
            if self.spotify_object.id in [s.id for s in playlist.songs]:
                send_request = True
        if send_request:
            self.client.send_add_remove_song_to_playlist_request(self.spotify_object, playlist, add_or_remove)

    def get_updated(self):
        song = self.spotify_object
        song.update_nb_likes(client=self.client)
        song.update_nb_streams(client=self.client)
        self.nb_likes_label.text = f"{song.nb_likes} like"
        self.nb_streams_label.text = f"{song.nb_streams} stream"

    def update(self):
        self.playlists_box.update()

    def update_vertical_position(self, y):
        self.y = y
        self.image.rect.y = self.y + self.height * 0.1
        self.label.rect.y = self.y + 0.1 * self.height
        self.sub_label.rect.y = self.y + self.height * 0.9
        self.play_button.rect.y = self.y + self.height * 0.2
        self.like_dislike_button.rect.y = self.play_button.rect.y
        self.song_duration_label.rect.y = self.sub_label.rect.y
        self.activate_widget_button.rect.y = self.y + self.height * 0.5
        self.nb_likes_label.rect.y = self.like_dislike_button.rect.y
        self.nb_streams_label.rect.y = (self.nb_likes_label.rect.y + self.nb_likes_label.rect.height) * 1.02
        self.widget.update_vertical_position(y=self.y)
        self.playlists_box.update_vertical_position(y=self.y)

        if self.y < self.box_y or self.y > self.box_y + self.box_height:
            self.make_elements_drawable(False)
        else:
            self.make_elements_drawable(True)
            # this to unsure that even if element is within the box, we only draw the widget's element if it's active
            if self.widget is not None:
                if not self.widget_activated:
                    self.widget.make_elements_drawable(False)
        self.nb_likes_label.drawable = False
        self.nb_streams_label.drawable = False
        self.playlists_box.scroll_bar.drawable = False
