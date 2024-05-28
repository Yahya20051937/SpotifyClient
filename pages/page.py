import pygame
from collections import deque


class Page:

    @staticmethod
    def switch(name, windows, client, current_page, *args):
        from pages.home import HomePage
        from pages.login import LoginPage
        from pages.signup import SignupPage
        from pages.user.main import MainPageU
        from pages.singer.main import MainPageS
        from pages.singer.upload_single import UploadSinglePage
        pages = {"login": LoginPage, "signup": SignupPage, "main_user": MainPageU, "main_singer": MainPageS,
                 "upload_single": UploadSinglePage, "home": HomePage}
        if current_page is not None:
            current_page.running = False
        client.previous_page = current_page
        new_page = pages[name](windows, client, name, *args)
        client.current_page = new_page
        new_page.run()

    FPS = 60

    def __init__(self, windows, client, name):
        from components.label import Label
        self.windows = windows
        self.client = client
        self.clock = pygame.time.Clock()
        self.components = []
        self.running = False
        self.active_entry = None
        self.active_widget = None
        self.name = name
        self.title = Label(width=self.windows.get_width() * 0.5, height=self.windows.get_height() * 0.05,
                           text="Spotify",
                           windows=self.windows, text_color=(29, 185, 84), y=self.windows.get_height() * 0.05,
                           color=(0, 0, 0), font_size=45)
        self.title.center_x()
        self.components.append(self.title)

    def update(self):
        pass

    def run(self):
        from components.button import Button
        from components.entry import Entry
        from components.image import ImageButton
        from components.check_box import CheckBox

        self.running = True
        while self.running:
            self.clock.tick(Page.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    if self.client.streaming:
                        self.client.streaming_channel.close()
                        self.client.streaming = False
                        self.client.streaming_chunks = deque()

                for component in self.components:
                    if component.__class__ == Button or component.__class__ == ImageButton or component.__class__ == CheckBox:
                        component.handle_event(event=event)
                    elif component.__class__ == Entry:
                        component.handle_event(event=event, page=self)

            self.windows.fill((0, 0, 0))
            for component in self.components:
                component.draw()
            self.update()
            pygame.display.update()

    def remove_component(self, component):
        self.components = [c for c in self.components if c is not component]
