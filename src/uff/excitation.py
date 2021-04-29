from dataclasses import dataclass 


@dataclass
class Excitation:
    """
    Describes the excitation applied to an element. 

    Attributes:
        pulse_shape (str): 	            String describing the pulse shape (e.g., sinusoidal, square wave, chirp),
                                        including necessary parameters
        waveform (float):               Vector containing the sampled excitation waveform [normalized units]
        sampling_frequency (float): 	Scalar conatining the sampling frequency of the excitation waveform [Hz]
    """
    pulse_shape:str
    waveform:float
    sampling_frequency:float
    
