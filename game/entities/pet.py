from dataclasses import dataclass, field
from pathlib import Path

import pygame

from game.utils.sprites import draw_sprite

from ..events import Event
from .ability import Ability


@dataclass
class Pet(pygame.sprite.Sprite):
    name: str
    attack: int
    health: int
    abilities: list[Ability] = field(default_factory=list)
    cost: int = 3

    sprite_sheet_path: Path = (
        Path(__file__).parent.parent / "assets" / "sprites" / "pets.png"
    )
    sprite_coords: tuple[int, int] = (0, 0)  # column, row
    sprite_size: tuple[int, int] = (230, 230)

    def __post_init__(self):
        super().__init__()
        self.image = draw_sprite(
            self.sprite_sheet_path, *self.sprite_coords, *self.sprite_size
        )
        self.rect = self.image.get_rect()

    def on_event(self, event: Event):
        # Trigger any abilities that respond to this event
        for ability in self.abilities:
            ability.trigger(event)

    def __str__(self):
        return f"{self.name} 🪙{self.cost} ⚔️{self.attack} ❤️{self.health}"

    def __hash__(self) -> int:
        return hash(self.name)
