from dataclasses import dataclass
from typing import List


@dataclass
class ImpulseResponse:
    """Specifies a temporal impulse response"""
    initial_time: float
    sampling_frequency: int
    data: List[float]
    units: str
    
