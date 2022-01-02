from menus.login_menu import LoginMenu


class MenuContext:
    # We initialize the Menu Context with a starting state called the LoginMenu within the Constructor
    def __init__(self):
        self.__current_menu = LoginMenu()

    def draw_menu(self):
        self.__current_menu = self.__current_menu.draw_menu()
