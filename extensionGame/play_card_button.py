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


class PlayCardButton(Components):
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
        text_surf, text_rect = text_objects("Play Card", button_text)
        text_rect.center = ((self.x + self.width / 2), (self.y + self.height / 2))
        surface.blit(text_surf, text_rect)

    def clicked(self, hand: Hand, all_sprites: pygame.sprite.Group, event, dic, hand_list, player):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
                card_to_play = hand.get_chosen_card
                if card_to_play is not None:
                    hand.remove_card(card_to_play, all_sprites)
                    card_obj = -1
                    for key, val in dic.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                        if val == card_to_play:
                            card_obj = key
                    index = hand_list.index(card_obj)
                    # test code
                    # player.play_card_at_pos(index)
                    client = Client.get_instance()
                    cmd = {'type': 'PlayCard',
                           'data': {"index": index}}
                    client.send_data(cmd)
