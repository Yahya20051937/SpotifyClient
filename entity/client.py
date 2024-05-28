import base64
import json
import threading
from collections import deque

import urllib3.exceptions
from mutagen.wave import WAVE
import pyaudio
import requests


def remove_element_from_list_by_id(list_, id_):
    i = 0
    for element in list_:
        if element.id == id_:
            del list_[i]
        i += 1


def get_spotify_objects_from_json_list(json_list, closing_border="}"):
    from entity.song import Song
    from entity.singer import Singer
    spotify_objects = []
    json_objects = json_list.decode("utf-8")[1:-1].split(closing_border)
    for json_object in json_objects[:-1]:
        if "," == json_object[0]:
            json_object = json_object[1:]
        json_object += closing_border
        if closing_border != "}":
            json_object = json_object.replace(")", "}")
            json_object = json_object.replace("(", "{")
        dict_object = json.loads(json_object)
        if dict_object["type"] == "song":
            song = Song.build(dict_object)
            spotify_objects.append(song)
        elif dict_object["type"] == "singer":
            singer = Singer.build(dict_object)
            spotify_objects.append(singer)
    return spotify_objects


def get_playlists_from_json_array(json_array):
    from entity.playlist import Playlist
    playlists = []
    playlists_json = json_array.decode("utf-8")[1:-1].split("}")
    for playlist_json in playlists_json[:-1]:
        if "," == playlist_json[0]:
            playlist_json = playlist_json[1:]
        playlist_json += "}"
        dict_object = json.loads(playlist_json)
        songs = get_spotify_objects_from_json_list(dict_object["songs"].encode("utf-8"), closing_border=")")
        playlists.append(Playlist(id_=dict_object["id"], name=dict_object["name"], songs=songs))
    return playlists


