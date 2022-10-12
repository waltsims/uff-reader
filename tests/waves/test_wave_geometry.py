from uff import Aperture, Position, Wave, WaveType, WaveOriginPlane, WaveOriginSpherical


def test_converging_wave():
    # Single convering wave

    # Geometric origin
    aperture = Aperture(
        window="hanning", origin=Position(), f_number=2.1, fixed_size=[12e-3]
    )

    wo = WaveOriginSpherical()
    wt = WaveType.CONVERGING
    wave = Wave(aperture=aperture, origin=wo, wave_type=wt)
    assert isinstance(wave.wave_type, WaveOriginSpherical)


def test_diverging_wave():
    # Single divergin wave

    # Geometric origin
    aperture = Aperture(
        window="hanning", origin=Position(), f_number=2.1, fixed_size=12e-3
    )

    wo = WaveOriginSpherical()
    wt = WaveType.DIVERGING
    wave = Wave(aperture=aperture, origin=wo, wave_type=wt)
    assert isinstance(wave.wave_type, WaveOriginSpherical)


def test_plane_wave():
    # Single divergin wave

    # Geometric origin
    aperture = Aperture(
        window="hanning", origin=Position(), f_number=2.1, fixed_size=12e-3
    )

    wo = WaveOriginPlane()
    wt = WaveType.DIVERGING
    wave = Wave(aperture=aperture, origin=wo, wave_type=wt)
    assert isinstance(wave.wave_type, WaveOriginPlane)
