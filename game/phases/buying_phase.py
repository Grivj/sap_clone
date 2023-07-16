import logging
from dataclasses import dataclass

from ..entities import Player, Shop

logger = logging.getLogger(__name__)


@dataclass
class BuyingPhase:
    player: Player
    shop: Shop

    def execute(self):
        """
        Buying phase, a player can chose to buy from the shop if he has the
        available amount of money and enough space in his inventory
        """

        # for now, we buy all pets from the shop
        logger.info("Buying phase")
        logger.info(f"Shop: {self.shop}")

        while self.player.gold:
            if not self.shop.pets:
                logger.info("Shop is empty")
                break
            pet = self.shop.pets.pop()
            logger.info(f"Buying {pet}")
            self.player.buy_pet(pet)
