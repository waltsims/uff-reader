from dataclasses import dataclass
from uff.rotation import Rotation
from uff.wave_origin import WaveOrigin


@dataclass
class PlaneWaveOrigin(WaveOrigin):
    rotation: Rotation = Rotation()
