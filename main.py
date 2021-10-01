from debug_h5_dict import traverse
from uff.uff_io import Serializable
from uff.utils import *

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
