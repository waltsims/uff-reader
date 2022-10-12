from typing import ClassVar, List, Optional

from attrs import define

from uff.element import Element
from uff.element_geometry import ElementGeometry
from uff.impulse_response import ImpulseResponse
from uff.transform import Transform

__all__ = ("Probe", "LinearArray", "CurvilinearArray", "MatrixArray")


@define
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

    _str_name: ClassVar = "probe"

    # def serialize(self):
    # assert self.element_geometry is None or isinstance(self.element_geometry, list), \
    # 'Probe.element_geometry should be a list of element geometries!'
    # return super().serialize()

    transform: Transform
    # TODO for conformity call `elements`
    element: List[Element]
    focal_length: Optional[float] = None
    element_impulse_response: Optional[List[ImpulseResponse]] = None
    element_geometry: Optional[List[ElementGeometry]] = None

    # TODO: These parameters are not defined in the standard
    number_elements: int = 0
    pitch: float = 0
    element_height: float = 0
    element_width: float = 0


class LinearArray(Probe):
    """
    Describes a linear array, made of identical elements, uniformly distributed on a line.

    Attributes:
    number_elements: Number of elements in the array
    pitch: Distance between the acoustic ceneter of adyacent elements [m]
    element_width: (Optional) Element size in the x-axis [m]
    element_height: (Optional) Element size in the y-axis [m]
    """

    _str_name: ClassVar = "probe.linear_array"

    number_elements: int
    pitch: float
    element_width: Optional[float]
    element_height: Optional[float]


class CurvilinearArray(Probe):
    """
    Describes a linear array, made of identical elements, uniformly distributed on a line.

    Attributes:
    number_elements: Number of elements in the array
    pitch: Distance between the acoustic ceneter of adyacent elements [m]
    radius: Radius of curvature of the curvilinear probe [m]
    element_width: (Optional) Element size in the x-axis [m]
    element_height: (Optional) Element size in the y-axis [m]
    """

    _str_name: ClassVar = "probe.curvilinear_array"

    number_elements: int
    pitch: float
    radius: float
    element_width: Optional[float] = None
    element_height: Optional[float] = None


class MatrixArray(Probe):
    """
    Describes a matrix array, made of identical elements, uniformly distributed on a 2D grid.

    Attributes:
    number_elements_x: of elements in the x-axis
    pitch_x: Distance between the acoustic center of adjacent elements along the x-axis [m]
    number_elements_y: of elements in the y-axis
    pitch_y: Distance between the acoustic center of adjacent elements along the y-axis [m]
    element_width: (Optional) Element size in the x-axis [m]
    element_height: (Optional) Element size in the y-axis [m]
    """

    _str_name: ClassVar = "probe.matrix_array"

    number_elements_x: int
    number_elements_y: int
    pitch_x: float
    pitch_y: float
    element_width: Optional[float] = None
    element_height: Optional[float] = None
