from uff.aperture import Aperture
from uff.position import Position


def test_instatiation():
    p1=Position(0,0,0)
    Aperture(origin=p1, window='Hamming', f_number=1, fixed_size=1)
    pass

