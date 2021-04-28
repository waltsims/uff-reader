from dataclasses import dataclass 


@dataclass
class ImpulseResponse:
    """Specifies a temporal impulse response"""
    initial_time: float
    sampling_frequency: int
    data: list[float]
    units: str
    
