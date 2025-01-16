from dataclasses import dataclass, field
from uuid import UUID, uuid1

from slamd.materials.processing.models.additional_property import AdditionalProperty


@dataclass
class Costs:
    co2_footprint: float = None
    costs: float = None
    delivery_time: float = None
    recyclingrate: float = None


@dataclass
class Material:
    # Generate a new UUID for every material, not one for every material
    uuid: UUID = field(default_factory=uuid1)
    name: str = ''
    type: str = ''
    density: float = None
    costs: Costs = None
    additional_properties: list[AdditionalProperty] = None
    is_blended: bool = False
    blending_ratios: str = ''
    created_from: list[UUID] = None
