from dataclasses import dataclass
from slamd.materials.processing.models.material import Material


@dataclass
class Process(Material):
    duration: float = None
    temperature: float = None
    relative_humidity: float = None
