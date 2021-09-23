from dataclasses import dataclass
from typing import List

from uff.position import Position


@dataclass
class Perimeter:
    """Describes the geometry of an ultrasonic element."""
    position: List[Position]
