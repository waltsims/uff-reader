from typing import ClassVar, Optional
from enum import IntEnum

from attrs import define

from uff.aperture import Aperture
from uff.wave_origin import WaveOrigin, WaveOriginPlane, WaveOriginPhotoacoustic, WaveOriginCylindrical, WaveOriginSpherical


class WaveType(IntEnum):
    """wave_type
    enumerated type (uint32) (
        converging = 0,
        diverging = 1,
        plane = 2,
        cylindrical = 3,
        photoacoustic = 4,
        default = 0
    )
    """

    CONVERGING = 0
    DIVERGING = 1
    PLANE = 2
    CYLINDRICAL = 3
    PHOTOACOUSTIC = 4
    DEFAULT = 0


@define
class Wave:
    """
    UFF class to describe the geometry of a transmitted wave or beam.

    TODO: custom deserialization code to check WaveType, then load
    the corresponding WaveOrigin

    Attributes
    ==========
    origin: Geometric origin of the wave.
    type: enumerated type (int)
        (converging = 0,
        diverging = 1,
        plane = 2,
        cylindrical = 3,
        photoacoustic = 4,
        default = 0)
    aperture: Description of the aperture used to produce the wave
    excitation: (Optional) index to the unique excitation in the parent group
    """

    _str_name: ClassVar = "unique_waves"

    origin: WaveOrigin
    wave_type: WaveType
    aperture: Aperture
    excitation: Optional[int] = None

    def __init__(self, origin, wave_type, aperture, excitation = None):
        match (wave_type):
            case WaveType.PLANE:
                origin = WaveOriginPlane(**origin)
            case WaveType.CYLINDRICAL:
                origin = WaveOriginCylindrical(**origin)
            case WaveType.CONVERGING:
                origin = WaveOriginSpherical(**origin)
            case WaveType.DIVERGING:
                origin = WaveOriginSpherical(**origin)
            case WaveType.PHOTOACOUSTIC:
                origin = WaveOriginPhotoacoustic()

        self.origin = origin
        self.wave_type = wave_type
        self.aperture = Aperture(**aperture)
        self.excitation = excitation

