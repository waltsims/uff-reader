from typing import ClassVar, Optional

from attrs import define

from numpy.typing import NDArray


@define
class ImpulseResponse:
    """Specifies a temporal impulse response

    Attributes:
    initial_time: Time in seconds from the delta excitation until the acquisition of the first sample
    sampling_frequency: Sampling frequency in Hz
    data: Collection of samples containing the impulse response
    units: (Optional) Name of the units of the impulse response
    """

    _str_name: ClassVar = "element_impulse_response"

    initial_time: float
    sampling_frequency: float
    data: NDArray
    units: Optional[str]
