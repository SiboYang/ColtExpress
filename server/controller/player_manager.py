from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from server.controller.player import Player
    from server.enum.Character import Character



class PlayerManager:
    __instance = None


    @staticmethod
    def get_instance() -> PlayerManager:
        """ Static access method. """
        if PlayerManager.__instance == None:
            PlayerManager()
        return PlayerManager.__instance
        # here I assume we have some way to get a unique ID for each player, maybe IP address or something?
    def add_player(self, player: Player, player_id: str) -> None:
        self.__players[player_id] = player

    def get_player_by_id(self, player_id: str) -> Player:
        return self.__players[player_id]

    def get_all_players(self) -> List[Player]:
        return list(self.__players.values())

    def get_all_players_with_ids(self) -> Dict[str, Player]:
        return self.__players

    def get_player_by_character(self, character: Character) -> Player:
        for (key, value) in self.__players.items():
            if value.get_bandit() == character:
                return value

    def __init__(self):
        if PlayerManager.__instance != None:
            raise Exception("PlayerManager is a singleton!")
        else:
            self.__players = {}
            PlayerManager.__instance = self
