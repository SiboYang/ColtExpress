import pygame
from pprint import pprint
import pickle
import math
import extensionGame.extension_gameboard as extension_gameboard
from assets.game_constants import SCREEN_HEIGHT, SCREEN_WIDTH
from menus.client_info import Client
from menus.informal_menu_interface import InformalMenuInterface
from server.enum.Character import Character


class BanditMenu(InformalMenuInterface):
    def draw_menu(self):
        print("Initializing Bandit menu...")
        pygame.init()
        # Color the background white
        background_colour = (255, 255, 255)
        (width, height) = (SCREEN_WIDTH, SCREEN_HEIGHT)
        # Makes first connection to the game server.
        client = Client.get_instance()
        status = client.connected
        while not status:
            status = client.connected
            print("Waiting for client to connect.")

        # client.server_socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # client.server_socket_connection.setblocking(True)
        # mysocket = client.server_socket_connection.connect((client.server_ip, int(client.server_port)))

        # TODO: Works up until here. Just need to work out the networking sequence now.
        # Retrieve list of bandits to draw here
        # ==========================================================================
        # Operation so that we get a list of disabled bandits.
        #   Begin connection to the new game server. (Detach from game manager server)
        # Draw the "players are picking screen"
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Other Players are picking!')
        screen.fill(background_colour)
        myfont = pygame.font.SysFont('Arial', 50)
        textsurface = myfont.render('Another player is picking a bandit...', False, (0, 0, 0))
        screen.blit(textsurface, (.3 * width, .05 * height))
        pygame.display.update()
        # wait for message from server in the background
        # To start, it is assumed to not be the turn of the client.
        current_turn = False
        # Wait until server lets us know that it is our turn to play
        bandits_available_enums = []
        while not current_turn:
            payload = client.receive_data()
            print("===========================================================")
            pprint(payload)
            if payload['type'] == "choose_bandit":
                if payload['data']['my_id'] != "" and payload['data']['my_turn']:
                    # we know that it is our turn and that this is our assigned ID.
                    client.my_player_id = payload['data']['my_id']
                    current_turn = True
                    bandits_available_enums = payload['data']['available_bandits']

        print(bandits_available_enums)  # TODO: Debug statement dumps the resulting list.

        # Print a text that asks player to pick their bandit
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Choose Bandit')
        screen.fill(background_colour)

        # Draw the images of the bandits.
        # TODO: We can simulate a bandit as taken by either drawing something on top or changing the transparency.
        belleImg = pygame.image.load('assets/bandit_imgs/belle.png')
        belleImg = pygame.transform.scale(belleImg, (math.ceil(width*.25), math.ceil(height*.3125)))

        cheyenneImg = pygame.image.load('assets/bandit_imgs/cheyenne.png')
        cheyenneImg = pygame.transform.scale(cheyenneImg, (math.ceil(width*.25), math.ceil(height*.3125)))

        djangoImg = pygame.image.load('assets/bandit_imgs/django.png')
        djangoImg = pygame.transform.scale(djangoImg, (math.ceil(width*.25), math.ceil(height*.3125)))

        docImg = pygame.image.load('assets/bandit_imgs/doc.png')
        docImg = pygame.transform.scale(docImg, (math.ceil(width*.25), math.ceil(height*.3125)))

        ghostImg = pygame.image.load('assets/bandit_imgs/ghost.png')
        ghostImg = pygame.transform.scale(ghostImg, (math.ceil(width*.25), math.ceil(height*.3125)))

        tucoImg = pygame.image.load('assets/bandit_imgs/tuco.png')
        tucoImg = pygame.transform.scale(tucoImg, (math.ceil(width*.25), math.ceil(height*.3125)))

        def setBandit(name, x, y):
            screen.blit(name, (x, y))

        # TODO: Convert bandits_available_enums to bandits_available which is a string. This is for legacy reasons.
        bandits_available = bandits_available_enums

        # Append the bandit to the bandits list if it is in the list of bandits available.
        bandits = []
        for bandit in bandits_available:  # this is now of type bandit in the enum class.
            if Character.Belle.value is bandit.value:
                bandits.append([belleImg, width * .08, height * .16, Character.Belle])
            elif Character.Cheynne.value is bandit.value:
                bandits.append([cheyenneImg, width * .361, height * .16, Character.Cheynne])
            elif Character.Django.value is bandit.value:
                bandits.append([djangoImg, width * .638, height * .16, Character.Django])
            elif Character.Doc.value is bandit.value:
                bandits.append([docImg, width * .08, height * .48, Character.Doc])
            elif Character.Ghost.value is bandit.value:
                bandits.append([ghostImg, width * .361, height * .48, Character.Ghost])
            elif Character.Tuco.value is bandit.value:
                bandits.append([tucoImg, width * .638, height * .48, Character.Tuco])
                
        for bandit in bandits:
            setBandit(bandit[0], bandit[1], bandit[2])  # banditImage, x, y coords placed on the screen.

        myfont = pygame.font.SysFont('Arial', 50)
        textsurface = myfont.render('Choose your Bandit', False, (0, 0, 0))
        screen.blit(textsurface, (.35 * width, .05 * height))
        pygame.display.flip()

        running = True
        bandit_chosen = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and bandit_chosen == False:
                    x, y = event.pos

                    for bandit in bandits:
                        if bandit[0].get_rect(topleft=(bandit[1], bandit[2])).collidepoint(x, y):
                            print('you choose ' + str(bandit[3]))
                            screen.fill((255, 255, 255))
                            textsurface = myfont.render('You have chosen ' + str(bandit[3].name), False, (0, 0, 0))
                            # TODO: here we can send the return back to the server. We must send the bandit enums back.
                            payload = {
                                "type": "choose_bandit",
                                "data": {
                                    "chosen_bandit": bandit[3]
                                }
                            }
                            client.send_data(payload)

                            bandit[0] = pygame.transform.scale(bandit[0], (math.ceil(.55*width), math.ceil(.42*height)))

                            screen.blit(textsurface, (.3 * width, .05 * height))
                            setBandit(bandit[0], .22*width, .26*height)
                            pygame.display.flip()
                            bandit_chosen = True
                            return extension_gameboard.ExtensionGame()
                pygame.display.update()
