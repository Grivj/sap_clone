from typing import Protocol

import pygame


class Phase(Protocol):
    finished: bool = False

    def execute(self, screen: pygame.Surface, turn_number: int) -> None:
        ...

    def update(self):
        ...

    def draw(self, screen: pygame.Surface):
        ...

    def handle_event(self, event: pygame.event.Event):
        ...
