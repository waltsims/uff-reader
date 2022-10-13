from typing import ClassVar, List, Optional

from attrs import define

from uff.position import Position


@define
class Aperture:
    """
    UFF class to define analytically the aperture use in an ultrasound wave.

    Notes
    =====
    The class aperture defines the transmit apodization profile. In this case
    origin defines the center of the aperture. The size of the aperture can
    be described with fixed_size, or with f_number in which case the aperture
    size is d/f_number where d is the distance between uff.wave.origin and
    uff.wave.aperture.origin. The parameter window is a string describing
    the apodization window.

    Attributes
    ==========
    origin: Location of the aperture center in space.
    window: String defining the apodization window type and parameter
        (e.g., 'Hamming', 'Gauss(8)', 'Tukey(0.5)')
    f_number: Desired F-number of the aperture [Az, El]
    fixed_size: If non-zero, this overwrites the size of the aperture
        in [m] [Az, El]
    minimun_size: (Optional) If non-zero, this sets a limit for the minimum
        dynamic aperture in m [Az, El]
    maximum_size: (Optional) If non-zero, this sets a limit for the maximum
        dynamic aperture in m [Az, El]
    """

    _str_name: ClassVar = "aperture"

    # @classmethod
    # def deserialize(cls: object, data: dict):
    #     data['position'] = data.pop('origin')
    #     return super().deserialize(data)

    # TODO: standard has this named aperture but defined as position
    origin: Position
    # TODO: what should fixed size type be? list? float? how do you reproduce the same functionality
    fixed_size: List[float]
    window: str = "Hamming"
    f_number: float = 1.0
    minimum_size: Optional[float] = None
    maximum_size: Optional[float] = None
