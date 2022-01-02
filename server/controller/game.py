from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Dict

if TYPE_CHECKING:
    from server.controller.player import Player
import random
from server.enum.EndOfRoundEvent import EndOfRoundEvent
from server.model.bullet_card import BulletCard
from server.enum.GamePhase import GamePhase
from server.controller.player_manager import PlayerManager
from server.model.action_card import ActionCard
from server.model.train_car import TrainCar
from server.enum.ActionKind import ActionKind
from server.model.loot import Loot
from server.enum.LootType import LootType
from server.model.round import Round
from server.enum.TurnType import TurnType
from server.enum.Character import Character
random.seed(3)

class Game:
    __instance = None

    def __init__(self):

        self.game_end: bool = False
        self.final_score: Dict[str, int] = {}
        self.__current_player_index: int = 0
        self.__current_round_index: int = 0
        self.__current_turn_index: int = 0
        self.__current_phase: GamePhase = GamePhase.Schemin
        self.__number_of_player_played_this_turn: int = 0
        self.__game_rounds: List[Round] = [Round([TurnType.Standard, TurnType.Tunnel, TurnType.Standard, TurnType.Standard], EndOfRoundEvent.SwivelArm, "1_1"), \
                                           Round([TurnType.Standard, TurnType.Standard, TurnType.Tunnel, TurnType.Switching], EndOfRoundEvent.AngeryMarshal, "1_7"), \
                                           Round([TurnType.Standard, TurnType.SpeedingUp, TurnType.Standard], EndOfRoundEvent.NULL, "1_2"),\
                                           Round([TurnType.Standard, TurnType.Tunnel, TurnType.SpeedingUp, TurnType.Standard], EndOfRoundEvent.TakeItAll, "1_6"),\
                                           Round([TurnType.Standard, TurnType.Standard, TurnType.Standard, TurnType.Standard], EndOfRoundEvent.Braking, "1_3"),\
                                           Round([TurnType.Standard, TurnType.Standard, TurnType.Tunnel, TurnType.Standard, TurnType.Standard], EndOfRoundEvent.PassengerRebellion, "1_4"),\
                                           Round([TurnType.Standard, TurnType.Tunnel, TurnType.Standard, TurnType.Tunnel, TurnType.Standard], EndOfRoundEvent.NULL, "1_5")]
        
        self.train_station_cards: List[Round] = [Round([TurnType.Standard, TurnType.Standard, TurnType.Tunnel, TurnType.Standard], EndOfRoundEvent.MarshalRevenge, "1_8"),\
                                                 Round([TurnType.Standard, TurnType.Standard, TurnType.Tunnel, TurnType.Standard], EndOfRoundEvent.Pickpocketing, "1_9"),\
                                                 Round([TurnType.Standard, TurnType.Standard, TurnType.Tunnel, TurnType.Standard], EndOfRoundEvent.HostageConductor, "1_10")]
        self.__participants: List[Player] = []
        self.__trains: List[TrainCar] = []
        self.card_just_played: Optional[ActionCard] = None
        # card just played is action card player just played in the schemin phase, it's not necessarily the last
        # card of card played this round, since player can choose to draw card.
        # This attribute is for UI displaying purpose
        self.current_action_card: Optional[ActionCard] = None
        # This attribute is the current action card we are executing in the stealin phase,
        # for UI displaying purpose.
        self.bandit_choices: List[Character] = [Character.Cheynne, Character.Belle, Character.Django,
                                                Character.Doc, Character.Ghost, Character.Tuco]
        Game.__instance = self

    @staticmethod
    def get_instance() -> Game:
        """ Static access method. """
        if Game.__instance is None:
            Game()
        return Game.__instance

    def _initialize_train(self) -> None:

        self.__trains.append(TrainCar(True))  # locomotive
        self.__trains[0].get_inside().set_marshal_here(True)
        num_of_participant = len(self.__participants)
        for i in range(num_of_participant):
            self.__trains.append(TrainCar(False))  # normal trains

        self.__trains[0].get_inside().add_loot(Loot(LootType.StrongBox, 1000))
        # currently not random, will figure it out later
        for j in range(1, len(self.__trains)):
            self.__trains[j].get_inside().add_loot(Loot(LootType.Purse, 300))
            self.__trains[j].get_inside().add_loot(Loot(LootType.Ruby, 300))

    def _initialize_participants(self) -> None:
        player_manager = PlayerManager.get_instance()
        self.__participants = player_manager.get_all_players()

    def _initialize_players(self) -> None:
        for count, player in enumerate(self.__participants):
            for i in range(6):
                player.revolver.append(BulletCard(i, player.get_bandit()))
            player.all_cards.append(ActionCard(ActionKind.Move, player.get_bandit()))
            player.all_cards.append(ActionCard(ActionKind.Move, player.get_bandit()))
            player.all_cards.append(ActionCard(ActionKind.ChangeFloor, player.get_bandit()))
            player.all_cards.append(ActionCard(ActionKind.Shoot, player.get_bandit()))
            player.all_cards.append(ActionCard(ActionKind.Rob, player.get_bandit()))
            player.all_cards.append(ActionCard(ActionKind.Rob, player.get_bandit()))
            player.all_cards.append(ActionCard(ActionKind.Punch, player.get_bandit()))
            player.all_cards.append(ActionCard(ActionKind.ChangeFloor, player.get_bandit()))
            player.all_cards.append(ActionCard(ActionKind.Marshal, player.get_bandit()))
            player.all_cards.append(ActionCard(ActionKind.Shoot, player.get_bandit()))

            #random.shuffle(player.all_cards)

            for i in range(6):
                card = player.all_cards.pop()
                player.add_card_to_hand(card)

            for j in range(4):
                card = player.all_cards.pop()
                player.discard_pile.append(card)

            player.possessions.append(Loot(LootType.Purse, 250))
            if (count + 1) % 2 == 1:  # odd bandit
                self.__trains[-1].get_inside().add_player(player)
            else:
                self.__trains[-2].get_inside().add_player(player)

    def initialize(self) -> None:
        self._initialize_participants()
        self._initialize_train()
        self._initialize_players()

        # currently hardcoded for demo
        #random.shuffle(self.__game_rounds)
        self.__game_rounds = self.__game_rounds[:4] # draw 4 round cards
        #random.shuffle(self.train_station_cards)
        self.__game_rounds.append(self.train_station_cards[0]) # append the train station card
        self.__participants[0].set_current_player(True)

    def get_participant_at(self, index: int) -> Player:
        return self.__participants[index]

    def size_of_participants(self) -> int:
        return len(self.__participants)

    def get_game_rounds_at(self, index: int) -> Round:
        return self.__game_rounds[index]

    def prepare_player_schemin_move(self) -> None:
        new_current_player = self.get_participant_at(self.__current_player_index)
        new_current_player.set_current_player(True)

    def get_current_turn_type(self) -> TurnType:
        return self.get_game_rounds_at(self.__current_round_index).get_turn_type(self.__current_turn_index)

    def end_player_schemin_move(self) -> None:
        self.__number_of_player_played_this_turn += 1
        num_of_participating_players = self.size_of_participants()

        current_turn_type = self.get_current_turn_type()
        current_player = self.__participants[self.__current_player_index]

        if current_turn_type == TurnType.SpeedingUp:
            # this means the player is in the first turn of a speeding up turn
            if not current_player.get_another_action:
                self.__number_of_player_played_this_turn -= 1
                # then we assume this player doesn't play, and let him play again

        if self.__number_of_player_played_this_turn == num_of_participating_players:
            self.__current_turn_index += 1
            current_round = self.get_game_rounds_at(self.__current_round_index)
            num_of_turns_this_round = current_round.get_num_of_turns()

            # current round is not over
            if self.__current_turn_index < num_of_turns_this_round:
                self.__number_of_player_played_this_turn = 0
                self.__current_player_index = self.__current_round_index
            else:  # current round over, enter stealing phase
                self.__current_phase = GamePhase.Stealin
                self.card_just_played = None
                self.current_action_card = None
                for p in self.__participants:
                    hand_size = p.get_hand_size()
                    for i in range(hand_size):
                        card = p.remove_card_from_hand_at_pos(0)
                        p.discard_pile.append(card)
                    p.set_current_player(False)
                self.execute_action()
                return

        else:
            if current_turn_type == TurnType.SpeedingUp:
                if not current_player.get_another_action:
                    current_player.get_another_action = True
                    self.__current_player_index = self.__current_player_index
                else:
                    current_player.get_another_action = False
                    self.__current_player_index = (self.__current_player_index + 1) % num_of_participating_players
                    # although in Speeding up, but the second speeding up turn
            elif current_turn_type == TurnType.Switching:
                self.__current_player_index = (self.__current_player_index - 1) % num_of_participating_players
            else:
                self.__current_player_index = (self.__current_player_index + 1) % num_of_participating_players

        self.prepare_player_schemin_move()

    def get_current_round(self) -> Round:
        return self.__game_rounds[self.__current_round_index]

    def choose_bandit(self, bandit: Character, player_id: str) -> None:
        if bandit not in self.bandit_choices:
            print("Not valid choice")
            return
        player_manager = PlayerManager.get_instance()
        player = player_manager.get_player_by_id(player_id)
        player.set_bandit(bandit)
        players = player_manager.get_all_players()
        self.bandit_choices.remove(bandit)
        for p in players:
            if p.get_bandit() is None:  # still player doesn't choose
                return
        self.initialize()
        return

    # to provide bandit chocie in bandit choosing part
    def get_available_bandit_choice(self) -> List[Character]:
        return self.bandit_choices


    def execute_action(self) -> None:
        if len(self.get_current_round().card_played) == 0:
            self.end_stealin_phase()
            return

        action_card = self.get_current_round().card_played.pop(0)
        self.current_action_card = action_card
        action_kind = action_card.action_kind
        if action_kind == ActionKind.Move:
            self.calculate_move(action_card, action_card.character)
        elif action_kind == ActionKind.Rob:
            self.calculate_rob(action_card, action_card.character)
        elif action_kind == ActionKind.Shoot:
            self.calculate_shoot(action_card, action_card.character)
        elif action_kind == ActionKind.ChangeFloor:
            self.execute_change_floor(action_card, action_card.character)
        elif action_kind == ActionKind.Marshal:
            self.calculate_marshal(action_card, action_card.character)
        elif action_kind == ActionKind.Punch:
            self.calculate_punch(action_card, action_card.character)

    def calculate_rob(self, action_card: ActionCard, character: Character) -> None:
        player_manager = PlayerManager.get_instance()
        player = player_manager.get_player_by_character(character)
        player.discard_pile.append(action_card)
        loots = player.get_position().get_loots()
        if len(loots) == 0:
            self.end_of_card(player)
            return
        else:
            for loot in loots:
                player.available_loots.append(loot)

            player.stealin_action = ActionKind.Rob
            player.set_current_player(True)
            return

    def calculate_shoot(self, action_card: ActionCard, character: Character) -> None:
        player_manager = PlayerManager.get_instance()
        player = player_manager.get_player_by_character(character)
        player.discard_pile.append(action_card)
        current_position = player.get_position()
        if len(player.revolver) == 0:
            print("No bullets")
            self.end_of_card(player)
        if current_position.is_roof():
            for train in self.__trains:
                if len(train.get_roof().get_players()) != 0:
                    for p in train.get_roof().get_players():
                        player.available_bandits.append(p.get_bandit())
            if player.get_bandit() == character.Tuco:
                for index, train in enumerate(self.__trains):
                    if player in train.get_roof().get_players():
                        for p in train.get_inside().get_players():
                            player.available_bandits.append(p.get_bandit())
            if len(player.available_bandits) > 1 and character.Belle in player.available_bandits:
                player.available_bandits.remove(character.Belle)

            if len(player.available_bandits) == 0:
                self.end_of_card(player)
                return
            else:
                player.stealin_action = ActionKind.Shoot
                player.set_current_player(True)
                return
        else:
            for index, train in enumerate(self.__trains):
                if player in train.get_inside().get_players():
                    start_index = max(0, index - 1)
                    end_index = min(len(self.__trains) - 1, index + 1)
                    for i in range(len(self.__trains)):
                        if start_index <= i <= end_index and i != index:
                            position = self.__trains[i].get_inside()
                            players = position.get_players()
                            if len(players) != 0:
                                for p in players:
                                    player.available_bandits.append(p.get_bandit())

            if len(player.available_bandits) > 1 and character.Belle in player.available_bandits:
                player.available_bandits.remove(character.Belle)

            if len(player.available_bandits) == 0:
                self.end_of_card(player)
                return
            else:
                player.stealin_action = ActionKind.Shoot
                player.set_current_player(True)
                return

    def calculate_punch(self, action_card: ActionCard, character: Character) -> None:
        player_manager = PlayerManager.get_instance()
        player = player_manager.get_player_by_character(character)
        player.discard_pile.append(action_card)
        current_position = player.get_position()
        if len(current_position.get_players()) == 1:  # only the player is at the position
            self.end_of_card(player)
            return
        else:
            for p in current_position.get_players():
                if p != player:
                    player.available_bandits.append(p.get_bandit())

                if len(player.available_bandits) > 1 and character.Belle in player.available_bandits:
                    player.available_bandits.remove(character.Belle)
            for index, train in enumerate(self.__trains):
                if player in train.get_roof().get_players():
                    start_index = max(0, index - 1)
                    end_index = min(len(self.__trains) - 1, index + 1)
                    for i in range(len(self.__trains)):
                        if (start_index <= i <= end_index) and i != index:
                            player.available_positions.append(
                                [0, 1])  # the first is inside, second is roof, 1 mean available
                        else:
                            player.available_positions.append([0, 0])
                    break
                elif player in train.get_inside().get_players():
                    start_index = max(0, index - 1)
                    end_index = min(len(self.__trains) - 1, index + 1)  # need to be changed later
                    for i in range(len(self.__trains)):
                        if (start_index <= i <= end_index) and i != index:
                            player.available_positions.append(
                                [1, 0])  # the first is inside, second is roof, 1 mean available
                        else:
                            player.available_positions.append([0, 0])

            player.stealin_action = ActionKind.Punch
            player.set_current_player(True)
            return

    def execute_change_floor(self, action_card: ActionCard, character: Character) -> None:
        player_manager = PlayerManager.get_instance()
        player = player_manager.get_player_by_character(character)
        player.discard_pile.append(action_card)
        for index, train in enumerate(self.__trains):
            if player in train.get_roof().get_players():
                player.set_position(train.get_roof(), train.get_inside())
                self.end_of_card(player)
                return
            if player in train.get_inside().get_players():
                player.set_position(train.get_inside(), train.get_roof())
                self.end_of_card(player)
                return

    def calculate_move(self, action_card: ActionCard, character: Character) -> None:
        player_manager = PlayerManager.get_instance()
        player = player_manager.get_player_by_character(character)
        player.discard_pile.append(action_card)
        # first find the position of the player
        for index, train in enumerate(self.__trains):
            if player in train.get_roof().get_players():
                start_index = max(0, index - 3)
                end_index = min(len(self.__trains) - 1, index + 3)  # need to be changed later
                for i in range(len(self.__trains)):
                    if (start_index <= i <= end_index) and i != index:
                        player.available_positions.append(
                            [0, 1])  # the first is inside, second is roof, 1 mean available
                    else:
                        player.available_positions.append([0, 0])
                player.stealin_action = ActionKind.Move
                player.set_current_player(True)
                return
            elif player in train.get_inside().get_players():
                start_index = max(0, index - 1)
                end_index = min(len(self.__trains) - 1, index + 1)
                num_of_choice = 0
                for i in range(len(self.__trains)):
                    if start_index <= i <= end_index and i != index:
                        num_of_choice += 1
                        player.available_positions.append(
                            [1, 0])  # the first is inside, second is roof, 1 mean available
                    else:
                        player.available_positions.append([0, 0])
                if num_of_choice == 1:  # no need for user input
                    new_index = player.available_positions.index([1, 0])
                    player.set_position(player.get_position(), self.__trains[new_index].get_inside())
                    self.end_of_card(player)
                    return
                else:
                    player.stealin_action = ActionKind.Move
                    player.set_current_player(True)
                    return

    def calculate_marshal(self, action_card: ActionCard, character: Character) -> None:
        player_manager = PlayerManager.get_instance()
        player = player_manager.get_player_by_character(character)
        player.discard_pile.append(action_card)
        for index, train in enumerate(self.__trains):
            if train.get_inside().get_marshal_here():
                old_index = index
                start_index = max(0, index - 1)
                end_index = min(len(self.__trains) - 1, index + 1)
                num_of_choice = 0
                for i in range(len(self.__trains)):
                    if start_index <= i <= end_index and i != index:
                        num_of_choice += 1
                        player.available_positions.append([1, 0])
                    else:
                        player.available_positions.append([0, 0])

                if num_of_choice == 1:  # no need for user input
                    new_index = player.available_positions.index([1, 0])
                    self.__trains[new_index].get_inside().set_marshal_here(True)
                    self.__trains[old_index].get_inside().set_marshal_here(False)
                    self.end_of_card(player)
                    return
                else:
                    player.stealin_action = ActionKind.Marshal
                    player.set_current_player(True)
                    return

    def end_stealin_phase(self) -> None:
        # do a few checks for the end of round events
        current_event = self.__game_rounds[self.__current_round_index].end_round_event
        if current_event == EndOfRoundEvent.TakeItAll:
            for train in self.__trains:
                if train.get_inside().get_marshal_here():
                    train.get_inside().add_loot(Loot(LootType.StrongBox, 1000))
                elif train.get_roof().get_marshal_here():
                    train.get_roof().add_loot(Loot(LootType.StrongBox, 1000))

        elif current_event == EndOfRoundEvent.Braking:
            for i in range(1,len(self.__trains)):
                roof = self.__trains[i].get_roof()
                for player in roof.get_players():
                    player.set_position(roof, self.__trains[i-1].get_roof())

        elif current_event == EndOfRoundEvent.SwivelArm:
            for train in self.__trains:
                roof = train.get_roof()
                for player in roof.get_players():
                    player.set_position(roof, self.__trains[-1].get_roof())

        elif current_event == EndOfRoundEvent.PassengerRebellion:
            for train in self.__trains:
                inside = train.get_inside()
                for player in inside.get_players():
                    player.discard_pile.append(BulletCard(1, Character.Marshall))

        elif current_event == EndOfRoundEvent.AngeryMarshal:
            for train in self.__trains:
                roof = train.get_roof()
                for player in roof.get_players():
                    player.discard_pile.append(BulletCard(1, Character.Marshall))

            for i in range(0, len(self.__trains)-1):
                if self.__trains[i].get_inside().get_marshal_here():
                    self.__trains[i].get_inside().set_marshal_here(False)
                    self.__trains[i+1].get_inside().set_marshal_here(True)
                    break

        elif current_event == EndOfRoundEvent.MarshalRevenge:
            for train in self.__trains:
                roof = train.get_roof()
                for player in roof.get_players():
                    min_loot = None
                    min_value = 10000
                    for loot in player.possessions:
                        if loot.get_loot_type() == LootType.Purse:
                            if loot.get_loot_value() < min_value:
                                min_value = loot.get_loot_value()
                                min_loot = loot

                    if min_value != 10000:
                        player.possessions.remove(min_loot)

        elif current_event == EndOfRoundEvent.Pickpocketing:
            for train in self.__trains:
                if len(train.get_inside().get_players()) == 1:
                    purses = []
                    for loot in train.get_inside().get_loots():
                        if loot.get_loot_type() == LootType.Purse:
                            purses.append(loot)
                    if len(purses) > 0:
                        train.get_inside().get_players()[0].possessions.append(purses[0])
                        train.get_inside().get_loots().remove(purses[0])

                elif len(train.get_roof().get_players()) == 1:
                    purses = []
                    for loot in train.get_roof().get_loots():
                        if loot.get_loot_type() == LootType.Purse:
                            purses.append(loot)
                    if len(purses) > 0:
                        train.get_roof().get_players()[0].possessions.append(purses[0])
                        train.get_roof().get_loots().remove(purses[0])

        elif current_event == EndOfRoundEvent.HostageConductor:
            for player in self.__trains[0].get_inside().get_players():
                player.possessions.append(Loot(LootType.Purse, 250))

            for player in self.__trains[0].get_roof().get_players():
                player.possessions.append(Loot(LootType.Purse, 250))

        self.__current_round_index += 1
        self.__current_turn_index = 0
        self.__current_phase = GamePhase.Schemin
        num_of_participating_players = self.size_of_participants()
        self.__current_player_index = self.__current_round_index % num_of_participating_players
        self.__participants[self.__current_player_index].set_current_player(True)
        if self.__current_round_index >= len(self.__game_rounds):
            self.end_game()
            return
        # distribute the cards
        player_manager = PlayerManager.get_instance()
        all_players = player_manager.get_all_players()
        for player in all_players:
            random.shuffle(player.discard_pile)
            for i in range(6):
                card = player.discard_pile.pop()
                player.add_card_to_hand(card)
            if player.get_bandit() == Character.Doc:
                card = player.discard_pile.pop()
                player.add_card_to_hand(card)
        return

    def end_game(self):
        self.game_end = True
        self.__current_phase = GamePhase.GameEnd
        player_manager = PlayerManager.get_instance()
        players = player_manager.get_all_players_with_ids()
        for player_id, player in players.items():
            amount = 0
            for possession in player.possessions:
                amount += possession.get_loot_value()
            self.final_score[player_id] = amount

         # find the player with least bullets
        least_bullets_id = ""
        minimum_value = 10
        for player_id, player in players.items():
            if len(player.revolver) < minimum_value:
                minimum_value = len(player.revolver)
                least_bullets_id = player_id

        self.final_score[least_bullets_id] += 1000

    def end_of_card(self, player: Player) -> None:
        """
        This method is some testing after we execute one action card
        """
        # Do the marshal testing
        for train in self.__trains:
            #  marshal can only be inside of the train
            inside = train.get_inside()
            if inside.get_marshal_here():
                for p in inside.get_players():
                    inside.remove_player(p)
                    train.get_roof().add_player(p)
                    p.discard_pile.append(BulletCard(1, Character.Marshall))
                break

        player._waiting_for_input = False
        player.stealin_action = None
        player.available_bandits = []
        player.available_loots = []
        player.available_positions = []
        self.execute_action()
        return

    def get_trains(self) -> List[TrainCar]:
        return self.__trains

    def get_current_turn_index(self) -> int:
        return self.__current_turn_index

    def get_game_state(self, player_id: str) -> dict:
        '''
            this method provides all (hopefully) the information required for the client to draw the UI
        '''
        player_manager = PlayerManager.get_instance()
        player = player_manager.get_player_by_id(player_id)

        '''
         client will know how to draw the train from the trains field,
         train.get_inside().get_players(), /get_loots() will give you what is in that position
         from the player, you can get the bandit to draw through player1.get_bandit()
         from the loot, you can get the loot to draw through loot.get_loot_type()...
        '''
        # game_data is the same for every player
        game_data = {"trains": self.__trains,
                     "current_phase": self.__current_phase,
                     "card_just_played": self.card_just_played,
                     "current_action_card": self.current_action_card,  # this is for stealin
                     "game_end": self.game_end,
                     "final_score": self.final_score,
                     "current_round": self.get_current_round().name,
                     "current_round_index": self.__current_round_index,
                     "current_turn_index": self.__current_turn_index
                     }
        '''
            index gives back the index of the player in the participant list, maybe useful later
        '''
        player_data = {"index": self.__participants.index(player),
                       "hand": player.get_hand(),
                       "revolver": player.revolver,
                       "possessions": player.possessions,
                       "stealin_action": player.stealin_action,
                       "my_turn": player._waiting_for_input,  # every action should be disabled if not his turn
                       "available_bandits": player.available_bandits,
                       "available_loot": player.available_loots,
                       # didn't find a good way to pass the avaiablable loot, so I just passed the object itself
                       # when rendering, if in stealin phase, if my_turn, if stealin_action is rob, then
                       # check if the loot in that position is in the available list
                       "available_position": player.available_positions
                       # the form of available position is [[1,0], [1,0], [0,0], [1,0]] like this
                       # this mean the roof of train with index 0, 1, 3 is available position to choose

                       }
        game_state = {"game_data": game_data, "player_data": player_data}

        return game_state
