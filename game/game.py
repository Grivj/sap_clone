import logging
from dataclasses import dataclass

import pygame

from .entities import Pet, Player, Turn
from .entities.phases import BuyingPhase, CombatPhase

logger = logging.getLogger(__name__)


@dataclass
class Game:
    screen_size: tuple[int, int] = 800, 600

    def __post_init__(self):
        # Initialize Pygame and set up the display window
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        # Draw a white background color onto the screen
        self.screen.fill((255, 255, 255))

        # Initialize the entities
        self.player = Player()

        # Initialize with the starting phase
        self.phase = BuyingPhase(self.player)
        self.turn_number = 1

        logger.info("Initialized game")
        self.running: bool = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Quitting game")
                self.running = False

            self.phase.handle_event(event)

    def is_end_of_game(self):
        # Check for the end of the game
        if self.player.score >= 10:
            logger.info("🥇 Player has won the game!")
            self.running = False
        elif self.player.lives <= 0:
            logger.info("💀 Player has lost the game.")

    def run(self):
        self.phase.execute(self.screen, self.turn_number)
        while self.running:
            self.handle_events()
        pygame.quit()
