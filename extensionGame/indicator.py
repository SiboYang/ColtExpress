import pygame
from assets.color_constants import BLACK
from extensionGame.components import Components
from assets.media_constants import INDICATOR


class Indicator(pygame.sprite.Sprite, Components):

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int
                 ):
        # constructor calls for Sprite and superclass
        pygame.sprite.Sprite.__init__(self)
        Components.__init__(self, x, y, width, height)

        self.image = pygame.image.load(INDICATOR).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        # remove the black boarder around image
        self.image.set_colorkey(BLACK)
        # set the position
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
