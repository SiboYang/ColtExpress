from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from server.model.loot import Loot
    from server.controller.player import Player
    from server.model.train_car import TrainCar
    from server.model.loot import Loot


class Position:
    def __init__(self, roof: bool, train: TrainCar):
        self.__roof: bool = roof
        self.__loots: List[Loot] = []
        self.__players: List[Player] = []
        self.__train: TrainCar = train
        self.__marshal_here: bool = False

    def is_roof(self) -> bool:
        return self.__roof

    def add_loot(self, loot: Loot) -> None:
        self.__loots.append(loot)

    def remove_loot(self, loot: Loot) -> None:
        self.__loots.remove(loot)

    def add_player(self, player: Player) -> None:
        self.__players.append(player)

    def remove_player(self, player: Player) -> None:
        self.__players.remove(player)

    def get_players(self) -> List[Player]:
        return self.__players

    def get_loots(self) -> List[Loot]:
        return self.__loots

    def set_marshal_here(self, marshal: bool) -> None:
        self.__marshal_here = marshal

    def get_marshal_here(self) -> bool:
        return self.__marshal_here
