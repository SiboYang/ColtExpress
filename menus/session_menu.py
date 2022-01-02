import json
import time

import pygame
import requests

import menus.bandit_menu as bandit_menu
import menus.lobby_menu as lobby_menu
from assets.color_constants import *
from assets.font_constants import FONT_BOLD, FONT_REG
from assets.game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from assets.network_constants import *
from helpers.menu_helpers import text_objects, draw_rectangle, button, button_alpha
from menus.client_info import Client
from menus.informal_menu_interface import InformalMenuInterface


# this menu displays the current session. It contains the other players for example, and also
# manages the game's lobby state.
# isHost is checked once near the start of this session, and then we keep that state forever.
class SessionMenu(InformalMenuInterface):

    def __init__(self, session_number):
        self.session_number = session_number
        self.launched = False
        self.session = {}

    # This function pulls session data from the game manager server. If it has launched, it will update the
    # local variable. We can then check for the launch status, and potentially pull the new data from the endpoint?
    def refresh_session(self):
        resp = requests.get(LOBBYURL + "/api/sessions/" + self.session_number)
        if resp.status_code != 200:
            return None
        players = []
        self.session = resp.json()
        for player in resp.json()["players"]:
            players.append(player)
        self.launched = resp.json()["launched"]
        return players

    def draw_menu(self):
        screen = pygame.display.get_surface()
        client = Client.get_instance()
        # Sets background for the screen
        screen.fill((118, 95, 55))
        players = self.refresh_session()

        mover = 0
        # Try and draw a button or something
        # menu = pygame_menu.Menu(height=600, width=800, title="Colt Express",
        #                         columns=2, rows=2, theme=pygame_menu.themes.THEME_DARK)

        # Create variable for refreshing
        refresh_epoch = 0
        while True:
            screen.fill((118, 95, 55))
            # Try adding a button with custom helper
            ev = pygame.event.get()
            click = False

            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    click = True
                if event.type == pygame.QUIT:
                    exit()

            # TODO: Check if we have launched from the server every second somehow? I think we'd initialize the socket connection here...
            # TODO: Check and spam refresh session function here even if button isn't pushed.
            # TODO: We need to figure out how to retrieve the data or something, because of this dumb event loop.
            # TODO: We can check that it is launched, and once it is, we socket connect to the GMServer and wait for the agreed upon payload. Then it draws. in this case
            # TODO: We can potentially make another intermediate menu where it just tells the user to wait... And while this menu is happening, the user must wait for their turn to pick
            if refresh_epoch < time.time():
                players = self.refresh_session()
                refresh_epoch = time.time() + 0.5  # Adds 500ms to next refresh checkpoint
                print("refreshing session")

            # Game has launched, retrieve new server connection information and save that for the duration of the game.
            if self.launched:
                # The game has launched. Call the new endpoint to retrieve ADDRESS and PORT to the game server.
                # requests.get(GAMEMANAGERURL+"/api/startgame/"+self.session_number)
                # TODO: Again, like the one for the host, do we need to send any extra information in this case, or is this
                #   enough? This should return ADDRESS and PORT, and we will be able to set that in client_info for use elsewhere like in BanditMenu.
                # Launched as the host, so retrieve new socket connection:
                # request_return = requests.get(GAMEMANAGERURL + "/api/startgame/" + self.session_number)
                # client.server_ip = str(json.loads(request_return.json())['address'])
                # client.server_port = str(json.loads(request_return.json())['port'])
                client.launch_session()
                # go to bandit menu phase and wait for server to talk to us.
                return bandit_menu.BanditMenu()
            if button_alpha("Refresh", SCREEN_WIDTH * 0.65, SCREEN_HEIGHT * 0.01, SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.15,
                      click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                print("refreshed")
                players = self.refresh_session()
                if self.launched:
                    return bandit_menu.BanditMenu()
            scrollermenu = draw_rectangle(screen, SCREEN_WIDTH * 0.01, SCREEN_HEIGHT * 0.16, SCREEN_WIDTH * 0.98,
                                          SCREEN_HEIGHT * 0.7, (250, 222, 170))

            button("Players", SCREEN_WIDTH * 0.01, SCREEN_HEIGHT * 0.16, SCREEN_WIDTH * 0.98, SCREEN_HEIGHT * 0.1,
                   click,
                   screen, (250, 222, 170), (250, 222, 170), (0, 0, 0))
            for i, player in enumerate(players):
                player_info = "{:d} {:>20} ".format(i, player)
                y = SCREEN_HEIGHT * 0.16 + ((SCREEN_HEIGHT * 0.1) * (i + 1)) + mover
                clicked = button(player_info, SCREEN_WIDTH * 0.01, y, SCREEN_WIDTH * 0.98, SCREEN_HEIGHT * 0.1, click,
                                 screen, (250, 222, 170), (250, 222, 170), (0, 0, 0))

            # This is the part of the code that checks if you are the owner of the lobby. This also gives the player access to the launch session button.
            if self.session["creator"] == client.username:

                if button_alpha("Launch Session", SCREEN_WIDTH * 0.64, SCREEN_HEIGHT * 0.87, SCREEN_WIDTH * 0.35,
                          SCREEN_HEIGHT * 0.13,
                          click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                    print("Join!")
                    url = LOBBYURL + "/api/sessions/" + self.session_number
                    params = (
                        ('access_token', client.access_token),
                    )
                    resp = requests.post(url, params=params)
                    if resp.status_code == 200:
                        print("Launched")
                        # Launched as the host, so retrieve new socket connection:
                        # request_return = requests.get(GAMEMANAGERURL + "/api/startgame/" + self.session_number)
                        # client.server_ip = str(json.loads(request_return.json())['address'])
                        # client.server_port = str(json.loads(request_return.json())['port'])
                        client.launch_session()
                        # client.game_manager_addr
                        # Go to the bandit menu phase and wait for new server to talk to us.
                        return bandit_menu.BanditMenu()
                    else:
                        print(resp.text)
                        text, rectangle = text_objects('Launch Failed.',
                                                       pygame.font.Font(FONT_BOLD, int(25 / 720 * SCREEN_HEIGHT)),
                                                       (255, 0, 0))
                        rectangle.center = (int(SCREEN_WIDTH * 0.4), int(SCREEN_HEIGHT * 0.97))
                        screen.blit(text, rectangle)
                        return bandit_menu.BanditMenu()
            if button_alpha("Back", SCREEN_WIDTH * 0.01, SCREEN_HEIGHT * 0.87, SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.13,
                      click, screen, (153, 130, 51, 20), (153, 130, 51, 128)) and not self.launched:
                if self.session["creator"] == client.username:
                    url = LOBBYURL + "/api/sessions/" + self.session_number
                    params = (
                        ('access_token', client.access_token),
                    )
                    resp = requests.delete(url, params=params)
                    print("Deleted")
                else:
                    url = LOBBYURL + "/api/sessions/" + self.session_number + "/players/" + client.username
                    params = (
                        ('access_token', client.access_token),
                    )
                    resp = requests.delete(url, params=params)
                return lobby_menu.LobbyMenu()

            pygame.display.update()
