from dataclasses import dataclass
from uff.position import Position
from uff.time_zero_reference_point import TimeZeroReferencePoint
from uff.wave import Wave


@dataclass
class TransmitWave:
    """
    UFF class to describe a transmitted wave as used in an event. 

    Attributes:
        TODO: clarify weather type int or type wave is correct!
        wave now (Wave) was (int):           	            	Index of the uff.wave within the list of unique_waves
                                                in the uff.channel_data structure
        time_zero_reference_point (Position): 	Point in space that the waveform passes through at time zero.
        time_offset	(float):                 	(Optional) Time delay between the start of the event and the 
                                                moment this wave reaches the time_zero_reference_point in the
                                                corresponding transmit setup [s]. [Default = 0s]
        weight 	(float):                     	(Optional) Weight applied to the wave within the event 
                                                [unitless between -1 and +1]. This may be used to describe 
                                                pulse inversion sequences. [Default = 1]
    """
    wave: Wave
    # TODO: should be of type position but current dynamic instantiation does not allow for that.
    time_zero_reference_point: TimeZeroReferencePoint #Position
    time_offset: float = 0
    weight: float = 1
