import pygame

from assets.color_constants import BLACK
from assets.game_constants import SCREEN_HEIGHT
from extensionGame.components import Components


class Bandit(pygame.sprite.Sprite, Components):

    def __init__(self,
                 image_source: str,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 name):

        # constructor calls for Sprite and superclass
        pygame.sprite.Sprite.__init__(self)
        Components.__init__(self, x, y, width, height)
        self.on_roof = False
        self.rect = None
        self.image = pygame.image.load(image_source).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self._render()
        self.name = name

    def get_name(self):
        return self.name

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

    def change_floor(self):
        self.on_roof = not self.on_roof
        if self.on_roof:
            self.y = int(SCREEN_HEIGHT * 0.215)
        else:
            self.y = int(SCREEN_HEIGHT * 0.35)
        # sokect send the new position to the server
        self._render()

    def set_roof(self):
        self.on_roof = True
        self.change_floor()

    def choose_bandit(self, event, b):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
                return b
