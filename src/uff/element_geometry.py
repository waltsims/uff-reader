from typing import ClassVar
from attrs import define

from uff.perimeter import Perimeter


@define
class ElementGeometry:
    """Describes the geometry of an ultrasonic element.

    Notes: Here we assume that the acoustic center of the element is at origin O = (0; 0; 0) pointing towards Z = (0;
    0; 1). The element shape is defined by a closed perimeter contained within the XY -plane, that is in turn
    composed of an ordered set of uff.position instances.
    """

    _str_name: ClassVar = "element_geometry"

    perimeter: Perimeter
