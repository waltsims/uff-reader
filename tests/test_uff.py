from uff.utils import *
from uff.uff import UFF


def test_uff_save_load():
    ref_folder = '/Users/faridyagubbayli/Work/uff_references'
    ref_files = [
        'fieldII_converging_wave_mlt_sector.uff',
        'fieldII_converging_wave_grid.uff',
        'fieldII_diverging_wave_grid.uff',
        'fieldII_plane_wave_grid.uff',
        'fieldII_single_element_transmit_grid.uff',
    ]

    for ref_file in ref_files:
        ref_uff_path = os.path.join(ref_folder, ref_file)
        uff_dict = load_uff_dict(ref_uff_path)

        version = uff_dict.pop('version')
        assert is_version_compatible(version, (0, 3, 0))
        print("good version")

        uff_new = UFF.deserialize(uff_dict)

        uff_new_save_path = 'new.uff'
        uff_new.save(uff_new_save_path, version)

        verify_correctness(uff_new_save_path, ref_uff_path)
