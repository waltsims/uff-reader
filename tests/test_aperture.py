from uff import Aperture
from uff import Position


def test_instantiation():
    p1 = Position(0, 0, 0)
    Aperture(origin=p1, window='Hamming', f_number=1, fixed_size=1)
    pass
