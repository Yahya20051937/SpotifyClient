from pages.page import Page


class HomePage(Page):
    def __init__(self, windows, client, name):
        from components.label import Label
        from components.button import Button
        from components.image import Image
        super().__init__(windows, client, name)

        self.login_button = Button(width=self.windows.get_width() * 0.5, height=self.windows.get_height() * 0.1,
                                   text="login",
                                   windows=self.windows, color=(29, 185, 84), func=Page.switch,
                                   args=("login", windows, client, self),
                                   page=self, y=self.windows.get_height() * 0.25)
        self.login_button.center_x()

        self.signup_button = Button(width=self.windows.get_width() * 0.5, height=self.windows.get_height() * 0.1,
                                    text="register",
                                    windows=self.windows, color=(29, 185, 84),
                                    y=self.login_button.rect.y + self.login_button.rect.height * 1.1, func=Page.switch,
                                    args=("signup", windows, client, self),
                                    page=self)
        self.signup_button.center_x()

        self.image = Image(load="resources/spotify.png",
                           y=(self.signup_button.rect.y + self.signup_button.rect.height) * 1.1,
                           width=self.windows.get_width() * 0.3, height=(self.windows.get_height() - (
                    self.signup_button.rect.y + self.signup_button.rect.height)) * 0.8, windows=self.windows)
        self.image.center_x()

        self.components.append(self.login_button)
        self.components.append(self.signup_button)
        self.components.append(self.image)
