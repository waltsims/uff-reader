from dataclasses import dataclass
from uff.position import Position


@dataclass
class Perimeter:
    """Describes the geometry of an ultrasonic element."""
    position: list[Position]
