import uff
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

    # TODO: add plot and visualization functionality (should be excluded from tests)


def test_plane_wave_sequence():
    n_waves = 11
    angle_span = 30 * np.pi / 180

    angles = np.linspace(-0.5 * angle_span, 0.5 * angle_span, n_waves)

    waves = []

    for wave_idx in range(n_waves):
        a = Aperture(fixed_size=[40e-3, 12e-3], origin=Position(), window='hamming')
        origin = PlaneWaveOrigin(rotation=Rotation(y=angles[wave_idx]))
        waves.append(Wave(origin=origin, aperture=a, wave_type=WaveType.PLANE))


def test_sector_scan_diverging_beams():
    n_waves = 5
    azimuth = np.linspace(-np.pi / 6, np.pi / 6, n_waves)
    virtual_source_distance = 20e-3

    waves = []

    for angle in azimuth:
        w = Wave(origin=SphericalWaveOrigin(
            position=Position(x=virtual_source_distance * np.sin(angle), z=-virtual_source_distance * np.cos(angle))),
            wave_type=WaveType.DIVERGING, aperture=Aperture(window='rectwin', origin=Position(), fixed_size=[18e-3, 12e-3]))

        waves.append(w)
    pass


def test_sector_scan_focus_beams():
    n_waves = 16
    azimuth = np.linspace(-np.pi / 6, np.pi / 6, n_waves)
    focal_depth = 70e-3

    waves = []

    for angle in azimuth:
        w = Wave(origin=SphericalWaveOrigin(
            position=Position(x=focal_depth * np.sin(angle), z=focal_depth * np.cos(angle))),
            wave_type=WaveType.CONVERGING, aperture=Aperture(window='rectwin', origin=Position(), fixed_size=[18e-3, 12e-3]))

        waves.append(w)
    pass


    pass


def test_scan_mlt():
    n_waves = 70  # Number of unique beams in the sequence
    n_mlt = 2  # Number of Multi-Line Transmots (i.e. beams in the same transmit event)
    focal_depth = 0.06  # Transmit focal depth [m]
    angle_span = 70 * np.pi / 180  # Sector opening [rad]
    angles = np.linspace(-0.5 * angle_span, 0.5 * angle_span, n_waves)

    waves = []
    for angle in angles:
        x_pos = focal_depth * np.cos(angle)
        y_pos = focal_depth * np.sin(angle)
        p: Position = Position(y=y_pos, x=x_pos)
        origin = SphericalWaveOrigin(position=p)
        a: Aperture = Aperture(fixed_size=[16e-3, 12e-3], origin=Position(), window='Tukey(0.5)')
        waves.append(Wave(origin=origin, aperture=a, wave_type=WaveType.CONVERGING))

    events = []
    # Merge two beams into each event
    for i in range(int(n_waves / n_mlt)):
        for wave_n in range(n_mlt):
            tw = TransmitWave(time_zero_reference_point=0, wave=waves[int(i + wave_n * n_waves / n_mlt)])
            # TODO: currently many Nones passed since all arguments are required. Fix by setting default parameters.
            ts = TransmitSetup('transmit_waves', [tw], channel_mapping=None, sampled_delays=None,
                               sampled_excitations=None, sampling_frequency=None, transmit_voltage=None)
            # TODO: currently many Nones passed since all arguments are required. Fix by setting default parameters.
            rs = ReceiveSetup(probe=None, time_offset=None, channel_mapping=None, sampling_frequency=None,
                              tgc_profile=None, tgc_sampling_frequency=None, modulation_frequency=None)
            events.append(Event(transmit_setup=ts, receive_setup=rs))

    pass
