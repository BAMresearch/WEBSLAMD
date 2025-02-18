from dataclasses import dataclass

@dataclass
class Material:
    uuid: str
    mass: float | None
    volume: float | None


@dataclass
class ConcreteComposition:
    powder: Material | None
    liquid: Material | None
    admixture: Material | None
    aggregate: Material | None
    air_pore_content: float  # In percent
    custom: Material | None
