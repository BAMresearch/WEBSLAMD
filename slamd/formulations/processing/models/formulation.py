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
class Formulation:
    powder: MaterialContent | None
    liquid: MaterialContent | None
    admixture: MaterialContent | None
    aggregates: MaterialContent | None
    custom: MaterialContent | None

    air_pore_content: Optional[float]  # In percent
    process: Optional[Process]

    costs: Optional[float] = None
    co2_footprint: Optional[float] = None
    delivery_time: Optional[float] = None
    recycling_rate: Optional[float] = None
    specific_gravity: Optional[float] = None

    total_mass: Optional[float] = None
