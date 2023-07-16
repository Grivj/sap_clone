from dataclasses import dataclass, field

from ..events import BuyEvent, SellEvent
from .pet import Pet


@dataclass
class Player:
    pets: list[Pet] = field(default_factory=list)
    gold: int = 10
    score: int = 0
    lives: int = 5

    def buy_pet(self, pet: Pet):
        if self.gold >= pet.cost:
            self.pets.append(pet)
            self.gold -= pet.cost
            pet.on_event(BuyEvent())  # Trigger any on-buy abilities

    def sell_pet(self, pet: Pet, price: int):
        if pet in self.pets:
            self.pets.remove(pet)
            self.gold += price
            pet.on_event(SellEvent())  # Trigger any on-sell abilities
