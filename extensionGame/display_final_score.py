import sys

import pygame

from assets.color_constants import BLACK
from assets.font_constants import FONT_REG, FONT_BOLD
from assets.game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from assets.media_constants import BACKGROUND
from helpers.menu_helpers import button
from menus.client_info import username
from menus.informal_menu_interface import InformalMenuInterface


class FinalScore(InformalMenuInterface):
    def __init__(self, score):
        self.score = score

    def draw_menu(self):
        game_display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        background_img = pygame.image.load(BACKGROUND).convert()
        background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        game_display.blit(background_img, (0, 0))

        # display final score
        counter = 0
        for key, val in self.score:
            font = None
            if key != username:
                font = pygame.font.Font(FONT_REG, 20)
            else:
                font = pygame.font.Font(FONT_BOLD, 20)
            text = font.render("score of " + key + " : " + str(val), True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = ((SCREEN_WIDTH * 0.5), (SCREEN_HEIGHT * (0.2 + 0.1 * counter)))
            game_display.blit(text, text_rect)
            counter += 1

        while True:
            ev = pygame.event.get()
            click = False
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    click = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if button("Find Game", SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.8,
                      SCREEN_WIDTH * 0.2,
                      SCREEN_HEIGHT * 0.08, click, game_display):
                # do something here
                from menus.find_game_menu import FindGameMenu
                return FindGameMenu()
            elif button("Log out", SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.8,
                        SCREEN_WIDTH * 0.2,
                        SCREEN_HEIGHT * 0.08, click, game_display):
                # do something here
                from menus.login_menu import LoginMenu
                return LoginMenu()

            pygame.display.update()
