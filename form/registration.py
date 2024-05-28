import base64

from form.login import LoginForm


class RegistrationForm(LoginForm):
    def __init__(self):
        super().__init__()
        self.email = None
        self.role = None
        self.imageBytesBase64 = None

    def build(self, page):
        self.username = page.username_entry.text
        self.email = page.email_entry.text
        self.password = page.password_entry.text
        if self.role == "SINGER":
            self.imageBytesBase64 = base64.b64encode(open(page.image_path_entry.text, "rb").read()).decode("utf-8")




