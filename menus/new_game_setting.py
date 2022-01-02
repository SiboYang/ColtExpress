import sys

import pygame
from pygame.locals import *

import helpers.pygame_textinput as pygame_textinput
from assets.color_constants import DARK_GREEN, WHITE, BLUE
from assets.font_constants import FONT_BOLD
from assets.game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from helpers.menu_helpers import button, draw_rectangle
from menus.informal_menu_interface import InformalMenuInterface


class NewGame(InformalMenuInterface):
    def draw_menu(self):
        pygame.init()
        lobbyname_is_selected = False
        password_is_selected = False
        begin_click = False
        click = False
        public = False
        private = False
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen = pygame.display.get_surface()
        screen.fill(DARK_GREEN)
        my_font = pygame.font.Font(FONT_BOLD, 30)
        lobby_name = my_font.render("Lobby name", True, WHITE)
        lobby_password = my_font.render("Lobby password", True, WHITE)
        lobby_visibility = my_font.render("Lobby visibility", True, WHITE)
        screen.blit(lobby_name, ((SCREEN_WIDTH * 1 / 16),
                                 (SCREEN_HEIGHT * 2 / 12)))
        screen.blit(lobby_password, ((SCREEN_WIDTH * 1 / 16),
                                     (SCREEN_HEIGHT * 4 / 12)))
        screen.blit(lobby_visibility,
                    ((SCREEN_WIDTH * 1 / 16), (SCREEN_HEIGHT * 6 / 12)))
        button("Public", SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 6 / 12, SCREEN_WIDTH * 2 / 12, SCREEN_HEIGHT * 1 / 12,
               public, screen)
        button("Private", SCREEN_WIDTH * 12 / 16, SCREEN_HEIGHT * 6 / 12, SCREEN_WIDTH * 2 / 12, SCREEN_HEIGHT * 1 / 12,
               private, screen)
        # return Waiting()
        # go to the waiting interface
        lobby_name_input = pygame_textinput.TextInput()
        lobby_name_input.max_string_length = 16
        lobby_password_input = pygame_textinput.TextInput()
        lobby_password_input.max_string_length = 16
        lobby_password_input.password = True
        while True:
            lobbyname_textbox_rectangle = draw_rectangle(screen, SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 2 / 12,
                                                         5 / 16 * SCREEN_WIDTH,
                                                         1 / 9 * SCREEN_HEIGHT, BLUE)

            lobbypassword_textbox_rectangle = draw_rectangle(screen, SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 4 / 12,
                                                             5 / 16 * SCREEN_WIDTH,
                                                             1 / 9 * SCREEN_HEIGHT, BLUE)
            ev = pygame.event.get()
            for event in ev:
                mouse = pygame.mouse.get_pos()
                if event.type == QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if SCREEN_WIDTH * 3 / 8 < mouse[
                        0] < SCREEN_WIDTH * 3 / 8 + SCREEN_WIDTH * 3 / 12 and SCREEN_HEIGHT * 10 / 12 < mouse[
                        1] < SCREEN_HEIGHT * 10 / 12 + SCREEN_HEIGHT * 1 / 12:
                        begin_click = True
                    else:
                        click = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if lobbyname_textbox_rectangle.collidepoint(event.pos):
                        lobbyname_is_selected = True
                        password_is_selected = False
                    elif lobbypassword_textbox_rectangle.collidepoint(event.pos):
                        lobbyname_is_selected = False
                        password_is_selected = True
                    else:
                        lobbyname_is_selected = False
                        password_is_selected = False
            if lobbyname_is_selected:
                lobby_name_input.update(ev)
            if password_is_selected:
                lobby_password_input.update(ev)
            screen.blit(lobby_name_input.get_surface(),
                        (SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 2 / 12))
            screen.blit(lobby_password_input.get_surface(),
                        (SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 4 / 12))
            if button("Begin", SCREEN_WIDTH * 3 / 8, SCREEN_HEIGHT * 10 / 12, SCREEN_WIDTH * 3 / 12,
                      SCREEN_HEIGHT * 1 / 12,
                      begin_click, screen):
                if lobby_name_input.get_text() == '' or lobby_password_input.get_text() == '' or (
                        public == False and private == False):
                    print('Please fill all the blank!')
                    begin_click = False
                else:
                    # TODO: Send lobby_name,lobby_password,lobby_type to the server
                    # TODO: Receive the response from server and update the interface to character selection menu
                    print(lobby_name_input.get_text())
                    print(lobby_password_input.get_text())
                    print(public, private)
            if button("Public", SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 6 / 12, SCREEN_WIDTH * 2 / 12,
                      SCREEN_HEIGHT * 1 / 12,
                      click, screen):
                public = True
                private = False
            if button("Private", SCREEN_WIDTH * 12 / 16, SCREEN_HEIGHT * 6 / 12, SCREEN_WIDTH * 2 / 12,
                      SCREEN_HEIGHT * 1 / 12,
                      private, screen):
                private = True
                public = False

            pygame.display.update()


def main():
    NewGame().draw_menu()


if __name__ == '__main__':
    main()
