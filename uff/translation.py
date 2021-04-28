from dataclasses import dataclass

@dataclass
class Translation:
    "Define a translation operation in a 3D Cartesian system"
    x: float
    y: float
    z: float

