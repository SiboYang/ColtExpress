import pygame

import helpers.pygame_textinput as pygame_textinput
import menus.lobby_menu as lobby_menu
import menus.login_menu as login_menu
from assets.color_constants import DARK_GREEN, LIGHT_BLUE, BLUE
from assets.font_constants import FONT_REG, FONT_LIGHT
from assets.game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from helpers.menu_helpers import text_objects, button, draw_rectangle, button_alpha
from menus.client_info import Client
from menus.informal_menu_interface import InformalMenuInterface


class LoginMenuPrompt(InformalMenuInterface):

    def draw_menu(self):

        def display_background_decorations(screen):
            # Sets background for the screen
            background_image = pygame.image.load("assets/gameboard/coltexpress_keyart_01_1920x1080.jpg")
            background_image = pygame.transform.smoothscale(background_image,
                                                            (int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
            screen.blit(background_image, [0, 0])

        def display_login_area(screen):
            pygame.gfxdraw.box(screen, pygame.Rect(SCREEN_WIDTH * 2 / 16, SCREEN_HEIGHT * 3 / 9, 12 / 16 * SCREEN_WIDTH,
                           5 / 9 * SCREEN_HEIGHT), (87, 87, 87, 225))

        def display_username_text():
            # Username Text
            username_surface, username_dims = text_objects("Username:",
                                                           pygame.font.Font(FONT_LIGHT, int(0.9 / 16 * SCREEN_HEIGHT)), (210, 210, 210))
            username_dims = ((SCREEN_WIDTH * 3 / 16), (SCREEN_HEIGHT * 4 / 9))
            screen.blit(username_surface, username_dims)

        def display_password_text():

            # Password Text
            password_surface, password_dims = text_objects("Password:",
                                                           pygame.font.Font(FONT_LIGHT, int(0.9 / 16 * SCREEN_HEIGHT)), (210, 210, 210))
            password_dims = ((SCREEN_WIDTH * 3 / 16), (SCREEN_HEIGHT * 6 / 9))
            screen.blit(password_surface, password_dims)

        client = Client.get_instance()

        screen = pygame.display.get_surface()

        display_background_decorations(screen)
        # We draw a square for the login screen prompts. Username and Password currently placed below the relative
        # location of the title screen. We will put the username and password text after this.
        # The textbox that will hold the username and password input fields will go into the constant update
        # Because a user will type something, and will need to hit backspace, so we want to redraw every time.
        display_login_area(screen)
        display_username_text()
        display_password_text()

        # Create text inputs
        # Username
        username = pygame_textinput.TextInput()
        username.max_string_length = 16
        # Password
        password = pygame_textinput.TextInput()
        password.max_string_length = 16
        password.password = True

        # # Displays who made this game text in top left corner of the screen
        # text, rectangle = text_objects("Created by YUYU", pygame.font.Font(FONT_REG, int(40 / 1080 * SCREEN_HEIGHT)))
        # screen.blit(text, rectangle)
        # pygame.display.update()

        # We draw the username and password text below

        username_is_selected = True
        password_is_selected = False
        next_login_area_redraw = 0
        bad_credentials_warning = False
        error_message = ""
        # MAIN EVENT LOOP
        while True:
            display_background_decorations(screen)
            if bad_credentials_warning and pygame.time.get_ticks() < next_login_area_redraw:
                display_login_area(screen)
                display_username_text()
                display_password_text()
                warning_surface, warning_dims = text_objects(error_message, pygame.font.Font(FONT_REG, int(
                    40 / 1080 * SCREEN_HEIGHT)), (231, 24, 55))
                warning_dims = ((SCREEN_WIDTH * 3 / 16), (SCREEN_HEIGHT * 3 / 9))
                screen.blit(warning_surface, warning_dims)
            else:
                display_login_area(screen)
                display_username_text()
                display_password_text()
                bad_credentials_warning = False

            # # Draw the textboxes where the text will go.
            # Username textbox
            username_textbox_rectangle = draw_rectangle(screen, SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 4 / 9,
                                                        5 / 16 * SCREEN_WIDTH,
                                                        1 / 9 * SCREEN_HEIGHT, (210, 210, 210))

            # Password textbox
            password_textbox_rectange = draw_rectangle(screen, SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 6 / 9,
                                                       5 / 16 * SCREEN_WIDTH,
                                                       1 / 9 * SCREEN_HEIGHT, (210, 210, 210))

            # Try adding a button with custom helper
            ev = pygame.event.get()
            click = False

            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    click = True
                if event.type == pygame.QUIT:
                    return self
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user has clicked on the rectangle region corresponding to a textbox
                    if username_textbox_rectangle.collidepoint(event.pos):
                        username_is_selected = True
                        password_is_selected = False
                    elif password_textbox_rectange.collidepoint(event.pos):
                        username_is_selected = False
                        password_is_selected = True
                    else:
                        username_is_selected = False
                        password_is_selected = False

            if username_is_selected:
                username.update(ev)
            if password_is_selected:
                password.update(ev)
            # if username.update(None):
            #     print(username.get_text())
            # if password.update(None):
            #     print(password.get_text())
            screen.blit(username.get_surface(), (SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 4 / 9))
            screen.blit(password.get_surface(), (SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 6 / 9))
            if button_alpha("Back", SCREEN_WIDTH * 1 / 16, SCREEN_HEIGHT * 1 / 9, SCREEN_WIDTH * 2 / 16,
                      SCREEN_HEIGHT * 1 / 9,
                      click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                return login_menu.LoginMenu()
            if button_alpha("Submit", SCREEN_WIDTH * 12 / 16, SCREEN_HEIGHT * 1 / 9, SCREEN_WIDTH * 3 / 16,
                      SCREEN_HEIGHT * 1 / 9,
                      click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                # TODO: Return error messages from the LS:
                # bad username, bad password
                # bad server connection
                # Expired token perhaps?
                status, response = client.login(username.get_text(), password.get_text())
                if status:
                    print(response.json()['access_token'])
                    # TODO: Save this somewhere? request_return.json()['access_token']
                    # TODO: move the user to the main menu state with the game or prompt for the expansion
                else:
                    print("Exception")
                    # Print error out onto screen
                    if response.status_code == 400:
                        print("If statement")
                        next_login_area_redraw = pygame.time.get_ticks() + 5000
                        print(next_login_area_redraw)
                        print(pygame.time.get_ticks())
                        bad_credentials_warning = True
                        error_message = response.json()['error_description']
                        continue
                # Transition to main menu
                print(username.get_text())
                print(password.get_text())
                print(response.json()['access_token'])
                """
                client.username = username.get_text()
                client.password = password.get_text()
                client.access_token = response.json()['access_token']
                client.refresh_token = response.json()['refresh_token']"""
                return lobby_menu.LobbyMenu()

            pygame.display.update()
        #
        #
        # # We need a login menu with username + password or something. Perhaps true OAuth providers? Need to verify spec
        # # We need login backend talky talk. --> Should the logic sit in this menu, or do we decouple following MVP?
        # # We need Success/Failure outcomes (State machine has an output for every arrow) --> Must never return None
        #
        # return LoginMenuPrompt()  # We can return this on fail or something.
