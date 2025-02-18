from dataclasses import dataclass

@dataclass
class Material:
    uuid: str
    mass: float
    volume: float


@dataclass
class ConcreteComposition:
    powder: Material
    liquid: Material
    admixture: Material
    aggregate: Material
    air_pore_content: Material
    custom: Material
