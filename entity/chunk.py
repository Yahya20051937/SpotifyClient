import base64
import binascii

from pydub import AudioSegment


class Chunk:
    def __init__(self, base64_bytes, volume_padding=0):
        try:
            self.decoded_bytes = base64.b64decode(base64_bytes)
            self.audio_segment = AudioSegment(self.decoded_bytes, frame_rate=96000, channels=1, sample_width=2) + volume_padding
            self.bytes = self.audio_segment.raw_data
            self.size = len(self.bytes)
            self.correct = True
        except binascii.Error:
            self.correct = False

    def mute(self):
        if self.correct:
            self.bytes = bytes([0 for i in range(len([b for b in self.bytes]))])
