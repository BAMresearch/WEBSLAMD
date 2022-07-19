from dataclasses import dataclass
from slamd.materials.processing.models.material import Material


@dataclass
class Custom(Material):
    custom_name: str = None
    custom_value: str = None
