from dataclasses import dataclass
from slamd.materials.processing.models.material import Material


@dataclass
class Composition:
    fine_aggregates: float = None
    coarse_aggregates: float = None
    fa_density: str = None
    ca_density: str = None


@dataclass
class Aggregates(Material):
    composition: Composition = None
