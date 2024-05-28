from pages.login import LoginPage


class SignupPage(LoginPage):
    def __init__(self, windows, client, name):
        super().__init__(windows, client, name)
        from components.label import Label
        from components.entry import Entry
        from components.button import Button
        from form.registration import RegistrationForm
        self.form = RegistrationForm()
        self.form.role = "USER"
        self.email_label = Label(x=self.password_label.rect.x, y=self.password_label.rect.y,
                                 width=self.password_label.rect.width, height=self.password_label.rect.height
                                 , windows=self.windows, text="email", color=(29, 185, 84))
        self.email_entry = Entry(x=self.password_entry.rect.x, y=self.password_entry.rect.y,
                                 width=self.password_entry.rect.width, height=self.password_entry.rect.height,
                                 windows=self.windows,
                                 color=self.password_entry.color)

        self.password_label.rect.y = (self.email_label.rect.y + self.email_label.rect.height) * 1.1
        self.password_entry.rect.y = self.password_label.rect.y

        self.image.rect.y = (self.password_label.rect.y + self.password_label.rect.height) * 1.1
        self.submit_button.rect.y = self.windows.get_height() * 0.87

        self.submit_button.func = self.client.send_registration_request
        self.submit_button.args = (self,)

        self.image_path_label = Label(x=(self.image.rect.x + self.image.rect.width) * 1.1,
                                      y=self.windows.get_height() - self.image.rect.height * 0.5,
                                      width=self.password_label.rect.width * 0.8,
                                      height=self.password_label.rect.height, windows=windows, text_color=(0, 0, 0),
                                      color=self.username_label.color, text="image path")
        self.image_path_entry = Entry(x=(self.image_path_label.rect.x + self.image_path_label.rect.width) * 1.1,
                                      y=self.image_path_label.rect.y,
                                      width=self.image_path_label.rect.width, height=self.image_path_label.rect.height,
                                      color=
                                      self.image_path_label.color, text_color=self.image_path_label.text_color,
                                      windows=windows)
        self.response_label.rect.x = self.image.rect.x + self.image.rect.width
        self.response_label.rect.y = self.submit_button.rect.y * 1.1
        self.response_label.rect.width = self.windows.get_width() * 0.35

        self.components.append(self.email_label)
        self.components.append(self.email_entry)
        self.components.append(self.image_path_label)
        self.components.append(self.image_path_entry)

        self.save_credentials_label.drawable = False
        self.save_credentials_checkbox.drawable = False
        self.image_path_label.drawable = False
        self.image_path_entry.drawable = False

        self.user_role_button = Button(y=self.image.rect.y, width=self.submit_button.rect.width,
                                       height=self.submit_button.rect.height, color=(29, 185, 84),
                                       page=self, text="USER", args=("USER",), func=self.update_role,
                                       windows=self.windows)
        self.user_role_button.center_x()
        self.singer_role_button = Button(x=(self.user_role_button.rect.x + self.user_role_button.rect.width),
                                         y=self.user_role_button.rect.y,
                                         width=self.user_role_button.rect.width,
                                         height=self.user_role_button.rect.height, color=(211, 211, 211),
                                         func=self.update_role, page=self, text="SINGER", args=("SINGER",),
                                         windows=self.windows)

        self.components.append(self.user_role_button)
        self.components.append(self.singer_role_button)

    def build_form(self):
        self.form.build(page=self)

    def update_role(self, new_role):
        if new_role != self.form.role:
            if new_role == "USER":
                self.user_role_button.color = (29, 185, 84)
                self.singer_role_button.color = (211, 211, 211)
                self.image_path_label.drawable = False
                self.image_path_entry.drawable = False
            else:
                self.singer_role_button.color = (29, 185, 84)
                self.user_role_button.color = (211, 211, 211)
                self.image_path_entry.drawable = True
                self.image_path_label.drawable = True
                self.image_path_entry.text = "C:/images/"
            self.form.role = new_role
