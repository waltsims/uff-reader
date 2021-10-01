from __future__ import annotations
import abc
from typing import List, Type
import numpy as np
import typing

from uff.utils import *


class Serializable(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def str_name():
        return

    # @abc.abstractmethod
    def serialize(self):
        return

    @classmethod
    def deserialize(cls: object, data: dict):
        primitives = (np.ndarray, np.int64, np.float64, str, bytes, int, float)
        fields = cls.__annotations__

        for k, v in data.items():
            assert k in fields
            if isinstance(v, primitives):
                continue
            assert isinstance(v, dict), f'{type(v)} did not pass type-assertion'

            # property_cls = Serializable.get_subcls_with_name(k)
            property_cls = fields[k]
            if isinstance(property_cls, typing._GenericAlias):
                property_cls = property_cls.__args__[0]
            print(property_cls)  # property_cls.__origin__ is list§
            assert property_cls is not None, f'Class {k} is not Serializable!'

            if not is_keys_str_decimals(v):
                data[k] = property_cls.deserialize(v)
            else:
                # TODO: assert keys are correct => ascending order starting from 000001
                list_of_objs = list(v.values())
                list_of_objs = [property_cls.deserialize(item) for item in list_of_objs]
                data[k] = list_of_objs

        return cls(**data)

    # @classmethod
    # def deserialize(cls, data: dict):
    #     primitives = (np.ndarray, np.int64, np.float64, str, bytes, int, float)
    #
    #     if cls.__name__ == 'TransmitSetup':
    #         print('aaa')
    #
    #     for k, v in data.items():
    #         if isinstance(v, primitives):
    #             continue
    #         assert isinstance(v, dict), f'{type(v)} did not pass type-assertion'
    #
    #         property_cls = Serializable.get_subcls_with_name(k)
    #         print(property_cls)
    #         assert property_cls is not None, f'Class {k} is not Serializable!'
    #
    #         if not is_keys_str_decimals(v):
    #             data[k] = property_cls.deserialize(v)
    #         else:
    #             # TODO: assert keys are correct => ascending order starting from 000001
    #             list_of_objs = list(v.values())
    #             list_of_objs = [property_cls.deserialize(item) for item in list_of_objs]
    #             data[k] = list_of_objs
    #
    #     return cls(**data)

    @staticmethod
    def all_subclasses(cls=None) -> List[Type[Serializable]]:
        if cls is None:
            cls = Serializable
        subclasses = set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in Serializable.all_subclasses(c)])
        return list(subclasses)

    @staticmethod
    def get_subcls_with_name(name) -> Type[Serializable]:
        all_subclasses = Serializable.all_subclasses()
        for subcls in all_subclasses:
            if subcls.str_name() == name:
                return subcls
        return None

    def assign_primitives(self, dictionary: dict):
        primitives = (np.ndarray, np.int64, np.float64, str, bytes)
        set_list = []
        obj_attrs = list(self.__annotations__)
        for k, v in dictionary.items():
            assert k in obj_attrs
            if isinstance(v, primitives):
                setattr(self, k, primitives)
                set_list.append(k)

        remaining_list = list(set(obj_attrs) - set(set_list))
        return set_list, remaining_list
