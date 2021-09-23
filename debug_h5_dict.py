import numpy as np
import h5py
from src.uff import *
import inspect


def save_dict_to_hdf5(dic, filename):
    """
    ....
    """
    with h5py.File(filename, 'w') as h5file:
        recursively_save_dict_contents_to_group(h5file, '/', dic)


def recursively_save_dict_contents_to_group(h5file, path, dic):
    """
    ....
    """
    for key, item in dic.items():

        if isinstance(item, (np.ndarray, np.int64, np.float64, str, bytes)):
            h5file[path + key] = item
        elif isinstance(item, dict):
            recursively_save_dict_contents_to_group(h5file, path + key + '/', item)
        else:
            raise ValueError('Cannot save %s type' % type(item))


def load_dict_from_hdf5(filename):
    """
    ....
    """
    with h5py.File(filename, 'r') as h5file:
        return recursively_load_dict_contents_from_group(h5file, '/')


def decode_from_hdf5(item):
    """
    Decode an item from HDF5 format to python type.

    This currently just converts __none__ to None and some arrays to lists

    .. versionadded:: 1.0.0

    Parameters
    ----------
    item: object
        Item to be decoded

    Returns
    -------
    output: object
        Converted input item
    """
    if isinstance(item, str) and item == "__none__":
        output = None
    elif isinstance(item, bytes) and item == b"__none__":
        output = None
    elif isinstance(item, (bytes, bytearray)):
        output = item.decode()
    elif isinstance(item, np.ndarray):
        if item.size == 0:
            output = item
        elif item.size == 1:
            output = item.item()
        elif str(item.dtype).startswith('|S') or isinstance(item[0], bytes):
            output = "".join(np.char.decode([i[0] for i in item]))
            # if str(item.dtype).startswith('|S'):
            #     ans[key] = item.fillvalue.decode('utf-8')
            # elif str(item.dtype).startswith('>f'):
            #     ans[key] = float(item.fillvalue)
            # elif str(item.dtype).startswith('>u'):
            #     ans[key] = int(item.fillvalue)
            # else:
            #     raise NotImplementedError(f"Could not Do not handle {item.dtype}")
            #  output = [it.decode() for it in item]
        else:
            output = item
    elif isinstance(item, np.bool_):
        output = bool(item)
    else:
        output = item
    return output


def recursively_load_dict_contents_from_group(h5file, path):
    """
    ....
    """
    ans = {}
    for key, item in h5file[path].items():
        if isinstance(item, h5py._hl.dataset.Dataset):
            ans[key] = decode_from_hdf5(item[()])

        elif isinstance(item, h5py._hl.group.Group):
            ans[key] = recursively_load_dict_contents_from_group(h5file, path + key + '/')
    return ans


uff_h5 = h5py.File("out.h5")


def strip_prefix_from_keys(old_dict: dict, prefix: str):
    new_dict = {}
    for key in old_dict.keys():
        old_key = key
        if prefix in key:
            new_key = old_key.lstrip(prefix)
        else:
            new_key = old_key
        new_dict[new_key] = old_dict[old_key]
    return new_dict


