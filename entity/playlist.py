class Playlist:
    from components.playlist_component import PlaylistComponent, SubPlaylistComponent
    COMPONENT_CLASS = PlaylistComponent
    SUBCOMPONENT_CLASS = SubPlaylistComponent

    def __init__(self, id_, name, songs):
        self.id = id_
        self.name = name
        self.songs = songs

    def add_song(self, song):
        self.songs.append(song)

    def remove_song(self, song):
        i = 0
        for audio in self.songs:
            if audio.id == song.id:
                self.songs = self.songs[:i] + self.songs[i + 1:]
            i += 1
