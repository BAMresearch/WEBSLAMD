from dataclasses import dataclass, field
from uuid import UUID, uuid1

from slamd.materials.processing.models.additional_property import AdditionalProperty


@dataclass
class Costs:
    co2_footprint: float = None
    costs: float = None
    delivery_time: float = None

    def to_dict(self):
        return {
            'co2_footprint': self.co2_footprint,
            'costs': self.costs,
            'delivery_time': self.delivery_time
        }


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
        out = vars(self)
        out['uuid'] = str(self.uuid)

        if self.costs is not None:
            out['costs'] = self.costs.to_dict()
        else:
            out['costs'] = None

        return out
