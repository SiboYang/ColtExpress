import pygame

from assets.color_constants import BLACK
from extensionGame.components import Components


class Card(pygame.sprite.Sprite, Components):

    def __init__(self,
                 image_source: str,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 clickable):

        # constructor calls for Sprite and superclass
        pygame.sprite.Sprite.__init__(self)
        Components.__init__(self, x, y, width, height)

        self.chosen_y = 0
        self._chosen = False
        self.image = pygame.image.load(image_source).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.clickable = clickable
        self.rect = self.image.get_rect()
        # remove the black boarder of image
        self.image.set_colorkey(BLACK)
        self._render()

    # getter for chosen
    @property
    def chosen(self):
        return self._chosen

    def _render(self):
        # set the position
        self.rect.x = self.x
        self.rect.y = self.y
        # if is the chosen card, update the y
        if self._chosen:
            self.rect.y = self.chosen_y

    def draw(self, surface: pygame.Surface):

        surface.blit(self.image, self.rect)

    def change_pos(self, x: int, y: int):
        self.x = x
        self.y = y
        self.chosen_y = self.y - self.height * 0.7
        self._render()

    def update(self):
        # get whether this card is clicked
        if self.clickable:
            click = pygame.mouse.get_pressed()[0]
            if self.rect.collidepoint(pygame.mouse.get_pos()) and click:
                self._chosen = not self._chosen
            self._render()
