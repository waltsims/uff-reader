from dataclasses import dataclass 
from uff.position import Position


@dataclass
class Aperture:
    """
    UFF class to define analytically the aperture use in an ultrasound wave.

    Notes:
    The class aperture defines the transmit apodization profile. In this case 
    origin defines the center of the aperture. The size of the aperture can
    be described with fixed_size, or with f_number in which case the aperture 
    size is d/f_number where d is the distance between uff.wave.origin and 
    uff.wave.aperture.origin. The parameter window is a string describing 
    the apodization window.

    Attributes:
        origin (Position): 	    Location of the aperture center in space.
        window (str): 	        String defining the apodization window type and 
                                parameter (e.g., 'Hamming', 'Gauss(8)', 'Tukey(0.5)')
                            
        f_number (float):	    Desired F-number of the aperture [Az, El]
        fixed_size (float):     If non-zero, this overwrites the size of the aperture 
                                in [m] [Az, El]
        minimun_size (float):   (Optional) If non-zero, this sets a limit for the minimum 
                                dynamic aperture in m [Az, El]
        maximum_size (float): 	(Optional) If non-zero, this sets a limit for the maximum 
                                dynamic aperture in m [Az, El]
    """
    origin: Position
    window: str
    f_number: float
    fixed_size: float
    minimum_size: float = 0
    maximum_size: float = 0
        

    
