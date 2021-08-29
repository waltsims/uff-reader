from dataclasses import dataclass
from uff.event import Event


@dataclass
class TimedEvent:
    """
    UFF class to describe a TR/RX event transmitted at a given moment in time.

    Attributes:
    event (int):            Index of the uff.event within the list of unique_events in the uff.channel_data structure
    time_offset (float):    Time offset relative to start of the sequence repetition (frame) [s]

    """
    event: Event
    time_offset: float
