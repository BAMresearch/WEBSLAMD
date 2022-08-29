from dataclasses import dataclass


@dataclass
class AddTargetsDto:

    index: int = 0
    targets: list = None
