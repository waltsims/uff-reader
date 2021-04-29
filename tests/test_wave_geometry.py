from uff.position import Position
from uff.wave_type import WaveType
from uff.aperture import Aperture
from uff.position import Position
from uff.wave import Wave
from uff.spherical_wave_origin import SphericalWaveOrigin
from uff.plane_wave_origin import PlaneWaveOrigin


#TODO: make test class here?
#def test_wave_geometry();
def test_converging_wave():
    # Single convering wave

    # Geometric origin
    aperture = Aperture(window='hanning',
                        origin = Position(),
                        f_number = 2.1,
                        fixed_size=12e-3)

    wo = SphericalWaveOrigin()
    p = Position(x=20e-3, y=0, z=50e-3)
    wt = WaveType.CONVERGING
    wave = Wave(aperture=aperture, origin=wo, wave_type=wt)

def test_diverging_wave():
    # Single divergin wave

    # Geometric origin
    aperture = Aperture(window='hanning',
                        origin = Position(),
                        f_number = 2.1,
                        fixed_size=12e-3)

    wo = SphericalWaveOrigin()
    p = Position(x=20e-3, y=0, z=50e-3)
    wt = WaveType.DIVERGING
    wave = Wave(aperture=aperture, origin=wo, wave_type=wt)

def test_plane_wave():
    # Single divergin wave

    # Geometric origin
    aperture = Aperture(window='hanning',
                        origin = Position(),
                        f_number = 2.1,
                        fixed_size=12e-3)

    wo = PlaneWaveOrigin()
    p = Position(x=20e-3, y=0, z=50e-3)
    wt = WaveType.DIVERGING
    wave = Wave(aperture=aperture, origin=wo, wave_type=wt)
