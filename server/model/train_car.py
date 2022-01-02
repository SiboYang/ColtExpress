
from server.model.position import Position

class TrainCar:

    def __init__(self, locomotive: bool):
        self.__locomotive = locomotive
        self._inside = Position(False, self)
        self._roof = Position(True, self)
    
    def get_inside(self) -> Position:
        return self._inside
    
    def get_roof(self) -> Position:
        return self._roof
