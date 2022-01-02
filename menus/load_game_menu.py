# import pygame
import json

import requests

from assets.network_constants import *
from helpers.menu_helpers import *
from menus.client_info import Client
from menus.find_game_menu import FindGameMenu
from menus.lobby_menu import LobbyMenu
from menus.session_menu import SessionMenu


class LoadGameMenu(FindGameMenu):
    @staticmethod
    def refresh_saves(client):
        url = LOBBYURL + "/api/gameservices/ColtExpress/savegames"
        params = {("access_token", client.access_token)}
        response = requests.get(url=url, params=params)
        saves = []
        save_list = response.json()
        for save in save_list:
            if client.username in save['players']:
                saves.append(save)
        return saves

    def draw_menu(self):
        screen = pygame.display.get_surface()
        client = Client.get_instance()
        # Sets background for the screen
        screen.fill((118, 95, 55))
        sessions = FindGameMenu.refresh_sessions()
        saves = self.refresh_saves(client)

        session_selected = False
        session_live = False
        save_index = -1
        mover = 0

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
            if button_alpha("Refresh", SCREEN_WIDTH * 0.65, SCREEN_HEIGHT * 0.01, SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.15,
                      click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                print("refreshed")
                sessions = FindGameMenu.refresh_sessions()
                saves = self.refresh_saves(client)

            top_info = "{} {:>40} {:>30}".format("Number", "Save ID", "Created")
            button(top_info, SCREEN_WIDTH * 0.01, SCREEN_HEIGHT * 0.16, SCREEN_WIDTH * 0.98, SCREEN_HEIGHT * 0.1, click,
                   screen, (250, 222, 170), (250, 222, 170), (0, 0, 0))

            created_saves = [x for x in saves for s in sessions if s['savegameid'] == x['savegameid']]
            #saves.append({'savegameid'})
            for i, save in enumerate(saves):
                created = save in created_saves
                save_info = "{:d} {:>40} {:>30}".format(i, save['savegameid'], str(True))
                y = SCREEN_HEIGHT * 0.16 + ((SCREEN_HEIGHT * 0.1) * (i + 1)) + mover
                clicked = button(save_info, SCREEN_WIDTH * 0.01, y, SCREEN_WIDTH * 0.98, SCREEN_HEIGHT * 0.1, click,
                                 screen, (255, 255, 255), LIGHT_BLUE, (0, 0, 0))
                session_selected = session_selected or clicked
                if clicked:
                    save_index = i
                    session_live = created

            if session_selected:
                if button("Load Session", SCREEN_WIDTH * 0.55, SCREEN_HEIGHT * 0.87, SCREEN_WIDTH * 0.35,
                          SCREEN_HEIGHT * 0.13,
                          click, screen):
                    if session_live:
                        it = filter(lambda x: x['savegameid'] == saves[save_index]['savegameid'], sessions)
                        try:
                            live_session = next(it)
                            resp = client.join_session(live_session)
                            if resp.status_code == 200:
                                return SessionMenu(str(live_session["session"]))
                            elif resp.text == "Session can not be joined. Player is already registered for this session.":
                                return SessionMenu(str(live_session["session"]))
                            else:
                                print(resp.text)
                                text, rectangle = text_objects('Join Failed.',
                                                               pygame.font.Font(FONT_BOLD,
                                                                                int(25 / 720 * SCREEN_HEIGHT)),
                                                               (255, 0, 0))
                                rectangle.center = (int(SCREEN_WIDTH * 0.4), int(SCREEN_HEIGHT * 0.97))
                                screen.blit(text, rectangle)
                        except StopIteration:
                            status, response = client.create_session(saveid=saves[save_index]['savegameid'])
                            if status:
                                return SessionMenu(response.text)
                    else:
                        status, response = client.create_session(saveid=saves[save_index]['savegameid'])
                        if status:
                            return SessionMenu(response.text)

            if button_alpha("Back", SCREEN_WIDTH * 0.01, SCREEN_HEIGHT * 0.87, SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.13,
                      click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                return LobbyMenu()
            pygame.display.update()