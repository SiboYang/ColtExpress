from server.enum.LootType import LootType
from server.model.position import Position


class Loot():
    def __init__(self, type: LootType, value: int):
        self.__type = type
        self.__value = value

    def get_loot_type(self) -> LootType:
        return self.__type

    def get_loot_value(self) -> int:
        return self.__value

    def set_position(self, old_position: Position, new_position: Position) -> None:
        if old_position != None:
            old_position.remove_loot(self)
        new_position.add_loot(self)
