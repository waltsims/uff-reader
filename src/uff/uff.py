from __future__ import annotations
from typing import ClassVar
import warnings

from attrs import define
import numpy as np

import uff
from uff.aperture import Aperture
from uff.channel_data import ChannelData
from uff.element import Element
from uff.element_geometry import ElementGeometry
from uff.event import Event
from uff.excitation import Excitation
from uff.impulse_response import ImpulseResponse
from uff.perimeter import Perimeter
from uff.probe import Probe
from uff.receive_setup import ReceiveSetup
from uff.rotation import Rotation
from uff.timed_event import TimedEvent
from uff.transform import Transform
from uff.translation import Translation
from uff.transmit_setup import TransmitSetup
from uff.transmit_wave import TransmitWave
from uff.utils import (
    is_keys_str_decimals,
    snake_to_camel_case,
    save_dict_to_hdf5,
    load_uff_dict,
)
from uff.wave import Wave


@define
class UFF:
    """
    UFF v0.3

    Data model
    ==========

    The ultrasound sequence data model is designed following an object-oriented programming phylosophy. A common UFF class forms the base of the model, and all other classes inherit from the UFF class. A UFF class may have other UFF classes as members (or properties in MATLAB).

    Reference semantics (known as handle semantics in MATLAB) are applied such that for example a scan sequence may contain the same transmit/receive event multiple times without creating copies of the event. An example use is a color flow map, where each line is acquired multiple times corresponding to repetitions of the same events.

    File type and structure
    =======================

    The HDF5 file type is used to store data and parameters. UFF files have the extension .uff. HDF5 allows information to be described in a hierarchical manner akin to that of a class tree.

    Model mapped on to HDF5
    =======================
    The UFF describes how to store a data set consisting of one or more of channel data, beamformed data, velocity estimates and more including the sequence used to acquire the data. Each of these corresponds to a UFF class and it is the storage of objects of these classes that are defined here.

    It is possible (and the reference code allows) to store UFF objects of other types, e.g., an alternative probe definition, but storing such objects is not defined here, and the reference code provides a warning stating that the resulting file is not compliant.

    The convention in the first release is that an HDF5 group corresponds to an object in the model, and an HDF5 dataset corresponds to scalars and arrays of simple data types (note that a string is considered a simple data type). HDF5 compound datasets are not used in the initial release. A group contains one or more named links that point to other groups or datasets. This models the members (MATLAB: properties) of the class and the link names shall be those of the corresponding class members. It is possible for multiple links to point to the same group or dataset mimicking the reference semantics in OOP.

    For an array of objects, a link with the name of the class member containing the array points to a group that then contains a link to one group for each array element. These links are named sequentially starting from 1 according to the printf conversion specifier "%08d", i.e., the first element in the array is named "00000001" etc.

    An array of a simple data type is stored as a single dataset in the UFF file.

    HDF5 attributes are used as follows: For an object and an array of objects, an attribute named "class" contains a text string that is the fully qualified name of the object's class. For an array of objects, an attribute named "array_size" contains an array of 32-bit unsigned integers describing the array's dimensions.

    For performance optimizations, it is possible to set a flag that specifies that an object ignores handle semantics when writing it to a UFF file and when reading it back. If used wrongly this may cause a difference between the object in memory and the object in the UFF file. The intention is to be used for objects that are only ever referenced from one place, e.g., the position of a transducer element in a transducer array. The value of this flag is written as an attribute of the HDF5 group with attribute name "shared" with an 8-bit unsigned integer value of 0 if reference semantics are to be ignored and 1 if they are to be respected.

    File contents
    =============
    The file contains a root group with multiple links. The link of primary interest for reading the file is named "uff.channel_data" and points to an object of class uff.channel_data.

    Another link is "version" that points to a dataset containing the library version used to write the UFF file. This is stored as a string, and follows the major.minor.patch version numbering scheme.

    The two remaining links are "common_objects" and "common_doubles" that link to groups used for performance optimizations when writing and reading files. Note that initial benchmarks indicated writing times in excess of 1 minute for writing a 1024 element matrix probe (just the probe definition, no channel data) without performance optimizations and a few seconds with optimizations.

    """

    _str_name: ClassVar = "uff"

    channel_data: ChannelData
    event: Event
    timed_event: TimedEvent
    transmit_setup: TransmitSetup
    receive_setup: ReceiveSetup
    transmit_wave: TransmitWave
    excitation: Excitation
    wave: Wave
    aperture: Aperture
    probe: Probe
    element: Element
    element_geometry: ElementGeometry
    impulse_response: ImpulseResponse
    perimeter: Perimeter
    transform: Transform
    rotation: Rotation
    translation: Translation
    version = None

    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __deepcopy__(self, memodict={}):
        pass

    @classmethod
    def deserialize(cls: UFF, data: dict):
        obj = UFF()
        primitives = (np.ndarray, np.int64, np.float64, str, bytes, int, float)

        for k, v in data.items():
            if isinstance(v, primitives):
                setattr(obj, k, v)
                continue
            assert isinstance(v, dict), f"{type(v)} did not pass type-assertion"

            if k != "channel_data":
                warnings.warn(
                    f"\nWarning: The UFF standard specifies how objects of class uff.channel_data are "
                    f"written.\n Although other properties can be saved to the file, they very likely "
                    f"cannot be read back.\n In order to avoid unnecessary crashes, property `uff.{k}` will "
                    f"not be deserialized."
                )
                continue
            else:
                property_cls = ChannelData

            if not is_keys_str_decimals(v):
                setattr(obj, k, property_cls.deserialize(v))
            else:
                # TODO: assert keys are correct => ascending order starting from 000001
                list_of_objs = list(v.values())
                list_of_objs = [property_cls.deserialize(item) for item in list_of_objs]
                setattr(obj, k, list_of_objs)

        return obj

    @classmethod
    def load(cls: object, file_name: str):
        uff_dict = load_uff_dict(file_name)
        return cls.deserialize(uff_dict)

    @staticmethod
    def check_version(uff_h5):
        if uff_h5["version"]:
            # read uff version
            file_version = (
                uff_h5["version/major"],
                uff_h5["version/minor"],
                uff_h5["version/patch"],
            )
            package_version = uff.__version_info__
            if file_version == package_version:
                raise ValueError(
                    f"The file version given ({'.'.join(str(i) for i in file_version)})does not have a matching "
                    f"version. Version must be {uff.__version__} "
                )
        else:
            raise Exception("Not a valid uff file. UFF version field is missing")

    @property
    def summary(self):
        print(
            f"Summary:\n"
            f"\tSystem:\t{self.channel_data.system}\n"
            f"\tAuthors:\t{self.channel_data.authors}\n"
            f"\tCountry:\t{self.channel_data.country_code}\n"
            f"\tLocal Time:\t{self.channel_data.local_time}\n"
            f"\tDescription:\t{self.channel_data.description}\n"
        )

    def _init_obj_from_param_list(self, class_name: str, params: dict):
        class_ = globals()[class_name]
        obj_params = list(class_.__annotations__)
        return class_(**self._instantiate_args(obj_params, params))

    def _instantiate_list(self, real_list, class_name):
        # List of type title
        for idx, l in enumerate(real_list):
            assert isinstance(l, dict), f"Unrecognized list entry {l}"
            real_list[idx] = self._init_obj_from_param_list(class_name, l)
        return real_list

    def _str_indexed_list2regular_list(self, parameter, object_dictionary):
        # list of values in fake dictionary if key equals index - 1 because keys start with one
        real_list = [
            value
            for ind, (key, value) in enumerate(object_dictionary.items())
            if int(key) - 1 == ind
        ]
        if snake_to_camel_case(parameter) in globals().keys():
            title = snake_to_camel_case(parameter)
            # TODO: Aperture doesn't define origin type.
        else:
            # TODO: when parameter == 'probes' => this is not conform to the standard

            param_title_map = {
                "probes": "Probe",
                "sequence": "TimedEvent",
                "unique_events": "Event",
                "element_impulse_response": "ImpulseResponse",
                "unique_excitations": "Excitation",
                "unique_waves": "Wave",
                "transmit_waves": "TransmitWave",
            }
            assert parameter in param_title_map, f"What am I? {parameter}"

            title = param_title_map[parameter]

        return self._instantiate_list(real_list, title)

    def save(self, output_uff_path: str, version=None):
        if not output_uff_path.endswith(".uff"):
            output_uff_path += ".uff"

        serialized = self.serialize()
        if version is not None:
            serialized["version"] = version
        if "channel_data" in serialized:
            serialized["uff.channel_data"] = serialized.pop("channel_data")
        save_dict_to_hdf5(serialized, output_uff_path)
