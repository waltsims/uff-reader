from typing import ClassVar, Union

from attrs import define

from uff.position import Position
from uff.rotation import Rotation


@define
class WaveOriginSpherical:
    """UFF class to describe origin of a spherical wave

    Attributes:
    position: Location of the center of the spherical wave
    """

    _str_name: ClassVar = "wave_origin.spherical"

    position: Position = Position()


@define
class WaveOriginPlane:
    """UFF class to describe origin of a plane wave

    Attributes
    ==========
    rotation: Rotation of the wave relative to the direction [0 0 1]
    """

    _str_name: ClassVar = "wave_origin.plane"

    rotation: Rotation = Rotation()


@define
class WaveOriginCylindrical:
    """UFF class to describe origin of a cylindrical wave, as those typically used in wor-column addressed arrays.

    Attributes
    ==========
    position: 2-element vector of uff.position defining the line that originates the wave
    """

    _str_name: ClassVar = "wave_origin.cylindrical"

    position: Position = Position()


@define
class WaveOriginPhotoacoustic:
    """UFF class to describe the origin of a photoacoustic wave.

    Attributes
    ==========
    None
    """

    _str_name: ClassVar = "wave_origin.photoacoustic"


# TODO: when loading origin, how to know what type of origin is being loaded?
# @define
# class WaveOrigin:
# """
# UFF class to describe the origin of a wave. This is a superclass. Depending on the wave type the hdf5 file will hold a different format, namely:
# uff.wave_origin.spherical
# uff.wave_origin.plane
# uff.wave_origin.cylindrical
# uff.wave_origin.photoacoustic
# """
# _str_name: ClassVar = "origin"

WaveOrigin = Union[
    WaveOriginPlane, WaveOriginCylindrical, WaveOriginSpherical, WaveOriginPhotoacoustic
]
