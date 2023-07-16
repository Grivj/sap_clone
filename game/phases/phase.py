from typing import Protocol


class Phase(Protocol):
    def execute(self) -> None:
        ...
