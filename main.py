import os

import numpy as np

from debug_h5_dict import traverse
from uff.uff_io import Serializable
from uff.utils import *
from uff.uff import UFF


def load_with_previous_code(path):
    test_dict = load_dict_from_hdf5(path)
    uff = traverse(test_dict)
    return uff


def load_uff_dict(path):
    test_dict = load_dict_from_hdf5('/Users/faridyagubbayli/Work/uff_references/fieldII_converging_wave_mlt_sector.uff')
    uff_dict = strip_prefix_from_keys(old_dict=test_dict, prefix="uff.")
    return uff_dict


def load_h5dump(filepath):
    output_fields = os.popen(f'h5dump -n 1 {filepath}').read()
    output_fields = output_fields.split('\n')

    attributes = [l for l in output_fields if l.startswith(' attribute')]
    attributes = [a.replace('attribute', '').strip() for a in attributes]

    groups = [l for l in output_fields if l.startswith(' group')]
    groups = [g.replace('group', '').strip() for g in groups]

    datasets = [l for l in output_fields if l.startswith(' dataset')]
    datasets = [d.replace('dataset', '').strip() for d in datasets]

    return groups, datasets, attributes


def verify_correctness(output_path, ref_path):
    out_groups, out_datasets, out_attrs = load_h5dump(output_path)
    ref_groups, ref_datasets, ref_attrs = load_h5dump(ref_path)

    if len(set(ref_groups) - set(out_groups)):
        print('Some groups are not present in the output UFF file!')
        print(set(ref_groups) - set(out_groups))
        raise AssertionError

    if len(set(ref_datasets) - set(out_datasets)):
        print('Some datasets are not present in the output UFF file!')
        print(set(ref_datasets) - set(out_datasets))
        raise AssertionError

    if len(set(ref_attrs) - set(out_attrs)):
        print('Some attrs are not present in the output UFF file!')
        print(set(ref_attrs) - set(out_attrs))
        raise AssertionError

    # with h5py.File(output_path, 'r') as out_file:
    #     with h5py.File(ref_path, 'r') as ref_file:
    #
    #         for ds_path in out_datasets:
    #             print(ds_path)
    #
    #             ref_ds = np.array(ref_file[ds_path])
    #             out_ds = np.array(out_file[ds_path])
    #
    #             if ref_ds.dtype != '|S1':
    #                 assert np.allclose(out_ds, ref_ds)
    #
    # print('aaa')


if __name__ == '__main__':
    ref_uff_path = '/Users/faridyagubbayli/Work/uff_references/fieldII_converging_wave_mlt_sector.uff'
    # ref_uff_path = '/Users/faridyagubbayli/Work/uff_references/example_probe_curvilinear.uff'

    uff_dict = load_uff_dict(ref_uff_path)

    version = uff_dict.pop('version')
    assert is_version_compatible(version, (0, 3, 0))
    print("good version")

    uff_new = UFF.deserialize(uff_dict)

    uff_new_save_path = 'new.uff'
    uff_new.save(uff_new_save_path, version)

    verify_correctness(uff_new_save_path, ref_uff_path)

