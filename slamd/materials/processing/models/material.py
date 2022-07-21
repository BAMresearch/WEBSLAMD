from uuid import UUID, uuid1
from dataclasses import dataclass, field
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
