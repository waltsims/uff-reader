from dataclasses import dataclass
from uff.wave_origin import WaveOrigin
from uff.position import Position

@dataclass
class SphericalWaveOrigin(WaveOrigin):
    position: Position = Position()

