from dataclasses import dataclass, field, asdict
from uuid import UUID, uuid1

from slamd.common.error_handling import SlamdUnprocessableEntityException
from slamd.materials.processing.models.additional_property import AdditionalProperty

KEY_COSTS = 'costs'

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

    @classmethod
    def from_dict(cls, dictionary):
        mat = cls()
        mat.fill_object_from_dict(dictionary, mat)

        new_costs = Costs()
        mat.fill_object_from_dict(dictionary[KEY_COSTS], new_costs)
        mat.costs = new_costs

        if 'uuid' in dictionary:
            mat.uuid = UUID(dictionary['uuid'])
        else:
            raise SlamdUnprocessableEntityException(message='Error while attempting to construct Material from dict: '
                                                            'No UUID')

        if dictionary['created_from']:
            mat.created_from = [UUID(uuid_str) for uuid_str in dictionary['created_from']]

        if dictionary['additional_properties']:
            mat.additional_properties = [AdditionalProperty(name=p['name'], value=p['value'])
                                         for p in dictionary['additional_properties']]

        return mat

    @classmethod
    def fill_object_from_dict(cls, dictionary, target_object):
        for key in target_object.__dict__.keys():
            if key not in dictionary:
                raise SlamdUnprocessableEntityException(message=f'Error while attempting to write values into '
                                                                f'object: Expected key {key}, got '
                                                                f'keys {list(dictionary.keys())}')

            target_object.__dict__[key] = dictionary[key]
