from typing import ClassVar, Optional
from enum import IntEnum

from attrs import define

from uff.aperture import Aperture
from uff.wave_origin import WaveOrigin


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

    converging = 0
    diverging = 1
    plane = 2
    cylindrical = 3
    photoacoustic = 4


@define
class Wave:
    """
    UFF class to describe the geometry of a transmitted wave or beam.

    TODO: custom deserialization code to check WaveType, then load
    the corresponding WaveOrigin

    Attributes:
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
