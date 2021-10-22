import numpy as np
import h5py


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


def snake_to_camel_case(snake_str: str) -> str:
    """
        Convert `snake` pattern to `camel` pattern
    Args:
        snake_str: String in `snake` pattern

    Returns:
        String in `camel` pattern
    """
    components = snake_str.split('_')
    # Capitalize the first letter of each component with the 'title' method
    components = [x.title() for x in components]
    return ''.join(components)


def save_dict_to_hdf5(dic, filename):
    """
    ....
    """
    with h5py.File(filename, 'w') as h5file:
        _recursively_save_dict_contents_to_group(h5file, '/', dic)


def _recursively_save_dict_contents_to_group(h5file, path, dic):
    """
        argument => Tuple(data: dict, attrs: dict)
    ....
    """
    BASIC_DATATYPES = (np.ndarray, np.int64, np.float64, bytes, int, float)

    for key, item in dic.items():
        if isinstance(item, str):
            # Strings will be stored as list of lists where each element is a byte character
            h5file[path + key] = [[c.encode()] for c in list(item)]
        elif isinstance(item, BASIC_DATATYPES):
            # Primitive types stored directly
            h5file[path + key] = item
        elif isinstance(item, dict):
            _recursively_save_dict_contents_to_group(h5file, path + key + '/', item)
            if is_keys_str_decimals(item):
                h5file[path + key].attrs['array_size'] = len(item.keys())
            if path + key == '/uff.channel_data/probes/00000001':
                h5file[path + key].attrs['probe_type'] = 'uff.probe.linear_array'
        else:
            raise ValueError(f'Cannot save {type(item)} type')


def load_dict_from_hdf5(filename):
    """
    ....
    """
    with h5py.File(filename, 'r') as h5file:
        return _recursively_load_dict_contents_from_group(h5file, '/')


def _recursively_load_dict_contents_from_group(h5file, path):
    """
    ....
    """
    ans = {}
    for key, item in h5file[path].items():
        if isinstance(item, h5py._hl.dataset.Dataset):
            ans[key] = _decode_from_hdf5(item[()])

        elif isinstance(item, h5py._hl.group.Group):
            ans[key] = _recursively_load_dict_contents_from_group(h5file, path + key + '/')
    return ans


def _decode_from_hdf5(item):
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
    is_none_str     = isinstance(item, str) and item == "__none__"
    is_none_byte    = isinstance(item, bytes) and item == b"__none__"
    is_byte_arr     = isinstance(item, (bytes, bytearray))
    is_ndarray      = isinstance(item, np.ndarray)
    is_bool         = isinstance(item, np.bool_)

    if is_none_str or is_none_byte:
        output = None
    elif is_byte_arr:
        output = item.decode()
    elif is_ndarray :
        if item.size == 0:
            output = item
        elif item.size == 1:
            output = item.item()
        elif str(item.dtype).startswith('|S') or isinstance(item[0], bytes):
            output = "".join(np.char.decode([i[0] for i in item]))
        else:
            output = item
    elif is_bool:
        output = bool(item)
    else:
        output = item
    return output


def is_keys_str_decimals(dictionary: dict):
    """
        Checks if the keys are string decimals
    Args:
        dictionary: Dictionary object to check

    Returns:
        True if keys are numerical strings
    """
    keys = dictionary.keys()
    are_decimals = [type(k) == str and k.isdecimal() for k in keys]
    return all(are_decimals)


def is_keys_contain(dictionary: dict, substr: str = 'sequence'):
    keys = dictionary.keys()
    are_containing = [type(k) == str and substr in k for k in keys]
    return all(are_containing)


def is_version_compatible(version: dict, expected_version: tuple) -> bool:
    """

    Args:
        version: Dictionary containing version info.
                    Should have following fields -> 'major', 'minor', 'patch'
        expected_version: Tuple of 3 elements for ('major', 'minor', 'patch')

    Returns:
        Whether the version is the same as the expected version
    """
    # return bool(version['major'] == float(UFF.__version_info__[0]) and
    #             version['minor'] == float(uff.__version_info__[1]) and
    #             version['patch'] == float(uff.__version_info__[2]))
    major, minor, patch = expected_version
    return bool(version['major'] == major and
                version['minor'] == minor and
                version['patch'] == patch)
