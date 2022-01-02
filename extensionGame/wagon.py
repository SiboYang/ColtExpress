import pygame

from assets.color_constants import BLACK
from assets.media_constants import WAGON
from extensionGame.bandit import Bandit
from extensionGame.components import Components
from extensionGame.marshal import Marshal
from menus.client_info import Client


class Wagon(pygame.sprite.Sprite, Components):

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int):

        # constructor calls for Sprite and superclass
        pygame.sprite.Sprite.__init__(self)
        Components.__init__(self, x, y, width, height)

        self.image = pygame.image.load(WAGON).convert_alpha()
        # change the size of the image loaded
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        # remove the black boarder around image
        self.image.set_colorkey(BLACK)
        # set the position
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def chosen_bandit(self, bandit: Bandit, event, index, roof):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            # when clicking the upper part of the wagon  (y * 0.3)
            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height * 0.5:
                # bandit.change_pos(self.x, bandit.y)
                client = Client.get_instance()
                cmd = {'type': 'Move',
                       'data': {"index": [index, roof]}}
                client.send_data(cmd)

    def chosen_marshal(self, bandit: Marshal, event, index, roof):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            # when clicking the upper part of the wagon  (y * 0.3)
            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height * 0.5:
                # bandit.change_pos(self.x, bandit.y)
                client = Client.get_instance()
                cmd = {'type': 'Marshal',
                       'data': {"index": [index, roof]}}
                client.send_data(cmd)

    def punch_pos(self, event, index):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            # when clicking the upper part of the wagon  (y * 0.3)
            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height * 0.5:
                return index
