from dataclasses import dataclass

from ..events import Event
from .ability import Ability


@dataclass
class Pet:
    name: str
    attack: int
    health: int
    abilities: list[Ability]
    cost: int = 3

    def on_event(self, event: Event):
        # Trigger any abilities that respond to this event
        for ability in self.abilities:
            ability.trigger(event)

    def __str__(self):
        return f"{self.name} 🪙{self.cost} ⚔️{self.attack} ❤️{self.health}"
