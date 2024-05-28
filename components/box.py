class Box:
    def __init__(self, x, y, width, height, page, windows, border_color=(0, 0, 0), font_size=24, color=(29, 185, 84),
                 max_size=5, head_width_percentage=0.03, head_color=(29, 185, 84)):
        from components.scroll_bar import ScrollBar
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.border_color = border_color
        self.windows = windows
        self.page = page
        self.max_size = max_size
        self.scroll_bar = ScrollBar(x=self.x + self.width * 0.955,
                                    y=self.y, width=self.width * head_width_percentage,
                                    height=self.height * 1.03, color=(185, 185, 185), page=page, head_color=head_color)
        self.page.components.append(self.scroll_bar)
        self.components = []
        self.font_size = font_size
        self.active_widget = None
        self.default_y_coordinate_dict = dict()

    def add_component(self, spotify_object, cls=None, args=()):
        from components.song_component import SongComponent
        if cls is None:
            cls = spotify_object.__class__.COMPONENT_CLASS  # for the sub playlist component, there are two arguments func and args=(song, playlist, add_or_remove)

        component = cls(*args, spotify_object=spotify_object, x=self.x, box_y=self.y,
                        width=self.width * 0.955,
                        height=self.height / self.max_size, windows=self.windows,
                        client=self.page.client, index=len(self.components),
                        box_height=self.height, font_size=self.font_size,
                        color=self.color)
        self.default_y_coordinate_dict[component.spotify_object.id] = component.y
        if component.__class__ == SongComponent:
            component.get_updated()  # this to update the number of streams and likes while showing the component
        if len(self.components) >= self.max_size:
            component.make_elements_drawable(False)
            self.scroll_bar.drawable = True
        else:
            self.scroll_bar.drawable = False

        self.components.append(component)
        component.get_added_to_page(page=self.page)

    def update(self):
        """
        Here, we check if the sroll bar head position is updated, if so we calculate the percentage of the y variation, and that given that percentage, we will determine the first component
        that will be shown in the box.

        :return:
        """
        self.update_active_widget()
        self.update_positions()
        for component in self.components:
            component.update()

    def update_positions(self):
        from components.functions import get_element_from_list_by_percentage, get_element_index_in_a_list
        self.scroll_bar.scroll_head.update_vertical_position()
        if self.scroll_bar.scroll_head.position_updated:
            first_component = get_element_from_list_by_percentage(list_=self.components,
                                                                  percentage=self.scroll_bar.scroll_head.get_y_variation_percentage())
            component_list_index = get_element_index_in_a_list(self.components, first_component)
            for i in range(0, component_list_index):
                self.components[i].index = i - component_list_index
            index = 0
            for j in range(component_list_index, len(self.components)):
                self.components[j].index = index
                index += 1
            for component in self.components:
                component.update_vertical_position(y=(self.y + component.index * (self.height / self.max_size)) * 1.005)

            self.scroll_bar.scroll_head.position_updated = False

    def update_active_widget(self):
        for component in self.components:
            if component.widget != self.active_widget:
                if component.widget_activated:
                    component.deactivate_widget()
                    component.widget_activated = False
            else:
                if not component.widget_activated:
                    component.activate_widget()
                    component.widget_activated = True

    def clear(self):
        for component in self.components:
            component.deactivate_widget()
            for sub_component in component.sub_components:
                sub_component.drawable = False
                try:
                    sub_component.clickable_while_not_drawable = False
                except AttributeError:
                    pass
        self.components = []

    def update_vertical_position(self, y):
        self.y = y
        for component in self.components:
            component.update_vertical_position(y=(self.y + component.index * (self.height / self.max_size)) * 1.005)
        self.scroll_bar.rect.y = y
        self.scroll_bar.scroll_head.rect.y = y

    def set_active_widget(self, widget):
        self.active_widget = widget

    def update_components(self):
        from components.song_component import SongComponent
        for component in self.components:
            if component.__class__ == SongComponent:
                component.get_updated()
