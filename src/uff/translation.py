from typing import ClassVar

from attrs import define

from uff.position import Position


@define
class Translation:
    """Define a translation operation in a 3D Cartesian system

    Attributes
    ==========
    x: x coordinate in meters
    y: coordinate in meters
    z: z coordinate in meters
    """

    _str_name: ClassVar = "translation"

    x: float
    y: float
    z: float

    def __call__(self, pos):
        return Position(x=pos.x + self.x, y=pos.y + self.y, z=pos.z + self.z)
