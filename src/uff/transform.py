from typing import ClassVar

from attrs import define

from uff.rotation import Rotation
from uff.position import Position
from uff.translation import Translation


@define
class Transform:
    """Specifies a 3D affine transformation of rotation plus translation,
    IN THAT ORDER, where the translation is done on the unrotated
    coordinate system. The direction is given by local coordinate
    system of the object that owns this object.

    Attributes
    ==========
    translation: 	change in position in meters
    rotation: 	    change in rotation in radians
    """

    _str_name: ClassVar = "transform"

    translation: Translation
    rotation: Rotation

    def __call__(self, point):
        if isinstance(point, Position):
            return self.translation(self.rotation(point))

        raise TypeError(f"Type {type(point)} not recognized.")
