from dataclasses import dataclass, field, asdict
from uuid import UUID, uuid1

from slamd.common.error_handling import SlamdUnprocessableEntityException
from slamd.materials.processing.models.additional_property import AdditionalProperty


@dataclass
class Costs:
    co2_footprint: float = None
    costs: float = None
    delivery_time: float = None


@dataclass
class Material:
    # Generate a new UUID for every material, not one for every material
    uuid: UUID = field(default_factory=lambda: uuid1())
    name: str = ''
    type: str = ''
    costs: Costs = None
    additional_properties: list[AdditionalProperty] = None
    is_blended: bool = False
    blending_ratios: str = ''
    created_from: list[UUID] = None

    def to_dict(self):
        out = asdict(self)
        out['uuid'] = str(self.uuid)
        if self.costs:
            out['costs'] = asdict(self.costs)
        if self.additional_properties:
            out['additional_properties'] = [asdict(prop) for prop in self.additional_properties]
        if self.created_from:
            out['created_from'] = [str(uuid) for uuid in self.created_from]

        return out

    def from_dict(self, dictionary):
        # TODO turn into classmethod/factory?
        for key in self.__dict__.keys():
            if key not in dictionary:
                raise SlamdUnprocessableEntityException(message=f'Error while processing dictionary: Expected key '
                                                                f'{key}, got keys {list(dictionary.keys())}1')

            self.__dict__[key] = dictionary[key]

        new_costs = Costs()

        for key in new_costs.__dict__.keys():
            if key not in dictionary['costs']:
                raise SlamdUnprocessableEntityException(message=f'Error while processing dictionary: Expected key '
                                                                f'{key}, got keys {list(dictionary.keys())}2')

            new_costs.__dict__[key] = dictionary['costs'][key]

        self.costs = new_costs
        # TODO check for existence
        self.uuid = UUID(dictionary['uuid'])
        if dictionary['created_from']:
            self.created_from = [UUID(uuid_str) for uuid_str in dictionary['created_from']]
