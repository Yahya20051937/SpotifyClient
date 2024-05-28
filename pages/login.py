from pages.page import Page


class LoginPage(Page):
    def __init__(self, windows, client, name):
        from components.label import Label
        from components.button import Button
        from components.image import Image
        from components.entry import Entry
        from components.check_box import CheckBox
        from form.login import LoginForm
        super().__init__(windows, client, name)

        self.username_label = Label(x=0.15 * self.windows.get_width(), y=0.18 * self.windows.get_height(),
                                    width=0.35 * self.windows.get_width(), height=0.1 * self.windows.get_height(),
                                    windows=self.windows, text="username", color=(29, 185, 84))
        self.username_entry = Entry(x=(self.username_label.rect.x + self.username_label.rect.width) * 1.1,
                                    y=self.username_label.rect.y, width=self.username_label.rect.width,
                                    height=self.username_label.rect.height
                                    , windows=self.windows, color=self.username_label.color, text="")
        self.password_label = Label(x=0.15 * self.windows.get_width(),
                                    y=(self.username_entry.rect.y + self.username_entry.rect.height) * 1.1,
                                    width=0.35 * self.windows.get_width(), height=0.1 * self.windows.get_height(),
                                    windows=self.windows, text="password", color=(29, 185, 84))

        self.password_entry = Entry(x=(self.username_label.rect.x + self.username_label.rect.width) * 1.1,
                                    y=self.password_label.rect.y, width=self.username_label.rect.width,
                                    height=self.username_label.rect.height, windows=self.windows,
                                    color=self.username_label.color, text="")

        self.image = Image(load="resources/spotify.png",
                           y=(self.password_entry.rect.y + self.password_entry.rect.height) * 1.1,
                           width=self.windows.get_width() * 0.3, height=(self.windows.get_height() - (
                    self.password_entry.rect.y + self.password_entry.rect.height)) * 0.8, windows=self.windows, x=0)

        self.submit_button = Button(x=self.windows.get_width() * 0.7,
                                    y=self.image.rect.y + self.image.rect.height - 0.1 * self.windows.get_height(),
                                    width=0.2 * self.windows.get_width(), height=0.1 * self.windows.get_height()
                                    , color=(29, 185, 84), text="submit", func=self.client.send_authentication_request,
                                    args=(self,), page=self, windows=self.windows)

        self.save_credentials_label = Label(y=self.image.rect.y, width=self.submit_button.rect.width,
                                            height=self.submit_button.rect.height * 0.8,
                                            windows=windows, text="Save credentials",
                                            text_color=self.submit_button.color, color=(0, 0, 0))
        self.save_credentials_label.center_x()
        self.save_credentials_checkbox = CheckBox(
            x=(self.save_credentials_label.rect.x + self.save_credentials_label.rect.width) * 1.05,
            y=self.image.rect.y, width=self.submit_button.rect.width * 0.6, height=self.submit_button.rect.height * 0.9,
            windows=windows)

        self.form = LoginForm()

        self.response_label = Label(y=self.windows.get_height() - self.title.rect.height, width=self.title.rect.width,
                                    height=self.title.rect.height, windows=self.windows, text_color=(29, 185, 84),
                                    color=(0, 0, 0))
        self.back_button = Button(x=0, y=self.title.rect.y, width=self.submit_button.rect.width * 0.8,
                                  height=self.submit_button.rect.height * 0.8,
                                  text="Back", func=Page.switch,
                                  args=(self.client.previous_page.name, self.windows, self.client, self),
                                  color=self.submit_button.color, text_color=(0, 0, 0),
                                  page=self, windows=self.windows)
        self.response_label.drawable = False
        self.response_label.center_x()

        self.components.append(self.username_label)
        self.components.append(self.username_entry)
        self.components.append(self.password_label)
        self.components.append(self.password_entry)
        self.components.append(self.submit_button)
        self.components.append(self.image)
        self.components.append(self.response_label)
        self.components.append(self.save_credentials_label)
        self.components.append(self.save_credentials_checkbox)
        self.components.append(self.back_button)

    def build_form(self):
        self.form.username = self.username_entry.text
        self.form.password = self.password_entry.text
