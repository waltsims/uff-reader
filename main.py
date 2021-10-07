from debug_h5_dict import traverse
from uff.uff_io import Serializable
from uff.utils import *
from uff.uff import UFF


def load_with_previous_code(path):
    test_dict = load_dict_from_hdf5(path)
    uff = traverse(test_dict)
    return uff


def load_uff_dict(path):
    test_dict = load_dict_from_hdf5('/Users/faridyagubbayli/Work/fieldII_converging_wave_mlt_sector.uff')
    uff_dict = strip_prefix_from_keys(old_dict=test_dict, prefix="uff.")
    return uff_dict


if __name__ == '__main__':
    ref_uff_path = '/Users/faridyagubbayli/Work/fieldII_converging_wave_mlt_sector.uff'
    uff_previous = load_with_previous_code(ref_uff_path)

    uff_dict = load_uff_dict(ref_uff_path)

    version = uff_dict.pop('version')
    assert is_version_compatible(version, (0, 3, 0))
    print("good version")

    uff_new = UFF.deserialize(uff_dict)
    print('Does loading work correctly? -', uff_new.channel_data == uff_previous.channel_data)

    uff_new_save_path = 'new.uff'
    uff_new.save(uff_new_save_path)
    uff_dict = load_uff_dict('new.uff')
    uff_dict.pop('version')
    uff_new = UFF.deserialize(uff_dict)
    print('Does saving work correctly? -', uff_new.channel_data == uff_previous.channel_data)
