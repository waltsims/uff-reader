from dataclasses import dataclass 
from probe import Probe


@dataclass
class LinearArray(Probe):
    """
    Describes a linear array, made of identical elements, uniformly distributed on a line.

    Attributes:
        number_elements (int): 	Number of elements in the array
        pitch (float): 	 	    Distance between the acoustic ceneter of adyacent elements [m]
        element_width (float): 	(Optional) Element size in the x-axis [m]
        element_height (float):	(Optional) Element size in the y-axis [m]
    """

    number_elements:int
    pitch:float
    element_width:float
    element_height:float

    def __eq__(self, other):
        return super().__eq__(other)
