import pygame

from assets.color_constants import BLACK
from extensionGame.components import Components
from menus.client_info import Client


class Loot(pygame.sprite.Sprite, Components):

    def __init__(self,
                 image_source: str,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 loot_type,
                 value):
        # constructor calls for Sprite and superclass
        pygame.sprite.Sprite.__init__(self)
        Components.__init__(self, x, y, width, height)
        self.image = pygame.image.load(image_source).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.type = loot_type
        self.value = value
        self._render()

    def _render(self):
        # change the size of the image
        self.rect = self.image.get_rect()
        # remove the black boarder around image
        self.image.set_colorkey(BLACK)
        # set the position
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def change_pos(self, x: int, y: int):
        self.x = x
        self.y = y
        self._render()

    def choose_loot(self, event, l):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
                client = Client.get_instance()
                cmd = {'type': "Loot",
                       'data': {"loot": l}}
                client.send_data(cmd)
