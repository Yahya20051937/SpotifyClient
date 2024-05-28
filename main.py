import pygame

pygame.font.init()
from entity.client import Client
from pages.home import HomePage
from pages.user.main import MainPageU
from pages.singer.main import MainPageS

WIDTH = 800
HEIGHT = 650
FPS = 240
BACKGROUND = (0, 0, 0)
spotify_image = pygame.image.load("resources/spotify.png")
pygame.display.set_icon(spotify_image)
WINDOWS = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spotify")
client = Client(windows=WINDOWS)
# IF the credentials are not saved within the client's device, we display a page where the user can log in or register
if not client.are_credentials_saved():
    page = HomePage(windows=WINDOWS, client=client, name="home")
else:  # if not, then we update the jwt using  those credentials
    client.update_jwt()
    if client.jwt is not None:
        if client.user.role == "USER":  # if the client is a USER, we send a request to get the playlists of the user and the display the user main page
            page = MainPageU(windows=WINDOWS, client=client, name="mainU")
            client.current_page = page
            client.send_get_playlists_requests()
        else:
            page = MainPageS(windows=WINDOWS, client=client, name="mainS")  # if not we display the singer's main page.
    else:
        page = HomePage(windows=WINDOWS, client=client, name="home")
        print("p")

client.current_page = page
page.run()
