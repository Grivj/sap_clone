from typing import Protocol


class Phase(Protocol):
    def execute(self, turn_number: int) -> None:
        ...
