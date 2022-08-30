from dataclasses import dataclass


@dataclass
class AddTargetsDto:
    index: int = 0
    preview_of_data: str = ''
    targets: list = None
