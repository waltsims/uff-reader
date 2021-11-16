from dataclasses import dataclass

from uff.uff_io import Serializable


@dataclass
class Translation(Serializable):
    """Define a translation operation in a 3D Cartesian system"""
    x: float
    y: float
    z: float

    @staticmethod
    def str_name():
        return 'translation'
