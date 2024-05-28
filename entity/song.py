class Song:
    from components.song_component import SongComponent
    COMPONENT_CLASS = SongComponent

    @staticmethod
    def build(dict_):
        from entity.singer import Singer
        from entity.time import Time
        return Song(id_=dict_["id"], name=dict_["name"], singer=Singer(id_=dict_["singerId"], name=dict_["singerName"],
                                                                       image_bytes=dict_["singer_image_bytes"]),
                    image_bytes=dict_["image_bytes"], time=Time(value=dict_["duration"]), bit_rate=dict_["bitRate"],
                    nb_bytes=dict_["nbBytes"], nb_likes=dict_["nbLikes"], nb_streams=dict_["nbStreams"])

    def __init__(self, id_, name, singer, image_bytes, nb_bytes, bit_rate, time, nb_likes, nb_streams):
        self.id = id_
        self.name = name
        self.singer = singer
        self.image_bytes = image_bytes
        self.time = time
        self.nb_bytes = nb_bytes
        self.bit_rate = bit_rate
        self.streaming = False
        self.nb_likes = nb_likes
        self.nb_streams = nb_streams

    from entity.time import Time

    def get_all_bytes_size(self, starting_time=Time(0)):
        return self.nb_bytes - (starting_time.get_seconds_value() * self.bit_rate) / 8

    def update_nb_likes(self, client):
        self.nb_likes = client.send_get_likes_or_streams_request(song=self, attribute="likes")

    def update_nb_streams(self, client):
        self.nb_streams = client.send_get_likes_or_streams_request(song=self, attribute="streams")
