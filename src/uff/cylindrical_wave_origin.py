from dataclasses import dataclass
from uff.origin import Origin
from uff.position import Position


@dataclass
class CylindricalWaveOrigin(Origin):
    position: Position = Position()

