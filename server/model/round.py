from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from server.enum.TurnType import TurnType
    from server.enum.EndOfRoundEvent import EndOfRoundEvent
    from server.model.action_card import ActionCard

class Round:
    def __init__(self, turns: List[TurnType], end_round_event: EndOfRoundEvent, name: str):  # turns is a list of turn types
        self.__turns: List[TurnType] = turns
        self.card_played: List[ActionCard] = []
        self.end_round_event: EndOfRoundEvent = end_round_event
        self.name = name
    def get_num_of_turns(self) -> int:
        return len(self.__turns)

    def get_turn_type(self, turn_index: int) -> TurnType:
        return self.__turns[turn_index]

