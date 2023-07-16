from dataclasses import dataclass, field

from .pet import Pet


@dataclass
class Shop:
    pets: list[Pet] = field(default_factory=list)

    def sell_pet(self, pet: Pet) -> int:
        if pet in self.pets:
            self.pets.remove(pet)
            return pet.cost  # We assume that pets have a cost attribute
        return 0  # The pet was not in the shop

    def buy_pet(self, pet: Pet):
        self.pets.append(pet)

    def __str__(self):
        output = "Shop:\n"
        for pet in self.pets:
            output += f"{pet}\n"
        return output
