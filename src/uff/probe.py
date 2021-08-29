from dataclasses import dataclass 
from uff.transform import Transform
from uff.element import Element
from uff.element_geometry import ElementGeometry
from uff.impulse_response import ImpulseResponse


@dataclass
class Probe:
    """
    Describes an generic ultrsound probe formed by a collection of elements.

    Note:

    Where focal_length specifies the lens focusing distance. Note that the 
    elements in element_geometry and impulse_response are referred by the 
    fields inside each member in element, avoiding unnecessary replication 
    of information.

    More compact, although less general, descriptions are available for:

        uff.probe.linear_array,
        uff.probe.curvilinear_array, and
        uff.probe.matrix_array.
    """

    # >> TODO: These parameters are not defined in the standard
    number_elements: int
    pitch: float
    element_height: float
    element_width: float
    element_geometry: list[ElementGeometry]
    ##  <<
    transform: Transform
    element: list[Element]
    element_impulse_response: list[ImpulseResponse]
    focal_length: float = None



