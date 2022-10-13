from dataclasses import dataclass, asdict

from slamd.common.error_handling import SlamdUnprocessableEntityException
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

    def from_dict(self, dictionary):
        super().from_dict(dictionary)

        new_composition = Composition()

        for key in new_composition.__dict__.keys():
            if key not in dictionary['composition']:
                raise SlamdUnprocessableEntityException(message=f'Error while processing dictionary: Expected key '
                                                                f'{key}, got keys {list(dictionary.keys())}2')

            new_composition.__dict__[key] = dictionary['composition'][key]

        self.composition = new_composition
