from dataclasses import dataclass
from slamd.materials.processing.models.material import Material


@dataclass
class Composition:
    na2_si_o3: float = None
    na_o_h: float = None
    na2_si_o3_specific: float = None
    na_o_h_specific: float = None
    total: float = None
    na2_o: float = None
    si_o2: float = None
    h2_o: float = None
    na2_o_dry: float = None
    si_o2_dry: float = None
    water: float = None
    na_o_h_total: float = None


@dataclass
class Liquid(Material):
    composition: Composition = None
