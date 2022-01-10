from uff.translation import Translation
from uff.rotation import Rotation
from uff.transform import Transform
from uff.position import Position
import numpy as np
from scipy.spatial.transform.rotation import Rotation as R


def test_translate_position():
    point = Position(x=1, y=2, z=3)
    trans = Translation(x=-5, y=10, z=-17)
    new_point = trans(point)
    assert new_point == Position(x=-4, y=12, z=-14)


def test_rotation_position():
    rot1 = R.from_euler('xyz', [50, 60, 90], degrees=False)
    point = Position(x=1, y=2, z=3)
    point1 = Position(*rot1.apply(np.array(point)))
    rot2 = Rotation(50, 60, 90)
    point2 = rot2(point)
    assert point1 == point2


def test_transform_position():
    point = Position(x=1, y=2, z=3)
    rot = Rotation(50, 60, 90)
    trans = Translation(x=-5, y=10, z=-17)
    tr = Transform(rotation=rot, translation=trans)
    x = tr(point)
    point1 = Position(*rot(point))
    y = trans(point1)
    assert x == y
