import logging
from dataclasses import dataclass

from .phases import Phase

logger = logging.getLogger(__name__)


@dataclass
class Turn:
    phases: list[Phase]

    def run(self):
        for phase in self.phases:
            phase.execute()
