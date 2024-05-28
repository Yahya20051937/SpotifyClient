class SearchBar:
    def __init__(self, x, y, width, height, color, text_color, windows, func, page, args=()):
        from components.entry import Entry
        from components.border import VerticalBorder
        from components.button import Button
        self.x = x
        self.y = y
        self.entry = Entry(x=x, y=y, width=0.95 * width, height=height, color=color, text_color=text_color,
                           windows=windows, text="nirvana")
        self.border = VerticalBorder(x=x + 0.95 * width, y=y, width=0.05 * width, height=height, color=text_color,
                                     windows=windows)
        self.button = Button(x=x + 0.953 * width, y=y, width=0.25 * width, height=height, color=color,
                             windows=windows,
                             text="search", text_color=(0, 0, 0), func=func, args=args, page=page)

    def add_components(self, page):
        page.components.append(self.entry)
        page.components.append(self.border)
        page.components.append(self.button)
