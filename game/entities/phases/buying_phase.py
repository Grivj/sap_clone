import logging
from dataclasses import dataclass, field

import pygame
from pygame.constants import MOUSEBUTTONDOWN

from ...entities import Pet, Player, Shop
from ...events import BuyEvent, SellEvent
from ...exceptions import NotEnoughGold, NotEnoughPlace, NotOwnedPet
from .phase import Phase

logger = logging.getLogger(__name__)
REFRESH_COST = 1


def generate_shop(turn_number: int) -> Shop:
    """Generate a shop with pets for the player to buy from."""
    return Shop(
        [
            Pet(
                f"Shop pet {i}",
                attack=1 + turn_number,
                health=1 + turn_number,
                abilities=[],
            )
            for i in range(1, 6)
        ]
    )


@dataclass
class BuyingPhase(Phase):
    player: Player
    pets_rects: dict[Pet, pygame.Rect] = field(default_factory=dict)

    def handle_event(self, event: pygame.event.Event):
        if event.type == MOUSEBUTTONDOWN:
            # Check if the player clicked on a pet
            mouse_pos = pygame.mouse.get_pos()
            for pet, rect in self.pets_rects.items():
                if rect.collidepoint(mouse_pos):
                    self.buy_pet(pet)
                    # Remove the pet from the shop
                    self.shop.pets.remove(pet)
                    # Redraw the shop
                    pygame.display.flip()

        return

    def execute(self, screen: pygame.Surface, turn_number: int):
        """
        Buying phase, a player can chose to buy from the shop if he has the
        available amount of money and enough space in his inventory.
        """

        # for now, we buy all pets from the shop
        logger.info("Buying phase")
        self.shop = generate_shop(turn_number)
        self.draw_shop(screen)
        logger.info(f"Shop: {self.shop}")

    def draw_shop(self, screen: pygame.Surface):
        """Draw the shop on the screen."""
        # Clear the screen
        screen.fill((255, 255, 255))  # Fill the screen with white

        # Create a "Finish Buying" button
        finish_button_rect = pygame.Rect(50, 500, 200, 50)
        pygame.draw.rect(screen, (200, 0, 0), finish_button_rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Finish Buying", 1, (10, 10, 10))
        screen.blit(text, finish_button_rect)

        # Draw the shop pets
        for i, pet in enumerate(self.shop.pets):
            button_rect = pygame.Rect(50, 50 + i * 100, 200, 50)
            pygame.draw.rect(screen, (200, 0, 0), button_rect)
            font = pygame.font.Font(None, 36)
            text = font.render(f"Buy {pet}", 1, (10, 10, 10))
            screen.blit(text, button_rect)
            self.pets_rects[pet] = button_rect

        pygame.display.flip()

    def refresh_shop(self, turn_number: int):
        """Generate a shop with pets for the player to buy from."""
        if self.player.gold >= REFRESH_COST:
            self.shop = generate_shop(turn_number)
            logger.info(f"🔄 Refreshed shop: {self.shop}")
            self.player.gold -= REFRESH_COST
            return
        raise NotEnoughGold(
            f"Player has {self.player.gold} gold, but refreshing costs {REFRESH_COST}"
        )

    def buy_pet(self, pet: Pet) -> int:
        if len(self.player.pets) >= 5:
            raise NotEnoughPlace(f"Player already has {len(self.player.pets)} pets")
        if self.player.gold >= pet.cost:
            logger.info(f"🛒 Buying {pet}")
            self.player.pets.append(pet)
            self.player.gold -= pet.cost
            pet.on_event(BuyEvent())  # Trigger any on-buy abilities
            return self.player.gold
        raise NotEnoughGold(
            f"Player has {self.player.gold} gold, but {pet} costs {pet.cost}"
        )

    def sell_pet(self, pet: Pet, price: int):
        if pet in self.player.pets:
            logger.info(f"🛒 Selling {pet}")
            self.player.pets.remove(pet)
            self.player.gold += price
            pet.on_event(SellEvent())  # Trigger any on-sell abilities
        raise NotOwnedPet(f"Player does not own {pet}")

    def update(self):
        ...

    def draw(self, screen: pygame.Surface):
        ...
