import abc
import copy
import inspect

import h5py
# from src.uff import *
from uff import ChannelData
from uff.uff_io import Serializable
from uff.utils import *


# TODO: best to instatiate with dictionary, since h5py also creates dictionary of data from h5 file...
class UFF(Serializable):

    # TODO: @classmethod for from file construction
    def __init__(self):
        self.channel_data:ChannelData = None
        self.event = None
        self.timed_event = None
        self.transmit_setup = None
        self.receive_setup = None
        self.transmit_wave = None
        self.excitation = None
        self.wave = None
        self.aperture = None
        self.probe = None
        self.element = None
        self.element_geometry = None
        self.impulse_response = None
        self.perimeter = None
        self.transform = None
        self.rotation = None
        self.translation = None
        self.version = None

    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __deepcopy__(self, memodict={}):
        pass

    @staticmethod
    def str_name():
        return "UFF"

    @classmethod
    def deserialize(cls: object, data: dict):
        obj = UFF()
        primitives = (np.ndarray, np.int64, np.float64, str, bytes, int, float)

        for k, v in data.items():
            if isinstance(v, primitives):
                setattr(obj, k, v)
                continue
            assert isinstance(v, dict), f'{type(v)} did not pass type-assertion'

            property_cls = Serializable.get_subcls_with_name(k)

            if not is_keys_str_decimals(v):
                setattr(obj, k, property_cls.deserialize(v))
            else:
                # TODO: assert keys are correct => ascending order starting from 000001
                list_of_objs = list(v.values())
                list_of_objs = [property_cls.deserialize(item) for item in list_of_objs]
                setattr(obj, k, list_of_objs)

        return obj

    @staticmethod
    def check_version(uff_h5):
        if uff_h5['version']:
            # read uff version
            file_version = uff_h5['version/major'], uff_h5['version/minor'], uff_h5['version/patch']
            package_version = uff.__version_info__
            if file_version == package_version:
                raise ValueError(
                    f"The file version given ({'.'.join(str(i) for i in file_version)})does not have a matching version. Version must be {uff.__version__}")
        else:
            raise Exception("Not a valid uff file. UFF version field is missing")

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
        real_list = [value for ind, (key, value) in enumerate(object_dictionary.items()) if int(key) - 1 == ind]
        if snake_to_camel_case(parameter) in globals().keys():
            title = snake_to_camel_case(parameter)
            # TODO: Aperture doesn't define origin type.
        else:
            # TODO: when parameter == 'probes' => this is not conform to the standard

            param_title_map = {
                'probes'                      : 'Probe',
                'sequence'                    : 'TimedEvent',
                'unique_events'               : 'Event',
                'element_impulse_response'    : 'ImpulseResponse',
                'unique_excitations'          : 'Excitation',
                'unique_waves'                : 'Wave',
                'transmit_waves'              : 'TransmitWave',
            }
            assert parameter in param_title_map, f"What am I? {parameter}"

            title = param_title_map[parameter]

        return self._instantiate_list(real_list, title)

    def _instantiate_args(self, object_parameters: list, args_dict: dict) -> dict:
        # TODO: fix saved name from type to wave_type in standard
        if 'type' in args_dict.keys():
            args_dict['wave_type'] = args_dict.pop('type')
        for parameter, arg in args_dict.items():
            # TODO: if key is an object get object name
            # TODO: if val is dict instantiate args
            # TODO: if key is fake list correct it.
            # TODO: if val is dict instantiate args
            if parameter in object_parameters:
                object_name = snake_to_camel_case(parameter)
                if type(arg) == dict:
                    # identify "fake list" dictionaries and convert to list.
                    if is_keys_str_decimals(arg):
                        # print(f"Found fake list for parameter {parameter}")
                        # real_list = str_indexed_list2regular_list(object_name, arg)
                        # args_dict[parameter] = instantiate_list(real_list, object_name)
                        args_dict[parameter] = self.str_indexed_list2regular_list(parameter, arg)

                    elif parameter == 'version':
                        if is_version_compatible(arg, (0, 3, 0)):
                            print("good version")

                    else:
                        # TODO: fix the naming/ definition of aperture. Either position or origin
                        if parameter == "aperture":
                            arg['position'] = arg.pop('origin')

                        obj_params = [*inspect.signature(globals()[object_name]).parameters]
                        args_dict[parameter] = globals()[object_name](**self._instantiate_args(obj_params, arg))

                # args = instantiate_args(object, args)
                # globals()[object_name](**args)
                # TODO: return args dict for uff
            elif type(arg) == dict:
                # print(f"found parameter {parameter} with argument: {arg}")
                pass
                # else:
                #     raise RuntimeError("I didn't know what to do")
            else:
                # value already assigned
                raise ValueError(f"{parameter} not found in object parameters {object_parameters}")
                pass

        return args_dict

    def load(self, data_path):
        # get uff version number
        uff_dict = load_dict_from_hdf5(data_path)
        # self.check_version(uff_dict)

        uff_parameters = vars(UFF()).keys()
        # strip off uff prefix
        uff_dict = strip_prefix_from_keys(old_dict=uff_dict, prefix="uff.")
        args = self._instantiate_args(uff_parameters, uff_dict)
        self.__dict__ = args

        # # Default group for the parent object.
        # classname = 'uff.channel_data'
        #
        # if classname in uff_h5.keys():
        #     self.timed_event = 0
        #
        #     uff_h5[classname]
        #     # TODO: search subsequent keys and match to objects
        #     # TODO: if object exists, create it.
        #
        #     # TODO: should objects be created with dictionaries of agruments.. yes **dict
        #
        #     pass

    pass

    def save(self, output_uff_path:str, version=None):
        if not output_uff_path.endswith('.uff'):
            output_uff_path += '.uff'

        serialized = self.serialize()
        if version is not None:
            serialized['version'] = version
        serialized['uff.channel_data'] = serialized.pop('channel_data')
        save_dict_to_hdf5(serialized, output_uff_path)

def save(self, data_path, root_name):
    # Saves UFF object to disk

    # TODO: check if file already exists at path

    # TODO: prompt to overwrite previously written file

    # TODO: figure out how to only save channel data for now since that is what the standard defines.

    # TODO: set default "root_name" if one is not passed (name of object) (uff.channel.data)

    # TODO: only read hdf5. screw urls and databases
    # TODO: still check if url is passed.... ugh

    # TODO: write version number

    # TODO: start the (non-recursive) writing process.

    pass

    @property
    def ll_defined(self):
        ll_defined = True;
        if self.ll_open_fun is None:
            ll_defined = False
        return ll_defined
