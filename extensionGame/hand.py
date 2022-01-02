from typing import List

import pygame
from extensionGame.card import Card
from extensionGame.components import Components


class Hand(Components):

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 cards: List[Card]):

        Components.__init__(self, x, y, width, height)
        self._cards = cards  # list to store the cards in hand

    def has_card(self, card):
        if card in self._cards:
            return True
        return False

    def add_card(self, card: Card, all_sprites: pygame.sprite.Group):
        self._cards.append(card)
        all_sprites.add(card)

    def remove_card(self, card: Card, all_sprites: pygame.sprite.Group):
        self._cards.remove(card)
        all_sprites.remove(card)

    @property
    def get_chosen_card(self):
        for card in self._cards:
            if card.chosen:
                return card
        return None

    def update(self):
        # change the position of cards in hand when the number of cards in hand changes
        # This algorithm is bad, still finding a better one

        # don't do anything when no card (avoid division by zero error)
        if len(self._cards) == 0:
            return
        pos_x = self.x / 2
        gap = self.width / len(self._cards)  # the gap between cards
        self.check_chosen()
        for card in self._cards:
            card.change_pos(pos_x, self.y)
            pos_x += gap

    def check_chosen(self):
        chosen = False
        for card in self._cards:
            if card.chosen:
                if chosen:
                    card._chosen = False
                else:
                    chosen = True
