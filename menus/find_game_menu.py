import menus.session_menu as session_menu
import pygame
import requests
from assets.color_constants import *
from assets.network_constants import LOBBYURL
from helpers.menu_helpers import (text_objects, button, button_alpha, draw_rectangle, DARK_GREEN, SCREEN_HEIGHT,
                                  SCREEN_WIDTH, FONT_BOLD, FONT_REG)
from menus import lobby_menu
from menus.client_info import Client
from menus.informal_menu_interface import InformalMenuInterface


class FindGameMenu(InformalMenuInterface):

    # @staticmethod
    # def __login():
    #     print("Login button pressed")
    # Pings lobby service to find available sessions and returns list of session dictionaries
    @staticmethod
    def refresh_sessions():
        resp = requests.get(LOBBYURL + "/api/sessions")
        sessions = []
        try:
            for session, data in resp.json()["sessions"].items():
                if not data["launched"]:
                    cur = {"session": session,
                           "creator": data["creator"],
                           "numberofplayers": len(data["players"]),
                           "launched": data["launched"],
                           "savegameid": data["savegameid"]}
                    sessions.append(cur)
        except KeyError: # Sometimes we fail to grab a session for some reason (endpoint glitch?) so we try again.
            return FindGameMenu.refresh_sessions() # ... via recursion.
        return sessions # Otherwise, return the updated session list.

    def draw_menu(self):
        screen = pygame.display.get_surface()
        client = Client.get_instance()

        session_selected = False
        session_number = -1
        mover = 0
        # Try and draw a button or something
        # menu = pygame_menu.Menu(height=600, width=800, title="Colt Express",
        #                         columns=2, rows=2, theme=pygame_menu.themes.THEME_DARK)
        refresh_game = 0
        while True:
            # Sets background for the screen
            screen.fill((118, 95, 55))
            sessions = self.refresh_sessions()



            if refresh_game < pygame.time.get_ticks():
                refresh_game = pygame.time.get_ticks() + 5000
                self.refresh_sessions()

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
                sessions = self.refresh_sessions()
            scrollermenu = draw_rectangle(screen, SCREEN_WIDTH * 0.01, SCREEN_HEIGHT * 0.16, SCREEN_WIDTH * 0.98,
                                          SCREEN_HEIGHT * 0.7, (250, 222, 170))
            top_info = "{} {:>20} {:>20} {:>10} {:>10}".format("Number", "Creator", "Number of players"
                                                               , "Save ID", str("Launched"))
            button(top_info, SCREEN_WIDTH * 0.01, SCREEN_HEIGHT * 0.16, SCREEN_WIDTH * 0.98, SCREEN_HEIGHT * 0.1, click,
                   screen, (250, 222, 170), (250, 222, 170), (0, 0, 0))
            for i, session in enumerate(sessions):
                session_info = "{:d} {:>20} {:>20d} {:>20} {:>20}".format(i, session["creator"],
                                                                          session["numberofplayers"],
                                                                          str(session['savegameid']),
                                                                          str(session["launched"]))
                y = SCREEN_HEIGHT * 0.16 + ((SCREEN_HEIGHT * 0.1) * (i + 1)) + mover
                clicked = button(session_info, SCREEN_WIDTH * 0.01, y, SCREEN_WIDTH * 0.98, SCREEN_HEIGHT * 0.1, click,
                                 screen, (250, 222, 170), LIGHT_BLUE, (0, 0, 0))
                session_selected = clicked or session_selected
                if clicked:
                    session_number = i
            if session_selected:
                # we will attempt to join the session
                if button_alpha("Join Session", SCREEN_WIDTH * 0.64, SCREEN_HEIGHT * 0.87, SCREEN_WIDTH * 0.35,
                          SCREEN_HEIGHT * 0.13,
                          click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                    print("Join!")
                    resp = client.join_session(sessions[session_number])
                    '''url = LOBBYURL + "/api/sessions/" + str(sessions[session_number]["session"]) + "/players/" + client.username
                    params = (
                        ('access_token', client.access_token),
                    )
                    resp = requests.put(url, params=params)'''
                    if resp.status_code == 200:
                        return session_menu.SessionMenu(str(sessions[session_number]["session"]))
                    elif resp.text == "Session can not be joined. Player is already registered for this session.":
                        return session_menu.SessionMenu(str(sessions[session_number]["session"]))
                    else:
                        print(resp.text)
                        text, rectangle = text_objects('Join Failed.',
                                                       pygame.font.Font(FONT_BOLD, int(25 / 720 * SCREEN_HEIGHT)),
                                                       (255, 0, 0))
                        rectangle.center = (int(SCREEN_WIDTH * 0.4), int(SCREEN_HEIGHT * 0.97))
                        screen.blit(text, rectangle)
            if button_alpha("Back", SCREEN_WIDTH * 0.01, SCREEN_HEIGHT * 0.87, SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.13,
                      click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                return lobby_menu.LobbyMenu()
            # # Add some vertical margins in px. (So add something to adjust this based on current screen size)
            # menu.add_vertical_margin(210)
            # menu.add_button("Login", self.__login)
            # menu.add_vertical_margin(210)
            # menu.add_button("SUCC", None)
            # menu.mainloop(screen)  # this can be replaced for a more manual event loop

            pygame.display.update()
