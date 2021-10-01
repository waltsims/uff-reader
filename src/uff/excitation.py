from dataclasses import dataclass
from typing import List

from uff.uff_io import Serializable


@dataclass
class Excitation(Serializable):
    """
    Describes the excitation applied to an element. 

    Attributes:
        pulse_shape (str): 	            String describing the pulse shape (e.g., sinusoidal, square wave, chirp),
                                        including necessary parameters
        waveform (float):               Vector containing the sampled excitation waveform [normalized units]
        sampling_frequency (float): 	Scalar conatining the sampling frequency of the excitation waveform [Hz]
    """

    @staticmethod
    def str_name():
        return 'unique_excitations'

    pulse_shape:str
    waveform:List[float]
    sampling_frequency:float

    def __eq__(self, other):
        return super().__eq__(other)
