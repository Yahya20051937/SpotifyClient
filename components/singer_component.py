import base64
import io


class SingerComponent:
    def __init__(self, spotify_object, x, box_y, box_height, width, height, windows, client, index, font_size, color):
        from components.image import Image
        from components.label import Label
        self.index = index
        self.box_y = box_y
        self.box_height = box_height
        self.x = x
        self.y = (box_y + self.index * height) * 1.005
        self.width = width
        self.height = height
        self.windows = windows
        self.client = client
        self.spotify_object = spotify_object
        self.font_size = font_size
        self.color = color
        try:  # for the playlist object, the spotify object will not have an image bytes attribute
            load = io.BytesIO(base64.b64decode(spotify_object.image_bytes))
        except (TypeError, AttributeError):
            load = "resources/spotify.png"

        self.image = Image(load=load,
                           width=0.2 * self.width,
                           height=self.height, windows=self.windows,
                           y=self.y + self.height * 0.1, x=self.x)

        self.label = Label(width=self.width, height=self.height, x=self.x,
                           y=self.y + 0.1 * self.height, windows=windows, text=self.spotify_object.name,
                           color=self.color, font_size=font_size)
        self.sub_label = Label(width=0.15 * self.width, height=0.05 * self.height, x=self.x + 0.22 * self.width,
                               y=self.y + self.height * 0.9, text="artist", windows=windows,
                               color=self.label.color, font_size=16)
        self.sub_components = [self.label, self.sub_label, self.image]
        self.widget = None
        self.widget_activated = False

    def get_added_to_page(self, page):
        for component in self.sub_components:
            if component is not None:
                page.components.append(component)

    def make_elements_drawable(self, boolean):
        for component in self.sub_components:
            component.drawable = boolean

    def update_vertical_position(self, y):
        self.y = y
        self.image.rect.y = self.y + self.height * 0.1
        self.label.rect.y = self.y + 0.1 * self.height
        self.sub_label.rect.y = self.y + self.height * 0.9

        if self.y < self.box_y or self.y > self.box_y + self.box_height:
            self.make_elements_drawable(False)
        else:
            self.make_elements_drawable(True)

    def deactivate_widget(self):
        pass

    def activate_widget(self):
        pass

    def update_like_button(self, client):
        pass

    def update(self):
        pass
