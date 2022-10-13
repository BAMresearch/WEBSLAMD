from dataclasses import dataclass, asdict
from slamd.materials.processing.models.material import Material


@dataclass
class Composition:
    fine_aggregates: float = None
    coarse_aggregates: float = None
    gravity: float = None
    bulk_density: float = None
    fineness_modulus: float = None
    water_absorption: float = None

@dataclass
class Aggregates(Material):
    composition: Composition = None

    def to_dict(self):
        out = super().to_dict()
        out['composition'] = asdict(self.composition)

        return out
