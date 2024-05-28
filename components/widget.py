class Widget:
    def __init__(self, x, y, width, height, buttons_dicts, page, windows, box=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttons = []
        self.page = page
        self.windows = windows
        self.box = box
        self.create_buttons(buttons_dicts)

    def create_buttons(self, buttons_dict):
        from components.button import Button
        i = 0
        divided_height = self.height / len(buttons_dict)
        for button_dict in buttons_dict:
            button = Button(width=self.width, height=divided_height, x=self.x, y=self.y + i * divided_height,
                            page=self.page, windows=self.windows,
                            text_color=(0, 0, 0), text=button_dict["text"], color=(64, 64, 64),
                            func=button_dict["func"], font_size=12, args=button_dict["args"])
            self.buttons.append(button)
            i += 1

    def make_elements_drawable(self, boolean):
        for button in self.buttons:
            button.drawable = boolean

    def get_added_to_page(self, page):
        for button in self.buttons:
            page.components.append(button)

    def draw(self):
        pass

    def update_vertical_position(self, y):
        self.y = y
        i = 0
        divided_height = self.height / len(self.buttons)
        for button in self.buttons:
            button.rect.y = self.y + i * divided_height
            i += 1
