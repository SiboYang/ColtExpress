import os

import pygame

os.chdir(os.path.abspath(os.path.dirname(__file__)))

import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from assets.game_constants import SCREEN_HEIGHT, SCREEN_WIDTH
from menus.menu_context import MenuContext

# Initialize Pygame
pygame.init()

# Create the screen -- Width, Height
# TODO: Get rid of hardcode later or move to config file
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set Window Title
pygame.display.set_caption("Colt Express")
# Initialize menu state machine
menu = MenuContext()
# Game Loop
running = True
while running:
    # Debug Print
    print("entering primary game loop")

    # Draw Menus (State Design Pattern -- State Machine)
    menu.draw_menu()

    # If there is an event affecting the game, we do something
    for event in pygame.event.get():

        # If Pygame receives a quit signal.
        if event.type == pygame.QUIT:
            print("Quit received")
            exit()
    # Redraws the screen. Not too sure if this is needed here for now, but meh
    pygame.display.update()
