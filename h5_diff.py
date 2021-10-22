import json
import os
from copy import deepcopy

import numpy as np
import h5py
from deepdiff import DeepDiff
from hashlib import sha256


class H5Summary(object):

    def __init__(self, summary: dict):
        self.summary = summary

    @staticmethod
    def from_h5(h5_path):
        data = {}

        def extract_summary(name, obj):
            if isinstance(obj, h5py.Group):
                return
            np_obj = np.array(obj)
            data[name] = {
                'dtype': str(obj.dtype),
                'attrs': H5Summary._convert_attrs(obj.attrs),
                'shape': list(obj.shape),
                'checksums': {
                    # why to have " + 0" here?
                    # because in NumPy, there could be 0 & -0
                    # while hashing we only want single type of zero
                    # therefore we add 0 to have only non-negative zero
                    str(sd): sha256(np_obj.round(sd) + 0).hexdigest() for sd in range(6, 17, 2)
                }
            }

        with h5py.File(h5_path, 'r') as hf:
            hf.visititems(extract_summary)
            data['root'] = {
                'attrs': H5Summary._convert_attrs(hf.attrs)
            }
        return H5Summary(data)

    @staticmethod
    def _convert_attrs(attrs):
        return {k: str(v) for k, v in dict(attrs).items()}

    def get_diff(self, other, eps=1e-8, precision=8):
        assert isinstance(other, H5Summary)
        own_summary = self._strip_checksums(precision)
        other_summary = other._strip_checksums(precision)
        # diff = DeepDiff(own_summary, other_summary, exclude_paths=excluded, math_epsilon=eps)
        diff = DeepDiff(own_summary, other_summary, math_epsilon=eps)
        return diff

    def _strip_checksums(self, target_precision):
        if not isinstance(target_precision, str):
            target_precision = str(target_precision)

        summary = deepcopy(self.summary)
        for k in summary.keys():
            if 'checksums' in summary[k]:
                summary[k]['checksums'] = {target_precision: summary[k]['checksums'][target_precision]}
        return summary

