from dataclasses import  dataclass
from uff.uff_io import Serializable


@dataclass
class Position(Serializable):
    """Contains a location in space in Cartesian coordinates and SI units."""
    x: float = 0
    y: float = 0
    z: float = 0

    def __add__(self, p2):
        self.x += p2.x
        self.y += p2.y
        self.z += p2.z
        return self

    @staticmethod
    def str_name():
        return 'position'

    def __eq__(self, other):
        return super().__eq__(other)
