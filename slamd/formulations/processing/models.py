from dataclasses import dataclass
from typing import Optional

from slamd.materials.processing.models.material import Material
from slamd.materials.processing.models.process import Process


@dataclass
class MaterialContent:
    material: Material
    mass: Optional[float] = None
    volume: Optional[float] = None


@dataclass
class ConcreteComposition:
    powder: MaterialContent | None
    liquid: MaterialContent | None
    admixture: MaterialContent | None
    aggregate: MaterialContent | None
    custom: MaterialContent | None

    air_pore_content: float  # In percent
    process: Optional[Process]

    costs: Optional[float] = None
    co2_footprint: Optional[float] = None
    delivery_time: Optional[float] = None
