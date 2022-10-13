from typing import ClassVar

from pydantic import BaseModel


class TimedEvent(BaseModel):
    """
    UFF class to describe a TR/RX event transmitted at a given moment in time.

    Attributes
    ==========
    event: Index of the uff.event within the list of unique_events in the uff.channel_data structure
    time_offset: Time offset relative to start of the sequence repetition (frame) [s]
    """

    _str_name: ClassVar = "sequence"

    event: int
    time_offset: float
