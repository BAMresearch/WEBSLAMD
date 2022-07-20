from dataclasses import dataclass
from slamd.materials.processing.models.material import Material


@dataclass
class Admixture(Material):
    composition: float = None
    admixture_type: str = None
