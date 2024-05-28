from components.image import ImageButton


class CheckBox(ImageButton):
    @staticmethod
    def check(check_box):
        check_box.checked = True
        check_box.func = CheckBox.uncheck
        check_box.update_load(load="resources/checked.png")

    @staticmethod
    def uncheck(check_box):
        check_box.checked = False
        check_box.func = CheckBox.check
        check_box.update_load(load="resources/unchecked.png")

    def __init__(self, width, height, windows, x, y, load="resources/unchecked.png"):
        func = CheckBox.check
        args = (self, )
        super().__init__(load, width, height, windows, x, y, func=func, args=args)
        self.checked = False


