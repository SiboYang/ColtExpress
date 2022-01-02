from server.enum.Character import Character
from server.model.card import Card


class BulletCard(Card):
    # num represents the number of bullet this card represent
    def __init__(self, num: int, character: Character):
        super().__init__(character, False)
        self.__number = num

    def get_number(self) -> int:
        return self.__number
