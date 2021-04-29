from dataclasses import dataclass
from uff.rotation import Rotation


@dataclass
class PlaneWaveOrigin():
    rotation: Rotation = Rotation()
