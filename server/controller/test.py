from server.controller.game import Game
from server.controller.player import Player
from server.controller.player_manager import PlayerManager
from server.enum.Character import Character

manager = PlayerManager()
manager.add_player(Player(), "1")
manager.add_player(Player(), "2")
manager.add_player(Player(), "3")
# three players in game manager
player1 = manager.get_player_by_id("1")
player2 = manager.get_player_by_id("2")
player3 = manager.get_player_by_id("3")

game = Game.get_instance()
game.choose_bandit(Character.Tuco, "1")
game.choose_bandit(Character.Doc, "2")
game.choose_bandit(Character.Belle, "3")
state = game.get_game_state("1")
player1.play_card_at_pos(0)
player2.play_card_at_pos(0)
player3.play_card_at_pos(0)
player1.play_card_at_pos(0)
player2.play_card_at_pos(0)
player3.play_card_at_pos(0)
player1.play_card_at_pos(0)
player2.play_card_at_pos(0)
player3.play_card_at_pos(0)
player1.play_card_at_pos(0)
player2.play_card_at_pos(0)
player3.play_card_at_pos(0)

# first round over

state1 = game.get_game_state("1")
player1.choose_shoot_target(Character.Doc)
state1 = game.get_game_state("1")
state2 = game.get_game_state("2")
player2.choose_shoot_target(Character.Tuco)

print("Over")
