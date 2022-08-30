from dataclasses import dataclass


@dataclass
class DataWithTargetsDto:
    index: int = 0
    preview_of_data: str = ''
    targets: list = None


@dataclass
class TargetDto:
    index: int = 0
    name: str = ''
    value: float = None
