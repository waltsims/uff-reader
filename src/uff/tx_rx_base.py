from dataclasses import dataclass
import numpy as np
from uff.uff_io import Serializable


@dataclass
class TxRxSetupBase(Serializable):

    @staticmethod
    def str_name():
        raise NotImplementedError

    def __eq__(self, other):
        return super().__eq__(other)

    def __setattr__(self, name, val):
        # Why does the dataclass @property won't work here?
        # Because while serializing the objects to .uff file,
        #       we look at the __annotations__ of each class to collect the datatype.
        #       When using dataclass setter/getter methods, field name will not appear in the
        #       __annotations__ dictionary. Therefore, we need to use the `__setattr__`.
        if name == 'channel_mapping':
            if isinstance(val, list):
                pass
            elif isinstance(val, np.ndarray):
                assert val.ndim == 2
                val = val.tolist()
        super().__setattr__(name, val)
