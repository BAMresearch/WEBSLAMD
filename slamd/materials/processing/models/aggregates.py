from dataclasses import dataclass
from slamd.materials.processing.models.material import Material


@dataclass
class Composition:
    fine_aggregates: float = None
    coarse_aggregates: float = None
    specific_density: float = None
    bulk_density: float = None
    fineness_modulus: float = None


@dataclass
class Aggregates(Material):
    composition: Composition = None
