import pygame

import menus.login_menu_prompt as login_menu_prompt
import menus.sign_up_prompt as sign_up_prompt
from assets.color_constants import DARK_GREEN
from assets.font_constants import FONT_BOLD, FONT_LIGHT
from assets.game_constants import SCREEN_HEIGHT, SCREEN_WIDTH, VERSION
from helpers.menu_helpers import text_objects, button, button_alpha
from menus.informal_menu_interface import InformalMenuInterface


class LoginMenu(InformalMenuInterface):

    # @staticmethod
    # def __login():
    #     print("Login button pressed")

    def draw_menu(self):
        screen = pygame.display.get_surface()

        # Sets background for the screen
        screen.fill(DARK_GREEN)

        # Displays the name of the game in big text (We can later replace this with the game splash or something)
        text, rectangle = text_objects('Colt Express', pygame.font.Font(
            FONT_LIGHT, int(110 / 1080 * SCREEN_HEIGHT)))
        rectangle.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 4))
        screen.blit(text, rectangle)

        # Displays the version information in small text at the bottom right corner of the screen
        text, rectangle = text_objects(f'v{VERSION}', pygame.font.Font(
            FONT_BOLD, int(25 / 1440 * SCREEN_HEIGHT)))
        rectangle.center = (int(SCREEN_WIDTH * 0.98),
                            int(SCREEN_HEIGHT * 0.98))
        screen.blit(text, rectangle)

        # Try and draw a button or something
        # menu = pygame_menu.Menu(height=600, width=800, title="Colt Express",
        #                         columns=2, rows=2, theme=pygame_menu.themes.THEME_DARK)

        while True:
            background_image = pygame.image.load("assets/gameboard/coltexpress_keyart_01_1920x1080.jpg")
            background_image = pygame.transform.smoothscale(background_image,
                                                            (int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
            screen.blit(background_image, [0, 0])
            # Try adding a button with custom helper
            ev = pygame.event.get()
            click = False
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    click = True
                if event.type == pygame.QUIT:
                    print("Quit received")
                    exit(0)
            if button_alpha("Login", SCREEN_WIDTH * -0.07, SCREEN_HEIGHT * 0.3, SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.15,
                      click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                return login_menu_prompt.LoginMenuPrompt()
            if button_alpha("Sign Up", SCREEN_WIDTH * -0.045, SCREEN_HEIGHT * 0.5, SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.15,
                      click, screen, (153, 130, 51, 20), (153, 130, 51, 128)):
                return sign_up_prompt.SignUpPrompt()

            pygame.display.update()
