from dataclasses import dataclass

@dataclass
class Rotation:
    "Contains a rotation in space in spherical coordinates and SI units. The rotation is specified using Euler angles that are applied in the order ZYX."
    x: float = 0
    y: float = 0
    z: float = 0
