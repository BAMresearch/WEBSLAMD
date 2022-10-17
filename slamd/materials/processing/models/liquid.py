from dataclasses import dataclass, asdict

from slamd.materials.processing.models.material import Material

KEY_COMPOSITION = 'composition'


@dataclass
class Composition:
    na2_si_o3: float = None
    na2_si_o3_mol: float = None
    na_o_h: float = None
    na_o_h_mol: float = None
    na2_o: float = None
    na2_o_mol: float = None
    si_o2: float = None
    si_o2_mol: float = None
    h2_o: float = None
    h2_o_mol: float = None


@dataclass
class Liquid(Material):
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
