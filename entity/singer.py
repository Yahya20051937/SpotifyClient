class Singer:
    from components.singer_component import SingerComponent
    COMPONENT_CLASS = SingerComponent

    @staticmethod
    def build(_dict):
        return Singer(id_=_dict["id"], name=_dict["name"], image_bytes=_dict["singer_image_bytes"])

    def __init__(self, id_, name, image_bytes):
        self.id = id_
        self.name = name
        self.image_bytes = image_bytes
