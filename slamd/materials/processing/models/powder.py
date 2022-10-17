from dataclasses import dataclass, asdict

from slamd.materials.processing.models.material import Material

KEY_COMPOSITION = 'composition'
KEY_STRUCTURE = 'structure'


@dataclass
class Composition:
    fe3_o2: float = None
    si_o2: float = None
    al2_o3: float = None
    ca_o: float = None
    mg_o: float = None
    na2_o: float = None
    k2_o: float = None
    s_o3: float = None
    ti_o2: float = None
    p2_o5: float = None
    sr_o: float = None
    mn2_o3: float = None
    loi: float = None


@dataclass
class Structure:
    fine: float = None
    gravity: float = None


@dataclass
class Powder(Material):
    composition: Composition = None
    structure: Structure = None

    def to_dict(self):
        out = super().to_dict()
        out[KEY_COMPOSITION] = asdict(self.composition)
        out[KEY_STRUCTURE] = asdict(self.structure)

        return out

    def from_dict(self, dictionary):
        super().from_dict(dictionary)

        new_composition = Composition()
        self._fill_object_from_dict(dictionary[KEY_COMPOSITION], new_composition)
        self.composition = new_composition

        new_structure = Structure()
        self._fill_object_from_dict(dictionary[KEY_STRUCTURE], new_structure)
        self.structure = new_structure
