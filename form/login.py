class LoginForm:
    def __init__(self):
        self.username = None
        self.password = None

    def build(self, page):
        self.username = page.user_name_entry.text
        self.password = page.password_entry.text
