import pygame

from assets.color_constants import BLACK
from extensionGame.components import Components


class Marshal(pygame.sprite.Sprite, Components):

    def __init__(self,
                 image_source: str,
                 x: int,
                 y: int,
                 width: int,
                 height: int):
        # constructor calls for Sprite and superclass
        pygame.sprite.Sprite.__init__(self)
        Components.__init__(self, x, y, width, height)
        self.rect = None
        self.image = pygame.image.load(image_source).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
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
        # calling the setter in the superclass
        self.x = x
        self.y = y
        # sokect send the new position to the server
        self._render()
