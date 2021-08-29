from dataclasses import dataclass
from uff.rotation import Rotation
from uff.position import Position


@dataclass
# TODO: saved as origin but defined as wave origin in spec
# TODO: when loading origin, how to know what type of origin is being loaded?
class Origin:
    rotation: Rotation = Rotation()
    position: Position = Position()
    pass

