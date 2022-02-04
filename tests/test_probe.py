from uff.element import Element
from uff.element_geometry import ElementGeometry
from uff.impulse_response import ImpulseResponse
from uff.perimeter import Perimeter
from uff.position import Position
from uff.probe import Probe
from uff.rotation import Rotation
from uff.transform import Transform
from uff.translation import Translation


def test_instantiation():
    t = Translation(1, 1, 1)
    r = Rotation(0, 0, 0)
    tt = Transform(t, r)
    eg = ElementGeometry(Perimeter([Position(1, 1, 1)]))
    ir = ImpulseResponse(0, 10, [1, 1, 1], '[m]')
    e = Element(tt, eg, ir)
    p = Probe(transform=tt,
              element=e,
              element_geometry=[eg],
              element_impulse_response=[ir],
              number_elements=128,
              pitch=0,
              element_height=0.15,
              element_width=0.3)


def test_serialization():
    t = Translation(1, 1, 1)
    r = Rotation(0, 0, 0)
    tt = Transform(t, r)
    eg = ElementGeometry(Perimeter([Position(1, 1, 1)]))
    ir = ImpulseResponse(0, 10, [1, 1, 1], '[m]')
    e = Element(tt, eg, ir)
    p = Probe(transform=tt,
              element=e,
              element_geometry=[eg],
              element_impulse_response=[ir],
              number_elements=128,
              pitch=0,
              element_height=0.15,
              element_width=0.3)

    p_ser = p.serialize()
    pass


def test_serialization_with_only_required_args():
    t = Translation(1, 1, 1)
    r = Rotation(0, 0, 0)
    tt = Transform(t, r)
    ir = ImpulseResponse(0, 10, [1, 1, 1], '[m]')
    eg = ElementGeometry(Perimeter([Position(1, 1, 1)]))
    e = Element(tt, eg, ir)
    p = Probe(transform=tt,
              element=e,
              pitch=0)

    p_ser = p.serialize()
    pass
