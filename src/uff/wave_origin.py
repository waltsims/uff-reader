from abc import ABC
from dataclasses import dataclass


@dataclass
class WaveOrigin(ABC):
    def __new__(cls, *args, **kwargs):
        if cls == WaveOrigin or cls.__bases__[0] == WaveOrigin:
            raise TypeError("WaveOrigin is an abstract class. Cannot instantiate abstract class")
        return super().__new__(cls)

