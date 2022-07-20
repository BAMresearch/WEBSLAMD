from dataclasses import dataclass
from slamd.materials.processing.models.material import Material


@dataclass
class Composition:
    fine_aggregates: float = None
    coarse_aggregates: float = None
    fa_density: float = None
    ca_density: float = None


@dataclass
class Aggregates(Material):
    composition: Composition = None
