from dataclasses import dataclass, field, asdict
from uuid import UUID, uuid1

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
        out = self.__dict__.copy()
        out['uuid'] = str(self.uuid)
        if self.costs:
            out['costs'] = asdict(self.costs)
        if self.additional_properties:
            out['additional_properties'] = [asdict(prop) for prop in self.additional_properties]
        if self.created_from:
            out['created_from'] = [str(uuid) for uuid in self.created_from]

        return out
