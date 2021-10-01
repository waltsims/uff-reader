from typing import List

import numpy as np
import h5py
from uff.utils import *
from src.uff import *
import inspect
from uff.uff_io import Serializable
from debug_h5_dict import traverse


def init_obj_from_param_list(class_name: str, params: dict):
    class_ = globals()[class_name]
    obj_params = list(class_.__annotations__)
    return class_(**instantiate_args(obj_params, params))


def instantiate_list(real_list, class_name):
    # List of type title
    for idx, l in enumerate(real_list):
        assert isinstance(l, dict), f"Unrecognized list entry {l}"
        real_list[idx] = init_obj_from_param_list(class_name, l)
    return real_list


def str_indexed_list2regular_list(parameter, object_dictionary):
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

    return instantiate_list(real_list, title)


def instantiate_args(object_parameters: list, args_dict: dict) -> dict:
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
                    args_dict[parameter] = str_indexed_list2regular_list(parameter, arg)

                elif parameter == 'version':
                    if is_version_compatible(arg, (0, 3, 0)):
                        print("good version")

                else:
                    # TODO: fix the naming/ definition of aperture. Either position or origin
                    if parameter == "aperture":
                        arg['position'] = arg.pop('origin')

                    obj_params = [*inspect.signature(globals()[object_name]).parameters]
                    args_dict[parameter] = globals()[object_name](**instantiate_args(obj_params, arg))

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

if __name__ == '__main__':
    test_dict = load_dict_from_hdf5('/Users/faridyagubbayli/Work/fieldII_converging_wave_mlt_sector.uff')
    uff = traverse(test_dict)

    test_dict = load_dict_from_hdf5('/Users/faridyagubbayli/Work/fieldII_converging_wave_mlt_sector.uff')
    uff_dict = strip_prefix_from_keys(old_dict=test_dict, prefix="uff.")

    for k, v in uff_dict.items():
        if k == 'version':
            assert is_version_compatible(v, (0, 3, 0))
            print("good version")
            continue
        cls = Serializable.get_subcls_with_name(k)
        out = cls.deserialize(v)
        print('Does outputs match:', out == uff.channel_data)

    # print(out)

# print(uff_dict)
# filepath = '/private/var/folders/wd/pzn3h1fn37s6gbt12tyj50gw0000gn/T/example_output.h5'
# uff_h5 = h5py.File(filepath)
# test_dict = load_dict_from_hdf5(filepath)

# traverse(test_dict)
# print(test_dict)


