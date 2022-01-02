from typing import Tuple

import pygame
from assets.color_constants import BLACK
from assets.font_constants import FONT_REG
from extensionGame.components import Components
from extensionGame.hand import Hand
from menus.client_info import Client


def text_objects(text, font, color=BLACK):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


class DrawCardButton(Components):
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 active_color: Tuple[int, int, int],
                 normal_color: Tuple[int, int, int]):
        Components.__init__(self, x, y, width, height)
        self.active_color = active_color
        self.normal_color = normal_color

    def draw(self, surface: pygame.Surface):
        mouse = pygame.mouse.get_pos()
        # hovering or not
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            pygame.draw.rect(surface, self.active_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(surface, self.normal_color, (self.x, self.y, self.width, self.height))
        button_text = pygame.font.Font(FONT_REG, 20)
        text_surf, text_rect = text_objects("Draw Cards", button_text)
        text_rect.center = ((self.x + self.width / 2), (self.y + self.height / 2))
        surface.blit(text_surf, text_rect)

    # once clicked, remove the card from hand
    def clicked(self, hand: Hand, all_sprites: pygame.sprite.Group, event, player):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
                # hand.add_card(Card(DJANGO_MOVE, 0, 0, int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.23)), all_sprites)
                # player.draw_cards()
                client = Client.get_instance()
                cmd = {'type': 'DrawCard',
                       'data': {}}
                client.send_data(cmd)
