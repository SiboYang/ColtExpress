import sys

import pygame
from assets.color_constants import BLUE, LIGHT_BLUE, WHITE
from assets.font_constants import FONT_REG
from assets.game_constants import SCREEN_HEIGHT, SCREEN_WIDTH
from assets.media_constants import *
from extensionGame.bandit import Bandit
from extensionGame.card import Card
from extensionGame.change_floor_button import ChangeFloorButton
from extensionGame.display_final_score import FinalScore
from extensionGame.draw_button import DrawCardButton
from extensionGame.hand import Hand
from extensionGame.indicator import Indicator
from extensionGame.locomotive import Locomotive
from extensionGame.loot import Loot
from extensionGame.marshal import Marshal
from extensionGame.play_card_button import PlayCardButton
from extensionGame.wagon import Wagon
from menus.client_info import Client
from menus.informal_menu_interface import InformalMenuInterface
from server.controller.game import Game
from server.controller.player import Player
from server.controller.player_manager import PlayerManager
from server.enum.ActionKind import ActionKind
from server.enum.Character import Character
from server.enum.GamePhase import GamePhase
from server.enum.LootType import LootType
from server.model.action_card import ActionCard
from extensionGame.SettingsButton import SettingsButton
bandit_hand = {
    Character.Ghost: GHOST_HANDS_BASE,
    Character.Tuco: TUCO_HANDS_BASE,
    Character.Doc: DOC_HANDS_BASE,
    Character.Cheynne: CHEYENNE_HANDS_BASE,
    Character.Belle: BELLE_HANDS_BASE,
    Character.Django: DJANGO_HANDS_BASE,
}
Loot_type = {
    LootType.Purse: "Purse",
    LootType.Ruby: "Jewel",
    LootType.StrongBox: "Strongbox"
}
action_name = {
    ActionKind.Move: "move.png",
    ActionKind.ChangeFloor: "change_floor.png",
    ActionKind.Shoot: "shoot.png",
    ActionKind.Rob: "loot.png",
    ActionKind.Marshal: "marshal.png",
    ActionKind.Punch: "punch.png"
}


