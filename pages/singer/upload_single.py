from pages.page import Page


class UploadSinglePage(Page):
    def __init__(self, windows, client, name):
        from components.label import Label
        from components.entry import Entry
        from components.button import Button
        from form.upload_song import UploadSongForm
        super().__init__(windows, client, name)

        self.song_name_label = Label(x=self.windows.get_width() * 0.15, y=self.windows.get_height() * 0.3,
                                     width=self.windows.get_width() * 0.35,
                                     height=self.windows.get_height() * 0.1, text="Song name", windows=windows,
                                     color=(29, 185, 84), text_color=(0, 0, 0))
        self.song_name_entry = Entry(x=(self.song_name_label.rect.x + self.song_name_label.rect.width) * 1.1,
                                     y=self.song_name_label.rect.y,
                                     width=self.song_name_label.rect.width, height=self.song_name_label.rect.height,
                                     windows=windows, color=self.song_name_label.color,
                                     text_color=self.song_name_label.text_color, text="")

        self.audio_path_label = Label(x=self.song_name_label.rect.x,
                                      y=(self.song_name_entry.rect.y + self.song_name_label.rect.height) * 1.1,
                                      width=self.song_name_label.rect.width,
                                      height=self.song_name_label.rect.height, windows=windows, text="Audio path",
                                      color=self.song_name_label.color, text_color=self.song_name_label.text_color)
        self.audio_path_entry = Entry(x=self.song_name_entry.rect.x, y=self.audio_path_label.rect.y,
                                      width=self.song_name_label.rect.width,
                                      height=self.song_name_label.rect.height, windows=windows,
                                      color=self.song_name_label.color, text_color=self.song_name_label.text_color,
                                      text="C:/songs/")

        self.image_path_label = Label(x=self.song_name_label.rect.x,
                                      y=(self.audio_path_entry.rect.y + self.audio_path_entry.rect.height) * 1.1,
                                      width=self.song_name_label.rect.width,
                                      height=self.song_name_label.rect.height, windows=windows, text="Image path",
                                      color=self.song_name_label.color, text_color=self.song_name_label.text_color)
        self.image_path_entry = Entry(x=self.audio_path_entry.rect.x, y=self.image_path_label.rect.y,
                                      width=self.song_name_label.rect.width,
                                      height=self.song_name_label.rect.height, windows=windows,
                                      color=self.song_name_label.color, text_color=self.song_name_label.text_color,
                                      text="C:/images/")

        self.song_duration_label = Label
        self.song_duration_entry = Entry

        self.submit_button = Button(x=0.75 * self.windows.get_width(), y=0.8 * self.windows.get_height(),
                                    width=0.2 * self.windows.get_width(), height=0.1 * self.windows.get_height(),
                                    text="submit", color=self.song_name_label.color,
                                    text_color=self.song_name_label.text_color, windows=windows, page=self,
                                    func=self.client.send_upload_request, args=(self,))

        self.back_button = Button(x=0, y=self.title.rect.y, width=self.submit_button.rect.width * 0.8,
                                  height=self.submit_button.rect.height * 0.8,
                                  text="Back", func=Page.switch,
                                  args=(self.client.previous_page.name, self.windows, self.client, self),
                                  color=self.submit_button.color, text_color=(0, 0, 0),
                                  page=self, windows=self.windows)

        self.response_label = Label(y=self.submit_button.rect.y, color=(0, 0, 0), windows=windows,
                                    width=self.song_name_label.rect.width,
                                    height=self.song_name_label.rect.height, text_color=self.song_name_label.color)
        self.response_label.center_x()

        self.form = UploadSongForm()

        self.components.append(self.song_name_label)
        self.components.append(self.song_name_entry)
        self.components.append(self.audio_path_label)
        self.components.append(self.audio_path_entry)
        self.components.append(self.image_path_label)
        self.components.append(self.image_path_entry)
        self.components.append(self.submit_button)
        self.components.append(self.response_label)
        self.components.append(self.back_button)
