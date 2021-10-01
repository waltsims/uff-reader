from dataclasses import dataclass
from uff.rotation import Rotation
from uff.origin import Origin


@dataclass
class PlaneWaveOrigin(Origin):
    rotation: Rotation = Rotation()

    def __eq__(self, other):
        return super().__eq__(other)