class ExtensionGame(InformalMenuInterface):
    def __init__(self):

        self.manager = None
        self.game = None
        self.player1 = None

        self.game_state = None
        self.bandit = []
        self.hands = []
        self.trains = []
        self.bandit_name = []
        self.all_sprites = pygame.sprite.Group()
        self.loots = {}
        self.cards = {}
        self.hand = Hand(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.78), int(SCREEN_WIDTH * 0.5),
                         int(SCREEN_HEIGHT * 0.2), [])
        self.character = None
        self.current_revolver_num = -1
        self.current_revolver = None
        self.latest_card = {}
        self.possessions = {}
        self.current_action_card = {}
        self.marshal_instance = None
        self.client = Client.get_instance()
        self.indicator = []
        self.current_round_num = ""
        self.current_round = None

    def draw_menu(self):
        gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # some initializations for pictures used in game board
        background_img = pygame.image.load(BACKGROUND).convert()
        background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # pause_button = pygame.image.load(PAUSE_BUTTON).convert()
        # pause_button = pygame.transform.scale(pause_button, (int(SCREEN_WIDTH * 0.06), int(SCREEN_HEIGHT * 0.09)))
        # pause_button.set_colorkey(BLACK)

        self.get_game_state()
        # self.test_init()

        locomotive = Locomotive(int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.3), int(SCREEN_WIDTH * 0.2),
                                int(SCREEN_HEIGHT * 0.2))
        self.trains.append(locomotive)
        self.all_sprites.add(locomotive)
        wagon_num = len(self.game_state['game_data']['trains']) - 1
        for i in range(wagon_num):
            wagon = Wagon(int(SCREEN_WIDTH * 0.8) - int(SCREEN_WIDTH * 0.2 * (i + 1)), int(SCREEN_HEIGHT * 0.3),
                          int(SCREEN_WIDTH * 0.2),
                          int(SCREEN_HEIGHT * 0.2))
            self.trains.append(wagon)
            self.all_sprites.add(wagon)

        change_floor_button = ChangeFloorButton(int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.7),
                                                int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.1), BLUE, LIGHT_BLUE)
        draw_card_button = DrawCardButton(int(SCREEN_WIDTH * 0.9), int(SCREEN_HEIGHT * 0.8), int(SCREEN_WIDTH * 0.07),
                                          int(SCREEN_HEIGHT * 0.1), BLUE, LIGHT_BLUE)
        play_card_button = PlayCardButton(int(SCREEN_WIDTH * 0.9), int(SCREEN_HEIGHT * 0.9), int(SCREEN_WIDTH * 0.07),
                                          int(SCREEN_HEIGHT * 0.1), BLUE, LIGHT_BLUE)


        # TODO: fixed indicator blinks problem
        while True:

            # self.test_update()
            self.get_game_state()

            self.draw_trains()
            self.draw_hands()
            self.draw_revolver()
            self.draw_possessions()
            self.clear_indicator()
            self.draw_round_card()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.game_state["game_data"]["game_end"]:
                    return FinalScore(self.game_state["game_data"]["final_score"])
                elif self.game_state["game_data"]["current_phase"] == GamePhase.Schemin:
                    self.draw_played_cards()
                elif self.game_state["game_data"]["current_phase"] == GamePhase.Stealin:
                    self.draw_current_action_cards()

                if self.game_state["player_data"]["my_turn"]:
                    if self.game_state["game_data"]["current_phase"] == GamePhase.Schemin:
                        draw_card_button.clicked(self.hand, self.all_sprites, event, self.player1)
                        play_card_button.clicked(self.hand, self.all_sprites, event, self.cards,
                                                 self.game_state['player_data']['hand'], self.player1)
                    elif self.game_state["game_data"]["current_phase"] == GamePhase.Stealin:
                        action = list(self.current_action_card.keys())[0].action_kind
                        # if action == ActionKind.ChangeFloor:
                        #     change_floor_button.clicked(self.hand, self.all_sprites, event)
                        if action == ActionKind.Move:
                            available_pos = self.game_state["player_data"]["available_position"]
                            for p in available_pos:
                                if p:
                                    bandit = self.bandit[self.bandit_name.index(self.character)]
                                    index = available_pos.index(p)
                                    roof = 0
                                    if bandit.on_roof:
                                        roof = 1
                                    train = self.trains[index]
                                    self.draw_indicator(train.x, train.y, 20)
                                    train.chosen_bandit(bandit, event, index, roof)
                        elif action == ActionKind.Shoot:
                            chosen_b = self.get_chosen_bandit(event)
                            cmd = {'type': "Shoot",
                                   'data': {"bandit": chosen_b}}
                            self.client.send(cmd)
                        elif action == ActionKind.Punch:
                            chosen_b = self.get_chosen_bandit(event)
                            chosen_index = self.get_chosen_index(event)
                            cmd = {'type': "Punch",
                                   'data': {"bandit": chosen_b, "index": chosen_index}}
                            self.client.send(cmd)
                        elif action == ActionKind.Rob:
                            available_loots = self.game_state["player_data"]["available_loot"]
                            for loot in available_loots:
                                for key, val in self.loots.items():
                                    if key == loot:
                                        self.draw_indicator(val.x, val.y, 20)
                                        val.choose_loot(event, loot)
                        elif action == ActionKind.Marshal:
                            available_pos = self.game_state["player_data"]["available_position"]
                            for p in available_pos:
                                if p:
                                    index = available_pos.index(p)
                                    roof = 0
                                    train = self.trains[index]
                                    self.draw_indicator(train.x, train.y, 20)
                                    train.chosen_marshal(self.marshal_instance, event, index, roof)
            gameDisplay.blit(background_img, (0, 0))
            if self.game_state["player_data"]["my_turn"]:
                if self.game_state["game_data"]["current_phase"] == GamePhase.Schemin:
                    draw_card_button.draw(gameDisplay)
                    play_card_button.draw(gameDisplay)
            self.draw_round_and_turn(gameDisplay)
            self.all_sprites.update()
            self.all_sprites.draw(gameDisplay)
            # gameDisplay.blit(pause_button, (int(SCREEN_WIDTH * 0.9), int(SCREEN_HEIGHT * 0.05)))
            pygame.display.update()

    def draw_round_and_turn(self, screen):
        # int(SCREEN_WIDTH * 0.01), int(SCREEN_HEIGHT * 0.01),int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.23)
        cur_round = self.game_state['game_data']["current_round_index"]
        cur_turn = self.game_state['game_data']["current_turn_index"]
        myfont = pygame.font.Font(FONT_REG, 20)
        textsurface_1 = myfont.render("Current Round: " + str(cur_round+1), True, WHITE)
        rect_1 = textsurface_1.get_rect()
        textsurface_2 = myfont.render("Current Turn: " + str(cur_turn+1), True, WHITE)
        rect_2 = textsurface_2.get_rect()
        rect_1.x = int(SCREEN_WIDTH * 0.15)
        rect_1.y = int(SCREEN_WIDTH * 0.03)
        rect_2.x = int(SCREEN_WIDTH * 0.15)
        rect_2.y = int(SCREEN_WIDTH * 0.07)
        screen.blit(textsurface_1, rect_1)
        screen.blit(textsurface_2, rect_2)

    def get_chosen_index(self, event):
        try:
            available_pos = self.game_state["player_data"]["available_position"]
            chosen_index = None
            for p in available_pos:
                if p:
                    index = available_pos.index(p)
                    train = self.trains[index]
                    self.draw_indicator(train.x, train.y, 20)
                    chosen_index = train.punch_pos(event, index)
                    if chosen_index is not None:
                        break
            return chosen_index
        except KeyError:
            print("No available_position key")

    def get_chosen_bandit(self, event):
        try:
            available_bandits = self.game_state["player_data"]["available_bandits"]
            chosen_b = None
            for b in available_bandits:
                index = self.bandit_name.index(b)
                bandit = self.bandit[index]
                self.draw_indicator(bandit.x, bandit.y, 20)
                chosen_b = bandit.choose_bandit(event, b)
                if chosen_b is not None:
                    break
            return chosen_b
        except KeyError:
            print("No available_bandits key")

    def clear_indicator(self):
        for i in self.indicator:
            self.all_sprites.remove(i)
        self.indicator = []

    def draw_indicator(self, x, y, radius):
        circle = Indicator(x, y, radius, radius)
        self.indicator.append(circle)
        self.all_sprites.add(circle)

    def draw_trains(self):
        bandit_dic = {
            Character.Ghost: GHOST_FIGURE,
            Character.Tuco: TUCO_FIGURE,
            Character.Doc: DOC_FIGURE,
            Character.Cheynne: CHEYENNE_FIGURE,
            Character.Belle: BELLE_FIGURE,
            Character.Django: DJANGO_FIGURE,
        }
        if self is not None:
            train_info = self.game_state['game_data']['trains']
            x_last = -1
            for train in train_info:
                index = train_info.index(train)
                board_train = self.trains[index]
                # inside-player
                players = train.get_inside().get_players()
                for player in players:
                    bandit = player.get_bandit()
                    x_offset = int(players.index(player) * 0.05 * SCREEN_WIDTH)
                    if bandit not in self.bandit_name:
                        self.bandit_name.append(bandit)
                        bandit_obj = Bandit(bandit_dic[bandit], board_train.x + x_offset, int(SCREEN_HEIGHT * 0.35),
                                            int(SCREEN_WIDTH * 0.05), int(SCREEN_HEIGHT * 0.07), bandit)
                        self.bandit.append(bandit_obj)
                        self.all_sprites.add(bandit_obj)
                        x_last = bandit_obj.x
                    else:
                        i = self.bandit_name.index(bandit)
                        bandit_obj = self.bandit[i]
                        bandit_obj.change_pos(board_train.x + x_offset, int(SCREEN_HEIGHT * 0.35))
                        x_last = bandit_obj.x

                # roof-player
                players = train.get_roof().get_players()
                for player in players:
                    bandit = player.get_bandit()
                    x_offset = int(players.index(player) * 0.05 * SCREEN_WIDTH)
                    if bandit not in self.bandit_name:
                        self.bandit_name.append(bandit)
                        bandit_obj = Bandit(bandit_dic[bandit], board_train.x + x_offset,
                                            int(SCREEN_HEIGHT * 0.215),
                                            int(SCREEN_WIDTH * 0.05), int(SCREEN_HEIGHT * 0.07), bandit)
                        bandit_obj.set_roof()
                        self.bandit.append(bandit_obj)
                        self.all_sprites.add(bandit_obj)
                    else:
                        i = self.bandit_name.index(bandit)
                        bandit_obj = self.bandit[i]
                        bandit_obj.change_pos(board_train.x + x_offset, int(SCREEN_HEIGHT * 0.215))

                # inside-loots
                loots = train.get_inside().get_loots()
                for loot in loots:
                    x_offset = int(loots.index(loot) * 0.05 * SCREEN_WIDTH)
                    loot_type = loot.get_loot_type()
                    value = loot.get_loot_value()
                    path = LOOTS + Loot_type[loot_type] + "_Back" + ".png"

                    if loot not in self.loots.keys():
                        loot_obj = Loot(path, board_train.x + x_offset, int(SCREEN_HEIGHT * 0.4),
                                        int(SCREEN_WIDTH * 0.03), int(SCREEN_HEIGHT * 0.045), loot_type, value)
                        self.loots[loot] = loot_obj
                        self.all_sprites.add(loot_obj)
                    else:
                        loot_obj = self.loots[loot]
                        loot_obj.change_pos(board_train.x + x_offset, int(SCREEN_HEIGHT * 0.4))
                for i in list(set(self.loots.keys()) - set(loots)):
                    self.all_sprites.remove(self.loots[i])
                    del self.loots[i]

                # inside-marshal
                marshal_here = train.get_inside().get_marshal_here()
                if marshal_here:
                    if self.marshal_instance is None:
                        self.marshal_instance = Marshal(MARSHAL_FIGURE, x_last + board_train.x,
                                                        int(SCREEN_HEIGHT * 0.35),
                                                        int(SCREEN_WIDTH * 0.05), int(SCREEN_HEIGHT * 0.07))
                        self.all_sprites.add(self.marshal_instance)
                    else:
                        self.marshal_instance.change_pos(x_last + board_train.x,
                                                         int(SCREEN_HEIGHT * 0.35))

    def draw_hands(self):
        hands = self.game_state['player_data']['hand']
        if self.character is None:
            self.character = hands[0].character
        base_path = bandit_hand[self.character]
        for hand in hands:
            if hand not in self.cards.keys():
                card = None
                if isinstance(hand, ActionCard):
                    pic_path = action_name[hand.action_kind]
                    tlt_path = base_path + pic_path
                    card = Card(tlt_path, 0, 0, int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.23), True)
                else:
                    pic_path = "bullet_" + str(hand.get_number() + 1) + ".png"
                    tlt_path = base_path + pic_path
                    card = Card(tlt_path, 0, 0, int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.23), False)
                self.hand.add_card(card, self.all_sprites)
                self.cards[hand] = card
        for i in list(set(self.cards.keys()) - set(hands)):
            if self.hand.has_card(self.cards[i]):
                self.hand.remove_card(self.cards[i], self.all_sprites)
                del self.cards[i]
        self.hand.update()

    def draw_revolver(self):
        revolvers = self.game_state['player_data']["revolver"]
        cur = len(revolvers)
        if self.current_revolver_num != cur:
            self.current_revolver_num = cur
            if self.current_revolver is not None:
                self.all_sprites.remove(self.current_revolver)
            if cur != 0:
                path = bandit_hand[self.character] + "bullet_" + str(self.current_revolver_num) + ".png"
                self.current_revolver = Card(path, int(SCREEN_WIDTH * 0.01), int(SCREEN_HEIGHT * 0.78),
                                             int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.23), False)
                self.all_sprites.add(self.current_revolver)

    def draw_round_card(self):
        cur_round = self.game_state['game_data']['current_round']
        path = ROUND_2_4_BASE + cur_round + ".png"
        if self.current_round_num != cur_round:
            self.current_round_num = cur_round
            if self.current_round is not None:
                self.all_sprites.remove(self.current_round)
            self.current_round = Card(path, int(SCREEN_WIDTH * 0.5 - SCREEN_WIDTH * 0.23 / 2),
                                      int(SCREEN_HEIGHT * 0.01),
                                      int(SCREEN_WIDTH * 0.23), int(SCREEN_HEIGHT * 0.2), False)
            self.all_sprites.add(self.current_round)

    def draw_played_cards(self):
        latest_card = self.game_state['game_data']["card_just_played"]
        if latest_card is not None and latest_card not in self.latest_card.keys():
            path = ""
            if self.latest_card != {}:
                self.all_sprites.remove(list(self.latest_card.values())[0])
                del self.latest_card[list(self.latest_card.keys())[0]]
            if latest_card.get_visible():
                path = bandit_hand[latest_card.character] + action_name[latest_card.action_kind]
            else:
                path = BACK_SIDE
            self.latest_card[latest_card] = Card(path, int(SCREEN_WIDTH * 0.01), int(SCREEN_HEIGHT * 0.01),
                                                 int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.23), False)
            self.all_sprites.add(self.latest_card[latest_card])

    def draw_current_action_cards(self):
        card = self.game_state["game_data"]["current_action_card"]
        if card is not None and card not in self.current_action_card.keys():
            if self.current_action_card != {}:
                self.all_sprites.remove(list(self.current_action_card.values())[0])
                del self.current_action_card[list(self.current_action_card.keys())[0]]
            path = bandit_hand[card.character] + action_name[card.action_kind]
            self.current_action_card[card] = Card(path, int(SCREEN_WIDTH * 0.01), int(SCREEN_HEIGHT * 0.01),
                                                  int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.23), False)
            self.all_sprites.add(self.current_action_card[card])

    def draw_possessions(self):
        possessions = self.game_state["player_data"]["possessions"]
        for p in possessions:
            x_offset = int(possessions.index(p) * 0.05 * SCREEN_WIDTH)
            loot_type = p.get_loot_type()
            value = p.get_loot_value()
            path = LOOTS + Loot_type[loot_type] + "_" + str(value) + ".png"
            if p not in self.possessions.keys():
                x = 0
                if len(self.possessions.values()) == 0:
                    x = int(SCREEN_WIDTH * 0.12)
                else:
                    x = list(self.possessions.values())[-1].x + x_offset
                loot_obj = Loot(path, x, int(SCREEN_HEIGHT * 0.95),
                                int(SCREEN_WIDTH * 0.02), int(SCREEN_HEIGHT * 0.045), loot_type, value)
                self.possessions[p] = loot_obj
                self.all_sprites.add(loot_obj)
        for i in list(set(self.possessions.keys()) - set(possessions)):
            self.all_sprites.remove(self.possessions[i])
            del self.possessions[i]

    def get_game_state(self):
        print("Getting game state...")
        game_state = False
        while not game_state:
            payload = self.client.receive_data()
            try:
                if payload['type'] == 'game_state':
                    game_state = True
                    self.game_state = payload['data']
            except KeyError:
                print("No data in following payload")
                print(payload)

    def test_init(self):
        self.manager = PlayerManager()
        self.manager.add_player(Player(), "1")
        # self.manager.add_player(Player(), "2")
        # self.manager.add_player(Player(), "3")
        # three players in game manager
        self.player1 = self.manager.get_player_by_id("1")
        # player2 = self.manager.get_player_by_id("2")
        # player3 = self.manager.get_player_by_id("3")
        self.game = Game.get_instance()
        self.game.choose_bandit(Character.Tuco, "1")
        # self.game.choose_bandit(Character.Doc, "2")
        # self.game.choose_bandit(Character.Belle, "3")
        self.game_state = self.game.get_game_state("1")

    def test_update(self):
        self.game_state = self.game.get_game_state("1")