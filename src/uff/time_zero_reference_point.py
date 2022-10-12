from typing import ClassVar
from uff.position import Position


class TimeZeroReferencePoint(Position):
    """Contains a location in space in Cartesian coordinates and SI units for t0."""

    _str_name: ClassVar = "time_zero_reference_point"
