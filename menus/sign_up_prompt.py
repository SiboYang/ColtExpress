import pygame

import helpers.pygame_textinput as pygame_textinput
import menus.login_menu as login_menu
from assets.color_constants import DARK_GREEN, LIGHT_BLUE, BLUE
from assets.font_constants import FONT_LIGHT, FONT_REG
from assets.game_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from helpers.menu_helpers import text_objects, button, draw_rectangle, button_alpha
from menus import lobby_menu
from menus.client_info import Client
from menus.informal_menu_interface import InformalMenuInterface


class SignUpPrompt(InformalMenuInterface):
    def draw_menu(self):
        screen = pygame.display.get_surface()

        # Create text inputs
        # Username
        username = pygame_textinput.TextInput()
        # username.set_text_color((255, 255, 255))
        # username.set_cursor_color((0,0,0))
        username.max_string_length = 16
        # username.surface.set_alpha(100)
        # username.surface = pygame.Surface((int(SCREEN_WIDTH * 5 / 16), int(SCREEN_HEIGHT * 1 / 9)))

        # Password
        password = pygame_textinput.TextInput()
        # password.set_text_color((255, 255, 255))
        # password.set_cursor_color((0,0,0))
        password.max_string_length = 16
        password.password = True
        # password.surface.set_alpha(100)
        # password.surface = pygame.Surface((int(SCREEN_WIDTH * 5 / 16), int(SCREEN_HEIGHT * 1 / 9)))
        # password.surface = pygame.transform.scale(password.surface, (int(SCREEN_WIDTH * 5 / 16), int(SCREEN_HEIGHT * 1 / 9)))



        client = Client.get_instance()
        username_is_selected = True
        password_is_selected = False
        next_login_area_redraw = 0
        bad_credentials_warning = False
        error_message = ""
        # MAIN EVENT LOOP
        while True:

            # Sets background for the screen
            background_image = pygame.image.load("assets/gameboard/coltexpress_keyart_01_1920x1080.jpg")
            background_image = pygame.transform.smoothscale(background_image,
                                                            (int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
            screen.blit(background_image, [0, 0])
            # Displays the name of the game in big text (We can later replace this with the game splash or something)
            text, rectangle = text_objects('Sign Up', pygame.font.Font(
                FONT_LIGHT, int(110 / 1080 * SCREEN_HEIGHT)), (255, 255, 255))
            rectangle.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 4))
            screen.blit(text, rectangle)
            # We draw a square for the login screen prompts. Username and Password currently placed below the relative
            # location of the title screen. We will put the username and password text after this.
            # The textbox that will hold the username and password input fields will go into the constant update
            # Because a user will type something, and will need to hit backspace, so we want to redraw every time.
            draw_rectangle(screen, SCREEN_WIDTH * 2 / 16, SCREEN_HEIGHT * 3 / 9, 12 / 16 * SCREEN_WIDTH,
                           5 / 9 * SCREEN_HEIGHT, (87, 87, 87, 225))

            # We draw the username and password text below
            # Username Text
            username_surface, username_dims = text_objects("Username:",
                                                           pygame.font.Font(FONT_LIGHT, int(0.9 / 16 * SCREEN_HEIGHT)),  (210, 210, 210))
            username_dims = ((SCREEN_WIDTH * 3 / 16), (SCREEN_HEIGHT * 4 / 9))
            screen.blit(username_surface, username_dims)

            # Password Text
            password_surface, password_dims = text_objects("Password:",
                                                           pygame.font.Font(FONT_LIGHT, int(0.9 / 16 * SCREEN_HEIGHT)),  (210, 210, 210))
            password_dims = ((SCREEN_WIDTH * 3 / 16), (SCREEN_HEIGHT * 6 / 9))
            screen.blit(password_surface, password_dims)

            if bad_credentials_warning and next_login_area_redraw > pygame.time.get_ticks():
                warning_surface, warning_dims = text_objects(error_message, pygame.font.Font(FONT_REG, int(
                    40 / 1080 * SCREEN_HEIGHT)), (231, 24, 55))
                warning_dims = ((SCREEN_WIDTH * 3 / 16), (SCREEN_HEIGHT * 3 / 9))
                screen.blit(warning_surface, warning_dims)
            else:
                bad_credentials_warning = False
            # # Draw the textboxes where the text will go.
            # Username textbox
            username_textbox_rectangle = draw_rectangle(screen, SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 4 / 9,
                                                        5 / 16 * SCREEN_WIDTH,
                                                        1 / 9 * SCREEN_HEIGHT,  (210, 210, 210))

            # Password textbox
            password_textbox_rectange = draw_rectangle(screen, SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 6 / 9,
                                                       5 / 16 * SCREEN_WIDTH,
                                                       1 / 9 * SCREEN_HEIGHT,  (210, 210, 210))

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
            screen.blit(username.get_surface(),
                        (SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 4 / 9))
            screen.blit(password.get_surface(),
                        (SCREEN_WIDTH * 8 / 16, SCREEN_HEIGHT * 6 / 9))
            if button_alpha("Back", SCREEN_WIDTH * 1 / 16, SCREEN_HEIGHT * 1 / 9, SCREEN_WIDTH * 2 / 16,
                      SCREEN_HEIGHT * 1 / 9,
                      click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                return login_menu.LoginMenu()
            if button_alpha("Submit", SCREEN_WIDTH * 12 / 16, SCREEN_HEIGHT * 1 / 9, SCREEN_WIDTH * 3 / 16,
                      SCREEN_HEIGHT * 1 / 9,
                      click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                # TODO: Figure out how login functionality deals with requiring admin to make an account
                status, k = client.sign_up(username.get_text(), password.get_text())
                # TODO: Handle name taken and unmatched password policy returns
                if status:
                    print(k.text)
                    print(username.get_text())
                    print(password.get_text())
                    l_status, l_res = client.login(username.get_text(), password.get_text())
                    if l_status:
                        print("Logged In")
                        print(l_res)
                        return lobby_menu.LobbyMenu()
                    else:
                        print(l_res)
                        return login_menu.LoginMenu()
                else:
                    bad_credentials_warning = True
                    print(k.text)
                    error_message = k.text
                    next_login_area_redraw = pygame.time.get_ticks() + 5000
                    continue
                # Returns user back to login on success
                # TODO: Consider adding a "Successful" message perhaps? Maybe a dropdown?
                # return login_menu.LoginMenu()

            pygame.display.update()
