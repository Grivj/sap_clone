import logging
from dataclasses import dataclass

import pygame

from .entities import Pet, Player, Shop, Turn
from .entities.phases import BuyingPhase, CombatPhase

logger = logging.getLogger(__name__)


@dataclass
class Game:
    screen_size: tuple[int, int] = 800, 600

    def __post_init__(self):
        # Initialize Pygame and set up the display window
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)

        # Initialize the game state
        self.state = None  # TODO: Replace with actual game state

        # Initialize the entities
        self.player = Player()
        self.shop = Shop(
            pets=[
                Pet("Ant", attack=3, health=2, abilities=[]),
                Pet("Bird", attack=2, health=3, abilities=[]),
                Pet("Small Dog", attack=1, health=4, abilities=[]),
            ]
        )
        logger.info("Initialized game")

    def handle_events(self):
        # Process all events from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Signal to exit the game

            # TODO: Handle other events (like user input)

        return True  # Continue the game

    def update(self):
        # Update the game state
        pass  # TODO: Implement this

    def draw(self):
        # Draw the current game state onto the screen
        pass  # TODO: Implement this

    def run(self):
        # Main game loop
        running = True
        while running:
            # Create a new turn
            turn = Turn(
                [
                    BuyingPhase(self.player, self.shop),
                    CombatPhase(self.player),
                ]
            )
            # Run the phases of the turn
            turn.run()

            running = False

            # running = self.handle_events()
            # self.update()
            # self.draw()
            # pygame.display.flip()  # Update the display

        pygame.quit()
