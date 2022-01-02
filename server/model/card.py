from abc import ABC

from server.enum.Character import Character


class Card(ABC):
    def __init__(self, character: Character, action_card: bool):
        self.character = character
        self.is_action = action_card
        self.__visible = False

    def set_visible(self, visible: bool) -> None:
        self.__visible = visible

    def get_visible(self) -> bool:
        return self.__visible
