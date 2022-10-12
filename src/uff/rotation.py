from typing import ClassVar

from attrs import define
from scipy.spatial.transform import Rotation as R
import numpy as np

from uff.position import Position


@define
class Rotation:
    """Contains a rotation in space in spherical coordinates and SI units.
    The rotation is specified using Euler angles that are applied in the order ZYX.

    Attributes:
    x: rotation around the X-axis in radians
    y: rotation around the Y-axis in radians
    z: rotation around the Z-axis in radians
    """

    _str_name: ClassVar = "rotation"

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __call__(self, pos):
        # TODO: this may break with new type. Fix
        return Position(*self.rotation_object.apply(np.array(pos)))

    @property
    def matrix(self):
        return R.from_euler("xyz", [self.x, self.y, self.z], degrees=False).matrix()

    @property
    def rotation_object(self):
        return R.from_euler("xyz", [self.x, self.y, self.z], degrees=False)
