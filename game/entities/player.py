import logging
from dataclasses import dataclass, field

from .pet import Pet

logger = logging.getLogger(__name__)


@dataclass
class Player:
    pets: list[Pet] = field(default_factory=list)
    gold: int = 10
    score: int = 0
    lives: int = 5
