from pages.page import Page


class MainPageU(Page):
    def __init__(self, windows, client, name):
        from components.search_bar import SearchBar
        from components.media_player import MediaPlayer
        from components.box import Box
        from components.button import Button
        from components.label import Label
        from components.entry import Entry

        super().__init__(windows, client, name)

        self.search_bar = SearchBar(x=self.windows.get_width() * 0.25, y=0.13 * self.windows.get_height(),
                                    width=0.6 * self.windows.get_width(), height=0.1 * self.windows.get_height()
                                    , color=(29, 185, 84), text_color=(0, 0, 0), windows=windows,
                                    func=self.client.send_search_request, page=self)

        self.search_bar.add_components(self)

        self.box = Box(y=self.windows.get_height() * 0.25,
                       width=0.8 * self.windows.get_width(),
                       height=0.5 * self.windows.get_height(), color=(29, 185, 84), border_color=(29, 185, 84),
                       page=self,
                       windows=windows, x=self.windows.get_width() * 0.1)

        self.media_player = MediaPlayer(x=0, y=self.windows.get_height() * 0.79, width=self.windows.get_width(),
                                        height=0.15 * self.windows.get_width(), page=self, windows=windows)

        self.playlists_button = Button(width=0.15 * self.windows.get_width(), height=0.1 * self.windows.get_height(),
                                       x=0.05 * self.windows.get_width(), y=self.search_bar.y,
                                       color=(29, 185, 84), text_color=(0, 0, 0), windows=windows, page=self,
                                       func=self.add_playlists_to_box, text="My playlists")
        self.logout_button = Button(x=self.search_bar.button.rect.x, y=self.title.rect.y * 0.8,
                                    width=self.playlists_button.rect.width,
                                    height=self.playlists_button.rect.height * 0.8, color=self.playlists_button.color,
                                    text_color=(0, 0, 0),
                                    page=self, windows=windows, text="LOGOUT", func=self.client.logout)
        self.create_playlist_button = Button(x=self.windows.get_width() * 0.01, y=self.logout_button.rect.y,
                                             width=self.logout_button.rect.width * 0.7,
                                             height=self.logout_button.rect.height * 0.8,
                                             color=self.logout_button.color,
                                             page=self, windows=windows, text="Create Playlist",
                                             func=self.activate_add_playlist_components, font_size=12)
        self.playlist_name_label = Label(
            x=(self.create_playlist_button.rect.x + self.create_playlist_button.rect.width) * 1.1,
            y=self.logout_button.rect.y, width=self.create_playlist_button.rect.width,
            height=self.create_playlist_button.rect.height,
            windows=windows, color=self.logout_button.color, text_color=self.logout_button.text_color,
            text="Playlist's name : ", font_size=12)
        self.playlist_name_entry = Entry(
            x=(self.playlist_name_label.rect.x + self.playlist_name_label.rect.width) * 1.1,
            y=self.logout_button.rect.y, width=self.create_playlist_button.rect.width,
            height=self.create_playlist_button.rect.height,
            windows=windows, color=self.logout_button.color, text_color=self.logout_button.text_color, font_size=12)

        self.playlist_name_entry.drawable = False
        self.playlist_name_label.drawable = False

        self.components.append(self.playlists_button)
        self.components.append(self.logout_button)
        self.components.append(self.create_playlist_button)
        self.components.append(self.playlist_name_entry)
        self.components.append(self.playlist_name_label)

    def update(self):
        self.client.update()
        self.box.update()
        self.media_player.update()

    def add_playlists_to_box(self):
        self.box.clear()
        for playlist in self.client.playlists:
            self.box.add_component(playlist, cls=playlist.__class__.COMPONENT_CLASS)

    def activate_add_playlist_components(self):
        self.playlist_name_label.drawable = True
        self.playlist_name_entry.drawable = True
        self.title.drawable = False
        self.create_playlist_button.text = "Send"
        self.create_playlist_button.func = self.create_playlist

    def create_playlist(self):
        self.playlist_name_label.drawable = False
        self.playlist_name_entry.drawable = False
        self.title.drawable = True
        self.create_playlist_button.text = "Create Playlist"
        self.create_playlist_button.func = self.activate_add_playlist_components
        self.client.send_create_playlist_request(name=self.playlist_name_entry.text)
        self.playlist_name_entry.text = ""
