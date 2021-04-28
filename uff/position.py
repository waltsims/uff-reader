from dataclasses import  dataclass


@dataclass
class Position:
    """Contains a location in space in Cartesian coordinates and SI units."""
    x: float
    y: float
    z: float

    def __add__(self, p2):
        self.x += p2.x
        self.y += p2.y
        self.z += p2.z
        return self