def snake_to_camel_case(snake_str: str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component
    # with the 'title' method and join them together.
    return ''.join(x.title() for x in components)


def is_fake_list(obeject_dictionary):
    # fake list is dictionary with numerical strings as keys
    return all(type(key) == str and key.isdecimal() for key in obeject_dictionary.keys())


def is_sequence(object_dictionary):
    # key has sequence and number in it
    return all(type(key) == str and 'sequence' in key for key in object_dictionary.keys())


def instantiate_list(real_list, title):
    # List of type title
    for idx, l in enumerate(real_list):
        if type(l) == dict:
            object_parameters = [*inspect.signature(globals()[title]).parameters]
            real_list[idx] = globals()[title](**instantiate_args(object_parameters, l))
        # Object name is singular capitalized parameter name
        else:
            raise ValueError(f"Unrecognized list entry {l}")

    return real_list


def fake_list_to_list(parameter, object_dictionary):
    # list of values in fake dictionary if key equals index
    # - 1 because keys start with one
    real_list = [value for ind, (key, value) in enumerate(object_dictionary.items()) if int(key) - 1 == ind]
    if snake_to_camel_case(parameter) in globals().keys():
        title = snake_to_camel_case(parameter)
        # TODO: Aperture doesn't define origin type.
    elif parameter == 'probes':
        # TODO: this is not conform to the standard
        # probe is a list of probes of length 1
        title = parameter.title()[:-1]
    elif parameter == 'sequence':
        title = 'TimedEvent'
    elif parameter == 'unique_events':
        title = 'Event'
    elif parameter == 'element_impulse_response':
        title = 'ImpulseResponse'
    elif parameter == 'unique_excitations':
        title = 'Excitation'
    elif parameter == 'unique_waves':
        title = 'Wave'
    elif parameter == 'transmit_waves':
        title = 'TransmitWave'
    else:
        raise ValueError(f"What am I? {parameter}")

    return instantiate_list(real_list, title)


def version_is_compatible(version: dict) -> bool:
    # return bool(version['major'] == float(UFF.__version_info__[0]) and
    #             version['minor'] == float(uff.__version_info__[1]) and
    #             version['patch'] == float(uff.__version_info__[2]))
    return bool(version['major'] == 0 and
                version['minor'] == 3 and
                version['patch'] == 0)

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
                if is_fake_list(arg):
                    # print(f"Found fake list for parameter {parameter}")
                    # real_list = fake_list_to_list(object_name, arg)
                    # args_dict[parameter] = instantiate_list(real_list, object_name)
                    args_dict[parameter] = fake_list_to_list(parameter, arg)

                elif parameter == 'version':
                    if version_is_compatible(arg):
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


# TODO traverse to bottom until value is not dict
def traverse(uff_dict: dict):
    uff_parameters = UFF().__dict__.keys()
    # strip off uff prefix
    uff_dict = strip_prefix_from_keys(old_dict=uff_dict, prefix="uff.")
    args = instantiate_args(uff_parameters, uff_dict)
    uff = UFF()
    uff.__dict__ = args

    # If val not dict
    # If key correct ObjectType ==> instatiate object
    # Elif check if string is index
    # cast str to int
    # add to dict of objects key int position and  value object
    # Else raise Error
    # return object
    # Else recursive call of dict
    # traverse dict
    pass


test_dict = load_dict_from_hdf5('/Users/faridyagubbayli/Work/fieldII_converging_wave_mlt_sector.uff')
# filepath = '/private/var/folders/wd/pzn3h1fn37s6gbt12tyj50gw0000gn/T/example_output.h5'
# uff_h5 = h5py.File(filepath)
# test_dict = load_dict_from_hdf5(filepath)



traverse(test_dict)
print(test_dict)


# if type object type,
# if key == 'translation':
#     Translation(**value)


#+=======+++++++++++++++++++++++++++++++++++
from datetime import datetime

n_elem = 32
Nx, Ny, Nz = 128, 128, 16
elem_width = 1
elem_spacing = 0
elem_length = 12
elem_pitch = elem_width + elem_spacing
transducer_width = n_elem * elem_width + (n_elem - 1) * elem_spacing
dt = 1.9481e-08     # in seconds

elem_x = 1e-3 * elem_pitch * np.linspace(-n_elem // 2, n_elem//2) - (elem_width // 2)
elem_y = np.zeros(n_elem)
elem_z = np.zeros(n_elem)

source_strength = 1e6
tone_burst_freq = 1.5e6
tone_burst_cycles = 1

eg = ElementGeometry(Perimeter([Position(1, 1, 1)]))
# ir = ImpulseResponse(0, 10, [1, 1, 1], '[m]')

elements = []
for elem_idx in range(n_elem):
    T = Translation(elem_x[elem_idx], elem_y[elem_idx], elem_z[elem_idx])
    R = Rotation(0, 0, 0)
    elem_transform = Transform(T, R)
    elem = Element(elem_transform, eg)
    elements.append(elem)



probe_T = Translation(1, Ny // 2 - transducer_width // 2, Nz // 2 - elem_length // 2)
probe_R = Rotation(0, 0, 0)
probe_transform = Transform(probe_T, probe_R)

probe = Probe(
    number_elements=32,
    pitch=1,
    element_height=12,
    element_width=1,
    element=elements,
    transform=probe_transform,
    element_geometry=eg
)

dt_string = datetime.now().isoformat()



transmit_waves = [TransmitWave(
    wave=1,
    time_zero_reference_point=TimeZeroReferencePoint(0, 0, 0)
)]


transmit_setup = TransmitSetup(
    probe=1,
    transmit_waves=transmit_waves,
    channel_mapping=[[i for i in range(n_elem)]],
    sampling_frequency=1/dt
)

receive_setup = ReceiveSetup(
    probe=1,
    time_offset=-100 * dt,
    channel_mapping=[[i for i in range(n_elem)]],
    sampling_frequency=1/dt
)

us_event = Event(
    transmit_setup=transmit_setup,
    receive_setup=receive_setup
)

seq = TimedEvent(
    event=us_event,
    time_offset=0,
)

unique_waves = [Wave(
    origin=Origin(
        position=Position(),
        rotation=Rotation()
    ),
    wave_type=WaveType.PLANE,
    aperture=Aperture(
        position=Position(),
        fixed_size=0,
        f_number=1.0,
        window='rectwin'
    ),
    excitation=1
)]

unique_events = [us_event]

unique_excitations = [Excitation(
    pulse_shape='sinusoidal',
    waveform=np.ones(10).tolist(),  # => np.delay_mask
    sampling_frequency=1/dt
)]

ChannelData(
    probes=[probe],
    sound_speed=1540,
    local_time=dt_string,
    country_code='DE',
    repetition_rate=(1 / tone_burst_freq),
    authors="Some random guy",
    description="Lorem ipsum si amet ... as always ;)",
    system="Whatever system it is ...",
    data=test_dict['p'],
    sequence=seq,
    unique_waves=unique_waves,
    unique_events=unique_events,
    unique_excitations=unique_excitations
)
