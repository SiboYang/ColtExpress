import pygame

from assets.font_constants import FONT_REG
from assets.game_constants import SCREEN_HEIGHT, SCREEN_WIDTH
from helpers.menu_helpers import text_objects, button
from menus import find_game_menu
from menus import session_menu
from menus.client_info import Client
from menus.informal_menu_interface import InformalMenuInterface


class LobbyMenu(InformalMenuInterface):
    def draw_menu(self):

        screen = pygame.display.get_surface()

        background_image = pygame.image.load("assets/gameboard/back-lobby.jpg")
        background_image = pygame.transform.scale(background_image,
                                                  (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background_image, [0, 0])

        header_image = pygame.image.load("assets/gameboard/header.png").convert_alpha()
        screen.blit(header_image, [(SCREEN_WIDTH - 500) / 2, SCREEN_HEIGHT / 20])



        pygame.display.flip()
        client = Client.get_instance()
        while True:
            # Try adding a button with custom helper
            ev = pygame.event.get()
            click = False
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    click = True
                if event.type == pygame.QUIT:
                    print("Quit received")
                    exit(0)

            # NEW GAME
            if button("New Game", (SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)) / 2, SCREEN_HEIGHT * 0.6, SCREEN_WIDTH * 0.3,
                      SCREEN_HEIGHT * 0.08, click, screen, (87, 87, 87), (140, 146, 172)):
                status, response = client.create_session()
                print(response.text)
                if status:
                    print("Game created at " + response.text)
                    return session_menu.SessionMenu(response.text)
            if button("Load Game", (SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)) / 2, SCREEN_HEIGHT * 0.7, SCREEN_WIDTH * 0.3,
                      SCREEN_HEIGHT * 0.08, click, screen, (87, 87, 87), (140, 146, 172)):
                from menus import load_game_menu
                return load_game_menu.LoadGameMenu()
            if button("Join Game", (SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)) / 2, SCREEN_HEIGHT * 0.8, SCREEN_WIDTH * 0.3,
                      SCREEN_HEIGHT * 0.08, click, screen, (87, 87, 87), (140, 146, 172)):
                return find_game_menu.FindGameMenu()
            pygame.display.update()
