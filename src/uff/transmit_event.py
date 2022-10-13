from typing import ClassVar
from attrs import define


@define
class TransmitEvent:
    """
    UFF class to describe a TR/RX event transmitted at a given moment in time.

    TODO: I cannot find this in the UFF documentation.

    Attributes
    ==========
    event: Index of the uff.event within the list of unique_events in the 
        uff.channel_data structure
    time_offset: Time offset relative to start of the sequence repetition (frame) [s]
    """

    _str_name: ClassVar = "transmit_event"

    event: int
    time_offset: float
