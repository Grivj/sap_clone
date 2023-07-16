import logging
from dataclasses import dataclass

from ...entities import Pet, Player, Shop
from ...events import BuyEvent, SellEvent
from ...exceptions import NotEnoughGold, NotEnoughPlace, NotOwnedPet

logger = logging.getLogger(__name__)
REFRESH_COST = 1


@dataclass
class BuyingPhase:
    player: Player

    def execute(self, turn_number: int):
        """
        Buying phase, a player can chose to buy from the shop if he has the
        available amount of money and enough space in his inventory.
        """

        # for now, we buy all pets from the shop
        logger.info("Buying phase")
        self.shop = self.generate_shop(turn_number)
        logger.info(f"Shop: {self.shop}")

        while self.player.gold >= 3:
            if not self.shop.pets:
                logger.info("Shop is empty")
                break
            pet = self.shop.pets.pop()
            self.buy_pet(pet)

    def generate_shop(self, turn_number: int) -> Shop:
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

    def refresh_shop(self, turn_number: int):
        """Generate a shop with pets for the player to buy from."""
        if self.player.gold >= REFRESH_COST:
            self.shop = self.generate_shop(turn_number)
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
