from typing import ClassVar, Optional
from attrs import define

from numpy.typing import NDArray


@define
class ReceiveSetup:
    """
    Describes the setup used to receive and sample data. If more than one probe is used in reception, this is a list
    of setups.

    Notes: The channel_mapping specifies the connection of system channels to transducer elements. The map is a
    M-by-N matrix (HDF5 dimension ordering), where N is the number of system channels and M is the maximum number of
    elements connected to a single channel. In most common cases, M=1. An unconnected state is marked by the value 0.

    Attributes:
    probe: Index of the uff.probe used in reception within the list of probes in the uff.channel_data structure
    time_offset: Time delay between the event start and the acquisition of the first sample [s]
    channel_mapping: Map of receive channels to transducer elements
    sampling_frequency: Sampling frequency of the recorded channel data [Hz]
    tgc_profile: Analog TGC profile sampled at tgc_sampling_frequency [dB]
    tgc_sampling_frequency: (Optional) Sampling frequency of the TGC profile [Hz]
    modulation_frequency: (Optional) Modulation frequency used in case of IQ-data [Hz]

    """

    _str_name: ClassVar = "receive_setup"

    probe: int
    time_offset: float
    channel_mapping: NDArray
    sampling_frequency: float
    tgc_profile: Optional[NDArray]
    tgc_sampling_frequency: Optional[float]
    modulation_frequency: Optional[float]
