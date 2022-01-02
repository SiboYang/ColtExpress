from enum import Enum, auto


class ActionKind(Enum):
    Move = auto()
    ChangeFloor = auto()
    Shoot = auto()
    Rob = auto()
    Marshal = auto()
    Punch = auto()
    NULL = auto()
