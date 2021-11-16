from dataclasses import dataclass

from uff.uff_io import Serializable


@dataclass
class Rotation(Serializable):
    """Contains a rotation in space in spherical coordinates and SI units.
    The rotation is specified using Euler angles that are applied in the order ZYX."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @staticmethod
    def str_name():
        return 'rotation'
