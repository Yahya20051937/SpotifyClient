import base64
import json

from mutagen.wave import WAVE


class UploadSongForm:
    def __init__(self):
        self.name = None
        self.audio_path = None
        self.image_path = None

    def build(self, page):
        self.name = page.song_name_entry.text
        self.audio_path = page.audio_path_entry.text
        self.image_path = page.image_path_entry.text

    @property
    def dict(self):
        return {"name": self.name,
                "duration": int(self.audio_duration), "bitRate": int(self.audio_bit_rate)}

    @property
    def json(self):
        return {"name": self.name, "audioFileBase64": self.audio_file_base64, "imageFileBase64": self.image_file_base64,
                "duration": int(self.audio_duration), "bitRate": int(self.audio_bit_rate)}

    @property
    def audio_file_base64(self):
        return base64.b64encode(open(f"{self.audio_path}", "rb").read()).decode("utf-8")

    @property
    def image_file_base64(self):
        return base64.b64encode(open(f"{self.image_path}", "rb").read()).decode("utf-8")

    @property
    def audio_duration(self):
        return WAVE(open(self.audio_path).name).info.length

    @property
    def audio_bit_rate(self):
        return WAVE(open(self.audio_path).name).info.bitrate
