from uff.transform import Transform
from uff.translation import Translation
from uff.rotation import Rotation
from uff.element import Element
from uff.element_geometry import ElementGeometry
from uff.impulse_response import ImpulseResponse
from uff.impulse_response import ImpulseResponse
from uff.perimeter import Perimeter 
from uff.element_geometry import ElementGeometry 
from uff.position import Position
from uff.probe import Probe


def test_instatiation():
    t = Translation(1,1,1)
    r = Rotation(0,0,0)
    tt = Transform(t, r)
    eg = ElementGeometry(Perimeter([Position(1,1,1)])) 
    ir = ImpulseResponse(0,10,[1,1,1],'[m]') 
    e = Element(tt, eg, ir)
    p = Probe(transform=tt, element=e,element_impulse_response=[ir] )

