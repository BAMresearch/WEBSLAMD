from dataclasses import dataclass, asdict

from slamd.materials.processing.models.material import Material

KEY_COMPOSITION = 'composition'


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
        out[KEY_COMPOSITION] = asdict(self.composition)

        return out

    @classmethod
    def from_dict(cls, dictionary):
        agg = super().from_dict(dictionary)

        new_composition = Composition()
        agg.fill_object_from_dict(dictionary[KEY_COMPOSITION], new_composition)
        agg.composition = new_composition

        return agg
