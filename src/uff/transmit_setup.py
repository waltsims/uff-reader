from typing import ClassVar, List, Optional
from attrs import define

from uff.transmit_wave import TransmitWave


@define
class TransmitSetup:
    """
    UFF class to describe the transmit event (probe/channels, waves, excitations, etc.).

    Attributes
    ==========
    probe: Index of the uff.probe used for transmit within the list of probes in
        the uff.channel_data structure
    transmit_waves: List of transmit waves used in this event with their respective
        time offset and weight
    channel_mapping: Map of transmit channels to transducer elements
    sampled_delays: (Optional) Transmit delay as set in the system for active channels [s].
    sampled_excitations: (Optional) Matrix of sampled excitation waveforms [normalized units].
    sampling_frequency : (Optional) Sampling frequency of the excitation waveforms [Hz]
    transmit_voltage: (Optional) Peak amplitude of the pulse generator [V]
    """

    _str_name: ClassVar = "transmit_setup"

    probe: int
    transmit_waves: List[TransmitWave]
    channel_mapping: List[int]
    sampled_delays: Optional[float] = None
    sampled_excitations: Optional[float] = None
    sampling_frequency: Optional[float] = None
    transmit_voltage: Optional[float] = None
