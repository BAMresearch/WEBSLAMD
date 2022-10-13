from dataclasses import dataclass, asdict

from slamd.common.error_handling import SlamdUnprocessableEntityException
from slamd.materials.processing.models.material import Material


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
        out['composition'] = asdict(self.composition)

        return out

    def from_dict(self, dictionary):
        super().from_dict(dictionary)

        new_composition = Composition()

        for key in new_composition.__dict__.keys():
            if key not in dictionary['composition']:
                raise SlamdUnprocessableEntityException(message=f'Error while processing dictionary: Expected key '
                                                                f'{key}, got keys {list(dictionary.keys())}3')

            new_composition.__dict__[key] = dictionary['composition'][key]

        self.composition = new_composition