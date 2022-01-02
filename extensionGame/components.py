from abc import ABC, abstractmethod


# an abstract class for components in game board
class Components(ABC):
    @abstractmethod
    def __init__(self, x: int, y: int, width: int, height: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self):
        """
        Get the x coord of the component
        """
        return self._x

    @x.setter
    def x(self, x: int):
        self._x = x

    @property
    def y(self):
        """
        Get the y coord of the component
        """
        return self._y

    @y.setter
    def y(self, y: int):
        self._y = y

    @property
    def width(self):
        """
        Get the width coord of the component
        """
        return self._width

    @width.setter
    def width(self, width: int):
        self._width = width

    @property
    def height(self):
        """
        Get the height coord of the component
        """
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height
