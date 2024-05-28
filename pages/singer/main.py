from pages.page import Page


class MainPageS(Page):
    def __init__(self, windows, client, name):
        from components.button import Button
        from components.label import Label
        super().__init__(windows, client, name)

        self.subtitle = Label(width=self.title.rect.width * 0.8, height=self.title.rect.height * 0.8, windows=windows,
                              color=self.title.color,
                              text=f"SINGER DASHBOARD", text_color=self.title.text_color,
                              y=(self.title.rect.y + self.title.rect.height) * 1.1)
        self.subtitle.center_x()

        self.upload_single_button = Button(y=0.4 * self.windows.get_height(), width=0.5 * self.windows.get_width(),
                                           height=0.1 * self.windows.get_height(), color=(29, 185, 84),
                                           text="upload single", func=Page.switch,
                                           args=("upload_single", windows, client, self), windows=windows, page=self)
        self.upload_album_button = Label(
            y=(self.upload_single_button.rect.y + self.upload_single_button.rect.height) * 1.1,
            width=self.upload_single_button.rect.width,
            height=self.upload_single_button.rect.height, text="upload album",
            windows=windows, color=self.upload_single_button.color)
        self.logout_button = Button(x=self.windows.get_width() * 0.8, y=self.title.rect.y * 0.8,
                                    width=self.windows.get_width() * 0.2,
                                    height=self.windows.get_height() * 0.08, color=(29, 185, 84),
                                    text_color=(0, 0, 0),
                                    page=self, windows=windows, text="LOGOUT", func=self.client.logout)

        self.upload_single_button.center_x()
        self.upload_album_button.center_x()

        self.components.append(self.subtitle)
        self.components.append(self.upload_single_button)
        self.components.append(self.upload_album_button)
        self.components.append(self.logout_button)
