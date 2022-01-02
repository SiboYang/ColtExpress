from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Tuple
import random
from server.enum.Character import Character
from server.enum.TurnType import TurnType
from server.controller.game import Game
from server.model.position import Position
from server.enum.ActionKind import ActionKind
from server.model.loot import Loot
from server.controller.player_manager import PlayerManager
from server.model.card import Card
from server.model.bullet_card import BulletCard
from server.enum.LootType import LootType


class Player:
    def __init__(self):
        self._waiting_for_input: bool = False
        self.get_another_action: bool = False
        self.__hand_of_card: List[Card] = []
        self.discard_pile: List[Card] = []
        self.__bandit: Optional[Character] = None
        self.revolver: List[BulletCard] = []
        self.possessions: List[Loot] = []
        self.all_cards: List[Card] = []
        self.stealin_action: Optional[ActionKind] = None
        # the action that this player is currently executing in Stealin phase
        self.available_bandits: List[Character] = []
        self.available_loots: List[Loot] = []
        self.available_positions: List[List[int]] = []

    def remove_card_from_hand_at_pos(self, index: int) -> Card:
        return self.__hand_of_card.pop(index)

    def get_card_in_hand_at_pos(self, index: int) -> Card:
        return self.__hand_of_card[index]

    def add_card_to_hand(self, card) -> None:
        self.__hand_of_card.append(card)

    def get_hand(self) -> List[Card]:
        return self.__hand_of_card

    #  operation PlayActionCard, client should pass the index of card that are being played
    def play_card_at_pos(self, index: int) -> None:
        if not self._waiting_for_input:
            print("not your turn")
            return
        card_to_play = self.get_card_in_hand_at_pos(index)
        self.remove_card_from_hand_at_pos(index)

        game = Game.get_instance()
        current_turn_type = game.get_current_turn_type()
        current_round = game.get_current_round()
        game.card_just_played = card_to_play
        if current_turn_type == TurnType.Tunnel or (self.get_bandit() == Character.Ghost and game.get_current_turn_index() == 0):
            card_to_play.set_visible(False)
        else:
            card_to_play.set_visible(True)

        current_round.card_played.append(card_to_play)
        self._waiting_for_input = False
        game.end_player_schemin_move()

    # operation drawCard
    def draw_cards(self) -> None:
        if len(self.discard_pile) < 3:
            print("not enough card in discard pile")
            return  # maybe need a way to disable draw button later
        for i in range(3):
            random.shuffle(self.discard_pile)
            card = self.discard_pile.pop()
            self.add_card_to_hand(card)
        self._waiting_for_input = False
        game = Game.get_instance()
        game.card_just_played = None
        game.end_player_schemin_move()

    def is_current_player(self) -> bool:
        return self._waiting_for_input

    def set_current_player(self, its_my_turn: bool):
        self._waiting_for_input = its_my_turn

    def set_position(self, old_position: Position, new_position: Position) -> None:
        if old_position != None:
            old_position.remove_player(self)
        new_position.add_player(self)

    def get_bandit(self) -> Character:
        return self.__bandit

    def set_bandit(self, bandit: Character):
        self.__bandit = bandit

    def get_hand_size(self) -> int:
        return len(self.__hand_of_card)

    def choose_loot(self, loot: Loot):  # this is the index of that loot in the current position of bandit
        current_pos = self.get_position()
        current_pos.remove_loot(loot)
        self.possessions.append(loot)
        game = Game.get_instance()
        game.end_of_card(self)

    def choose_position(self, position: List[int], action: ActionKind) -> None:
        '''
        position should be passed as a array with two elements, the first one is the train index,
        the second one is 0/1, 0 means inside, 1 means roof
        '''
        game = Game.get_instance()
        old_position = self.get_position()
        if action == ActionKind.Move:
            if position[1] == 1:
                new_position = game.get_trains()[position[0]].get_roof()
                self.set_position(old_position, new_position)
                game.end_of_card(self)
            else:
                new_position = game.get_trains()[position[0]].get_inside()
                self.set_position(old_position, new_position)
                game.end_of_card(self)
        elif action == ActionKind.Marshal:
            if position[1] == 1:
                print("Error Marshal should only inside the train")
            else:
                #   remove marshal from old position
                for train in game.get_trains():
                    inside = train.get_inside()
                    if inside.get_marshal_here():
                        inside.set_marshal_here(False)

                #   add marshal to new position
                new_position = game.get_trains()[position[0]].get_inside()
                new_position.set_marshal_here(True)
        game.end_of_card(self)

    def choose_punch_target(self, position, bandit_chose: Character) -> None:  # position is an array with 2 elements
        game = Game.get_instance()
        old_position = self.get_position()
        player_manager = PlayerManager.get_instance()
        player_to_punch = player_manager.get_player_by_character(bandit_chose)
        loots = player_to_punch.possessions
        if len(loots) > 0:
            random.shuffle(loots)
            loot_dropped = loots.pop()
            if self.__bandit == Character.Cheynne and loot_dropped.get_loot_type() == LootType.Purse:
                self.possessions.append(loot_dropped)
            else:
                old_position.add_loot(loot_dropped)

        if position[1] == 1:
            new_position = game.get_trains()[position[0]].get_roof()
            player_to_punch.set_position(old_position, new_position)

        else:
            new_position = game.get_trains()[position[0]].get_inside()
            player_to_punch.set_position(old_position, new_position)

        game.end_of_card(self)

    def choose_shoot_target(self, bandit_chose: Character) -> None:
        game = Game.get_instance()
        bullet = self.revolver.pop()
        player_manager = PlayerManager.get_instance()
        player_to_shoot = player_manager.get_player_by_character(bandit_chose)
        player_to_shoot.discard_pile.append(bullet)
        if self.__bandit == Character.Django:
            d_index, d_inside = self.get_train_index()
            target_index, target_inside = player_to_shoot.get_train_index()
            target_old_pos = player_to_shoot.get_position()
            if target_index == 0 and d_index == 0:
                player_to_shoot.set_position(target_old_pos, game.get_trains()[1].get_inside() if target_inside else game.get_trains()[1].get_roof())
            elif target_index == len(game.get_trains())-1 and d_index == len(game.get_trains())-1:
                player_to_shoot.set_position(target_old_pos, game.get_trains()[len(game.get_trains())-2].get_inside() if target_inside else game.get_trains()[len(game.get_trains())-2].get_roof())
            elif 0 < target_index < len(game.get_trains())-1:
                if target_index > d_index:
                    player_to_shoot.set_position(target_old_pos, game.get_trains()[target_index+1].get_inside() if target_inside else game.get_trains()[target_index+1].get_roof())
                else:
                    player_to_shoot.set_position(target_old_pos, game.get_trains()[target_index-1].get_inside() if target_inside else game.get_trains()[target_index-1].get_roof())
        game.end_of_card(self)
        return

    def get_position(self) -> Position:
        game = Game.get_instance()
        for train in game.get_trains():
            if self in train.get_inside().get_players():
                return train.get_inside()
            elif self in train.get_roof().get_players():
                return train.get_roof()

    def get_train_index(self) -> Tuple[int, bool]:   # if the second bool is true, we are inside, otherwise we are at roof
        game = Game.get_instance()
        for index, train in enumerate(game.get_trains()):
            if self in train.get_roof().get_players():
                return index, False
            if self in train.get_inside().get_players():
                return index, True
