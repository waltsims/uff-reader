from uff import *
import numpy as np

from uff import Rotation


def test_linear_scan_focused_beam():
    N_waves = 16
    x0 = np.linspace(-20e-3, 20e-3, N_waves)
    focal_depth = 20e-3

    waves = []

    for wave_idx in range(N_waves):
        p = Position(x=x0[wave_idx], y=focal_depth)
        a = Aperture(f_number=1, fixed_size=[40e-3, 12e-3], origin=Position())
        waves.append(Wave(origin=p, aperture=a, wave_type=WaveType.CONVERGING))

    # TODO: add plot and visualization functionality (should be excluded from tests


def test_plane_wave_sequence():
    N_waves = 11
    angle_span = 30 * np.pi / 180

    angles = np.linspace(-0.5 * angle_span, 0.5 * angle_span, N_waves)

    waves = []

    for wave_idx in range(N_waves):
        a: Aperture = Aperture(fixed_size=[40e-3, 12e-3], origin=Position(), window='hamming')
        origin = PlaneWaveOrigin(rotation=Rotation(y=angles[wave_idx]))
        waves.append(Wave(origin=origin, aperture=a, wave_type=WaveType.PLANE))
