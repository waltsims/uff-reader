from typing import ClassVar
from attrs import define


@define
class Position:
    """Contains a location in space in Cartesian coordinates and SI units.

    Attributes
    ==========
    x: x coordinate in meters
    y: y coordinate in meters
    z: z coordinate in meters
    """

    _str_name: ClassVar = "position"

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __len__(self):
        return 3

    def __add__(self, p2):
        if isinstance(p2, Position):
            return Position(x=p2.x + self.x, y=p2.y + self.y, z=p2.z + self.z)
        return Position(x=p2 + self.x, y=p2 + self.y, z=p2 + self.z)

    def __sub__(self, p2):
        if isinstance(p2, Position):
            return Position(x=p2.x - self.x, y=p2.y - self.y, z=p2.z - self.z)
        return Position(x=self.x - p2, y=self.y - p2, z=self.z - p2)

    def __truediv__(self, p2):
        if isinstance(p2, Position):
            return Position(x=self.x / p2.x, y=self.y / p2.y, z=self.z / p2.z)
        return Position(x=self.x / p2, y=self.y / p2, z=self.z / p2)

    def __mul__(self, p2):
        if isinstance(p2, Position):
            return Position(x=p2.x * self.x, y=p2.y * self.y, z=p2.z * self.z)
        return Position(x=p2 * self.x, y=p2 * self.y, z=p2 * self.z)

    def __floordiv__(self, p2):
        if isinstance(p2, Position):
            return Position(x=self.x // p2.x, y=self.y // p2.y, z=self.z // p2.z)
        return Position(x=self.x // p2, y=self.y // p2, z=self.z // p2)

    def __pow__(self, other):
        return Position(x=self.x**other, y=self.y**other, z=self.z**other)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        else:
            raise IndexError(f"Index {item} out of bounds for type {__name__}")
