class Stream:
    def __init__(self, audio, starting_time):
        self.audio = audio
        self.starting_time = starting_time
        self.streaming = False
        self.paused = False