class Client:
    BASE_URL = "http://localhost:9090/spotify/api"
    INCREMENT_DECREMENT_DICT = {"add": "increment", "remove": "decrement"}
    METHODS_DICT = {"get": requests.get, "post": requests.post, "delete": requests.delete, "put": requests.put}

    def __init__(self, windows):
        self.windows = windows
        self.jwt = None
        self.user = None
        self.current_page = None
        self.previous_page = None
        self.volume_padding = 0
        self.current_stream = None
        self.stream_active = False
        self.streaming = False
        self.stream_paused = False
        self.mute = False
        self.playlists = []
        self.liked_songs_playlist = None
        self.current_mode = "search"  # for now, there is the search mode, and the playlist mode
        self.current_playlist = None
        self.current_response = None
        self.streaming_chunks = deque()
        self.streaming_queue = deque()
        self.waiting = False
        p = pyaudio.PyAudio()
        self.streaming_channel = p.open(format=pyaudio.paInt16, channels=1, rate=96000, output=True)

    def send_request(self, method, uri, data=None, json_=None, headers=None, files=None):
        self.waiting = True
        response_dict = dict()
        thread = threading.Thread(target=self.get_response,
                                  args=(method, uri, data, json_, headers, files, response_dict))

        thread.start()
        thread.join()
        return response_dict["response"]

    def get_response(self, method, uri, data, json_, headers, files, response_dict):
        from entity.response import Response
        try:
            response = method(uri, data=data, json=json_, headers=headers, files=files)
            self.waiting = False
            response_dict["response"] = response
        except Exception\
                :
            print("Exception")
            response_dict["response"] = Response(500)

    def send_registration_request(self, page):
        page.response_label.drawable = True
        from entity.jwt import JWT
        try:
            self.current_page.build_form()
        except FileNotFoundError or PermissionError:
            page.response_label.text = "File not Found"
        else:
            response = self.send_request(method=requests.post, json_=page.form.__dict__,
                                         uri=Client.BASE_URL + "/register",
                                         )

            if response.status_code == 500 or response.status_code == 503:
                page.response_label.text = "Please try again later"

            elif response.status_code == 200:
                self.jwt = JWT(response.content)
                page.response_label.text = "Account Created successfully"
                self.post_authentication_process(page)
            else:
                page.response_label.text = response.content.decode("utf-8")

    def send_authentication_request(self, page):
        from entity.jwt import JWT
        page.build_form()
        response = self.send_request(method=requests.post, uri=Client.BASE_URL + "/authenticate",
                                     json_=page.form.__dict__)
        page.response_label.drawable = True
        if response.status_code == 500 or response.status_code == 503:
            page.response_label.text = "Please try again later"

        elif response.status_code == 200:
            page.response_label.text = "Welcome back"
            self.jwt = JWT(response.content)
            self.post_authentication_process(page)
        else:
            page.response_label.text = response.content.decode("utf-8")

    def post_authentication_process(self, page):
        from pages.page import Page
        from entity.user import User
        self.user = User(username=page.form.username, password=page.form.password, role=self.jwt.scope)
        if page.save_credentials_checkbox.checked:
            self.user.save_credentials()
        if self.jwt.scope == "SINGER":
            name = "main_singer"
        else:
            name = "main_user"
            self.send_get_playlists_requests()
        Page.switch(client=self, name=name, current_page=page, windows=page.windows)

    def update_jwt(self):
        from entity.jwt import JWT
        from pages.page import Page
        response = self.send_request(method=requests.post, uri=Client.BASE_URL + "/authenticate",
                                     json_=self.user.credentials_dict)
        if response.status_code == 200:
            self.jwt = JWT(response.content)

        else:
            Page.switch(client=self, name="home", current_page=self.current_page, windows=self.windows)

    def send_get_playlists_requests(self):
        auth = {"Authorization": self.jwt.token_type + " " + self.jwt.access_token}
        response = self.send_request(method=requests.get, uri=Client.BASE_URL + "/playlists/get", headers=auth)
        if response.status_code != 401:
            if self.user.role == "USER":
                self.playlists = get_playlists_from_json_array(response.content)
                try:
                    self.liked_songs_playlist = [p for p in self.playlists if p.name == "Liked Songs"][0]
                except IndexError:
                    self.send_create_playlist_request("Liked Songs")
        else:
            self.update_jwt()
            self.send_get_playlists_requests()

    def send_upload_request(self, page):
        try:
            self.current_page.form.build(page=self.current_page)
            auth = {"Authorization": self.jwt.token_type + " " + self.jwt.access_token}
            files = {"audio": open(self.current_page.form.audio_path, "rb"),
                     "image": open(self.current_page.form.image_path, "rb")}
            print(self.current_page.form.dict)
            response = self.send_request(method=requests.post, data=self.current_page.form.dict,
                                         headers=auth, uri=Client.BASE_URL + "/upload/song", files=files,
                                         )

            status_code = response.status_code
            if status_code == 200:
                page.response_label.text = "Song uploaded successfully"
            else:
                page.response_label.text = "Please try again later."

        except FileNotFoundError:
            page.response_label.text = "File not found !!"

    def send_search_request(self):
        auth = {"Authorization": self.jwt.token_type + " " + self.jwt.access_token}
        response = self.send_request(method=requests.get,
                                     uri=Client.BASE_URL + "/search/" + self.current_page.search_bar.entry.text,
                                     headers=auth)
        print("search response , ", response.status_code)
        if response.status_code != 401:
            self.current_page.box.clear()
            spotify_objects = get_spotify_objects_from_json_list(response.content)
            for spotify_object in spotify_objects:
                self.current_page.box.add_component(spotify_object=spotify_object)
            self.current_mode = "search"
            self.current_playlist = None
        else:
            self.update_jwt()
            self.send_search_request()

    def send_add_remove_song_to_playlist_request(self, song, playlist, add_or_remove='add'):
        if add_or_remove == "add":
            playlist.songs.append(song)
        else:
            remove_element_from_list_by_id(playlist.songs, song.id)
        auth = {"Authorization": self.jwt.token_type + " " + self.jwt.access_token}
        response = self.send_request(method=requests.post, uri=Client.BASE_URL + "/playlists/" + add_or_remove,
                                     headers=auth,
                                     json_={"playlistId": playlist.id, "songId": song.id})
        if response.status_code != 401:
            if self.current_mode == "playlist" and self.current_playlist.id == playlist.id:
                self.current_page.box.clear()  # this code is to update the remove or add the song in the playlist as soon as the user makes the change, when the mode is 'playlist' and the current playlist is the same playlist that we modified
                for song in playlist.songs:
                    self.current_page.box.add_component(song)
            if playlist.name == "Liked Songs":  # if the change is made in the liked songs playlist, this code update the like button as soon as the change is made
                for component in self.current_page.box.components:
                    component.update_like_button(
                        client=self)  # we send a method to decrement or increment the number of likes in the server
                self.send_increment_or_decrement_likes_or_streams_request(
                    method=Client.INCREMENT_DECREMENT_DICT[add_or_remove], attribute="likes", song=song)
        else:
            self.update_jwt()
            self.send_add_remove_song_to_playlist_request(song, playlist, add_or_remove)

    def update(self):
        if not self.streaming and self.stream_active:
            try:
                next_stream = self.streaming_queue.popleft()
                self.start_streaming_thread(next_stream)
            except IndexError:
                pass

    def start_streaming_thread(self, stream):
        from entity.time import Time
        if self.current_stream is not None:
            self.current_stream.streaming = False
            self.streaming_chunks = deque()

        self.current_page.media_player.activate(song=stream.audio, starting_time=Time(stream.starting_time))
        self.stream_paused = False
        self.current_page.media_player.play()
        self.streaming = True
        self.current_stream = stream
        self.current_stream.streaming = True
        thread = threading.Thread(target=self.stream, args=(self.current_stream,))
        thread.start()

    def stream(self, current_stream):
        from entity.chunk import Chunk
        auth = {"Authorization": self.jwt.token_type + " " + self.jwt.access_token}
        try:
            connection = requests.get(
                "http://localhost:9090/spotify/api/stream/" + current_stream.audio.id + "/" + str(
                    current_stream.starting_time),
                stream=True, headers=auth)
        except requests.exceptions.ConnectionError:
            self.stream(current_stream)
            return
        if connection.status_code != 401:
            self.send_increment_or_decrement_likes_or_streams_request(song=current_stream.audio, method="increment",
                                                                      attribute="streams")
            self.streaming_channel.start_stream()

            for chunk in connection.iter_content(64):
                if not current_stream.streaming or not self.streaming or not self.stream_active:
                    return
                decoded_chunk = chunk.decode("utf-8")
                if len(decoded_chunk) == 64:
                    bytes_chunk = Chunk(decoded_chunk, volume_padding=self.volume_padding)
                    self.streaming_chunks.append(bytes_chunk)
                    if not self.stream_paused:
                        self.stream_next_chunk()

            while len(self.streaming_chunks) > 0 and current_stream.streaming and self.streaming and self.stream_active:
                if not self.stream_paused:
                    self.stream_next_chunk()
            self.streaming = False
            self.streaming_channel.stop_stream()
        else:
            self.update_jwt()
            self.stream(current_stream)

    def stream_next_chunk(self):
        chunk = self.streaming_chunks.popleft()
        if self.mute:
            chunk.mute()
        if chunk.correct:
            self.streaming_channel.write(chunk.bytes)
            self.current_page.media_player.streamed_bytes += chunk.size

    def is_song_liked(self, song):
        if self.liked_songs_playlist is not None:
            for audio in self.liked_songs_playlist.songs:
                if audio.id == song.id:
                    return True
            return False

    def find_playlist_by_id(self, id_):
        for playlist in self.playlists:
            if playlist.id == id_:
                return playlist

    def are_credentials_saved(self):
        from entity.user import User
        with open("files/user_credentials.json", "r") as file:
            credentials = json.load(file)
            if not credentials["saved"] is True:
                return False
            else:
                self.user = User(username=credentials["username"], password=credentials["password"],
                                 role=credentials["role"])
                return True

    def logout(self):
        from entity.user import User
        from pages.page import Page
        self.jwt = None
        self.user = User(username=None, password=None, role=None)
        self.user.save_credentials()
        Page.switch("home", self.windows, self, self.current_page)

    def send_increment_or_decrement_likes_or_streams_request(self, song, method="increment", attribute="likes"):
        auth = {"Authorization": self.jwt.token_type + " " + self.jwt.access_token}
        response = self.send_request(method=requests.post, uri=Client.BASE_URL + f"/metrics/{method}/{attribute}",
                                     data={"id": song.id}, headers=auth)
        if response.status_code != 200:
            self.update_jwt()
            self.send_increment_or_decrement_likes_or_streams_request(song=song, method=method, attribute=attribute)

    def send_get_likes_or_streams_request(self, song, attribute="likes"):
        auth = {"Authorization": self.jwt.token_type + " " + self.jwt.access_token}
        response = self.send_request(method=requests.get, uri=Client.BASE_URL + f"/metrics/get/{attribute}/{song.id}",
                                     headers=auth)
        if response.status_code == 200:
            return json.loads(json.loads(response.content)["entity"])[attribute]
        else:
            self.update_jwt()
            return self.send_get_likes_or_streams_request(song, attribute)

    def send_create_playlist_request(self, name):
        from entity.playlist import Playlist
        auth = {"Authorization": self.jwt.token_type + " " + self.jwt.access_token}
        response = self.send_request(method=requests.post, uri=Client.BASE_URL + "/playlists/create",
                                     json_={"name": name, "username": self.user.username}, headers=auth)
        if response.status_code != 200:
            self.update_jwt()
            self.send_create_playlist_request(name)
        else:
            id_ = response.content
            self.playlists.append(Playlist(id_=id_, name=name, songs=[]))
