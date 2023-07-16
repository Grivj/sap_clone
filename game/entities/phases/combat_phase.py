import logging
from dataclasses import dataclass

from ...entities import Pet, Player

logger = logging.getLogger(__name__)


@dataclass
class CombatPhase:
    player: Player

    def execute(self, turn_number: int):
        """Combat phase, a player can chose to attack another player."""
        logger.info(f"[🎲{turn_number}] Combat phase")

        self.ai_team = self.generate_ai_team(turn_number)

        # Each pet attacks in order until one team has no pets left
        while self.player.pets and self.ai_team:
            self.attack_round(self.player.pets[0], self.ai_team[0])
            self.remove_dead_pets(self.player.pets)
            self.remove_dead_pets(self.ai_team)

        self.determine_winner(self.ai_team)

    def generate_ai_team(self, turn_number: int) -> list[Pet]:
        """
        Generate a team of pets for the AI that is based on the turn number.
        """
        return [
            Pet(
                f"AI pet {i}",
                attack=1 + turn_number,
                health=1 + turn_number,
                abilities=[],
            )
            for i in range(1, 6)
        ]

    def attack_round(self, player_pet: Pet, ai_pet: Pet):
        """One round of attacks between two pets."""
        # While both pets are alive, they attack each other
        while player_pet.health > 0 and ai_pet.health > 0:
            ai_pet.health -= player_pet.attack
            player_pet.health -= ai_pet.attack
            logger.info(f"{player_pet.name} ❤️{player_pet.health}")
            logger.info(f"{ai_pet.name} ❤️{ai_pet.health}")

    def remove_dead_pets(self, team: list[Pet]):
        """Remove dead pets from a team."""
        for pet in team:
            if pet.health <= 0:
                team.remove(pet)
                logger.info(f"{pet} died 😵")

    def determine_winner(self, ai_team: list[Pet]):
        """Determine the winner of the combat phase."""
        if len(self.player.pets) > len(ai_team):
            self.player.score += 1  # Player wins the round
            logger.info("Player wins the round")
        elif len(self.player.pets) < len(ai_team):
            self.player.lives -= 1  # Player loses the round
            logger.info("Player loses the round")
        else:
            logger.info(
                "Combat phase ended with a tie"
            )  # In case of a tie, no points are awarded
