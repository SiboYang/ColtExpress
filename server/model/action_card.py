from server.enum.ActionKind import ActionKind
from server.enum.Character import Character
from server.model.card import Card


class ActionCard(Card):
    def __init__(self, action_kind: ActionKind, character: Character):
        super().__init__(character, True)
        self.action_kind = action_kind
