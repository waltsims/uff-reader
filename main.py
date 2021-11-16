from uff.utils import *
from uff.uff import UFF


if __name__ == '__main__':
    # fieldII_converging_wave_mlt_sector.uff        =>      OK
    # fieldII_converging_wave_grid.uff              =>      OK
    # fieldII_diverging_wave_grid.uff               =>      OK
    # fieldII_plane_wave_grid.uff                   =>      OK
    # fieldII_single_element_transmit_grid.uff      =>      OK
    # spherical_probe.uff                           =>      BLIND LOAD
    # example_probe_curvilinear.uff                 =>      BLIND LOAD
    # example_probe_matrix.uff                      =>      BLIND LOAD

    ref_uff_path = 'tests/data/fieldII_converging_wave_mlt_sector.uff'
    uff_dict = load_uff_dict(ref_uff_path)

    version = uff_dict.pop('version')
    assert is_version_compatible(version, (0, 3, 0))
    print("good version")

    uff_new = UFF.deserialize(uff_dict)

    uff_new_save_path = 'new.uff'
    uff_new.save(uff_new_save_path, version)

    verify_correctness(uff_new_save_path, ref_uff_path)
