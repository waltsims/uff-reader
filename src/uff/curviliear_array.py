from dataclasses import dataclass
from probe import Probe


@dataclass
class CurvilinearArray(Probe):
    """
    Describes a linear array, made of identical elements, uniformly distributed on a line.

    Attributes:
        number_elements (int): 	Number of elements in the array
        pitch (float): 	 	    Distance between the acoustic ceneter of adyacent elements [m]
        radius (float):
        element_width (float):	(Optional) Element size in the x-axis [m]
        element_height (float):	(Optional) Element size in the y-axis [m]
    """

    number_elements: int
    pitch: float
    radius: float
    element_width: float = None
    element_height: float = None

    def __eq__(self, other):
        return super().__eq__(other)

    # def __eq__(self, other):
    #     if not super().__eq__(other):
    #         return False
    #
    #     return self.number_elements == other.number_elements and \
    #            self.pitch and other.pitch and \
    #            self.radius and other.radius and \
    #            self.element_width and other.element_width and \
    #            self.element_height and other.element_height
