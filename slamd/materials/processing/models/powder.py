from dataclasses import dataclass, asdict

from slamd.common.error_handling import SlamdUnprocessableEntityException
from slamd.materials.processing.models.material import Material


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
        out['composition'] = asdict(self.composition)
        out['structure'] = asdict(self.structure)

        return out

    def from_dict(self, dictionary):
        super().from_dict(dictionary)

        new_composition = Composition()
        new_structure = Structure()

        for key in new_composition.__dict__.keys():
            if key not in dictionary['composition']: # TODO Check for!
                raise SlamdUnprocessableEntityException(message=f'Error while processing dictionary: Expected key '
                                                                f'{key}, got keys {list(dictionary.keys())}5')

            new_composition.__dict__[key] = dictionary['composition'][key]

        for key in new_structure.__dict__.keys():
            if key not in dictionary['structure']:
                raise SlamdUnprocessableEntityException(message=f'Error while processing dictionary: Expected key '
                                                                f'{key}, got keys {list(dictionary.keys())}6')

            new_structure.__dict__[key] = dictionary['structure'][key]

        self.composition = new_composition
        self.structure = new_structure
