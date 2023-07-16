from typing import Protocol

from ..events import Event


class Ability(Protocol):
    def trigger(self, event: Event) -> None:
        ...
