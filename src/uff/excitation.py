from typing import ClassVar

from attrs import define

from numpy.typing import NDArray


@define
class Excitation:
    """
    Describes the excitation applied to an element.

    Attributes:
    pulse_shape: String describing the pulse shape (e.g., sinusoidal, square wave, chirp),
        including necessary parameters
    waveform: Vector containing the sampled excitation waveform [normalized units]
    sampling_frequency: Scalar containing the sampling frequency of the excitation waveform [Hz]
    """

    _str_name: ClassVar = "unique_excitations"

    pulse_shape: str
    waveform: NDArray
    sampling_frequency: float
