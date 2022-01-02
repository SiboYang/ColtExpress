from menus.informal_menu_interface import InformalMenuInterface
from assets.game_constants import SCREEN_HEIGHT, SCREEN_WIDTH
from helpers.menu_helpers import text_objects, button
from menus.client_info import Client

import pygame

class SettingsMenu(InformalMenuInterface):
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
            click = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    click = True
                if event.type == pygame.QUIT:
                    print("Quit received")
                    exit(0)

            # Save game button
            if button("Save Game", (SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)) / 2, SCREEN_HEIGHT * 0.6, SCREEN_WIDTH * 0.3,
                      SCREEN_HEIGHT * 0.08, click, screen):
                client.save()
            # Exit game button
            if button("Exit Game", (SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)) / 2, SCREEN_HEIGHT * 0.7, SCREEN_WIDTH * 0.3,
                      SCREEN_HEIGHT * 0.08, click, screen):
                client.exit()

            pygame.display.update()



