from dataclasses import dataclass
from uff.event import Event
from uff.uff_io import Serializable


@dataclass
class TimedEvent(Serializable):
    """
    UFF class to describe a TR/RX event transmitted at a given moment in time.

    Attributes:
    event (int):            Index of the uff.event within the list of unique_events in the uff.channel_data structure
    time_offset (float):    Time offset relative to start of the sequence repetition (frame) [s]

    """
    event: int
    time_offset: float

    def serialize(self):
        assert isinstance(self.event, int), 'TimedEvent.event should be index of the uff.event.'
        return super().serialize()

    @staticmethod
    def str_name():
        return 'sequence'

    def __eq__(self, other):
        return super().__eq__(other)
