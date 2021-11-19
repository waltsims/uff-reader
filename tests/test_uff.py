import os
from pathlib import Path

from uff.uff import UFF
from uff.utils import verify_correctness, is_version_compatible, load_uff_dict, download_test_data

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
)


def test_uff_save_load():
    ref_files = [
        'fieldII_converging_wave_mlt_sector.uff',
        'fieldII_converging_wave_grid.uff',
        'fieldII_diverging_wave_grid.uff',
        'fieldII_plane_wave_grid.uff',
        'fieldII_single_element_transmit_grid.uff',
    ]

    # check all files exist in data/
    missing_files = [file for file in ref_files if not os.path.isfile(Path(FIXTURE_DIR) / file)]
    if missing_files:
        print("Downloading test files...")
        # if they do not download them with utils.
        base_url = 'http://ustb.no/datasets/uff/'
        urls = [base_url + file for file in missing_files]
        download_test_data(rel_path=FIXTURE_DIR, file_urls=urls)

    for ref_file in ref_files:
        ref_uff_path = os.path.join(FIXTURE_DIR, ref_file)
        uff_dict = load_uff_dict(ref_uff_path)

        version = uff_dict['version']
        assert is_version_compatible(version, (0, 3, 0))
        print("good version")

        uff_new = UFF.load(ref_uff_path)

        uff_new_save_path = 'new.uff'
        uff_new.save(uff_new_save_path, version)

        verify_correctness(uff_new_save_path, ref_uff_path)
