import os

import pygame

os.chdir(os.path.abspath(os.path.dirname(__file__)))

import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from extensionGame.extension_gameboard import ExtensionGame


def main():
    pygame.init()
    eg = ExtensionGame()
    eg.draw_menu()


main()
