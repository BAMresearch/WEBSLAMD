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

    def from_dict(self, dictionary):
        super().from_dict(dictionary)

        new_composition = Composition()
        self._fill_object_from_dict(dictionary[KEY_COMPOSITION], new_composition)
        self.composition = new_composition
