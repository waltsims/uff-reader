from typing import ClassVar, List

from attrs import define

from uff.position import Position


@define
class Perimeter:
    """Describes the geometry of an ultrasonic element.

    Attributes:
    position: List of positions
    """

    _str_name: ClassVar = "perimeter"

    position: List[Position]
