from debug_h5_dict import traverse
from uff.uff_io import Serializable
from uff.utils import *
from uff.uff import UFF

if __name__ == '__main__':
    test_dict = load_dict_from_hdf5('/Users/faridyagubbayli/Work/fieldII_converging_wave_mlt_sector.uff')
    uff = traverse(test_dict)

    test_dict = load_dict_from_hdf5('/Users/faridyagubbayli/Work/fieldII_converging_wave_mlt_sector.uff')
    uff_dict = strip_prefix_from_keys(old_dict=test_dict, prefix="uff.")

    version = uff_dict.pop('version')
    assert is_version_compatible(version, (0, 3, 0))
    print("good version")

    uff_deserialized = UFF.deserialize(uff_dict)

    print('Does outputs match:', uff_deserialized.channel_data == uff.channel_data)

    uff_serialized = uff_deserialized.serialize()
    uff_serialized['version'] = version
    uff_serialized['uff.channel_data'] = uff_serialized.pop('channel_data')

    print(uff_serialized)
