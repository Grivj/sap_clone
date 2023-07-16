import logging
from dataclasses import dataclass

from ..phases import Phase
from .pet import Pet
from .player import Player
from .shop import Shop

logger = logging.getLogger(__name__)


@dataclass
class Turn:
    phases: list[Phase]

    def run(self):
        for phase in self.phases:
            phase.execute()
