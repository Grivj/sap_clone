import pytest

from game import Game, Pet, Player
from game.entities.phases import CombatPhase


@pytest.fixture
def game() -> Game:
    return Game(screen_size=(1980, 720))


@pytest.fixture
def player() -> Player:
    return Player(pets=[Pet("Cat", 1, 1), Pet("Dog", 2, 2), Pet("Bird", 3, 3)])


def test_attack_round_until_death():
    player = Player(pets=[Pet("Cat", 3, 3)])
    combat_phase = CombatPhase(player)
    pet_2 = Pet("Dog", 3, 3)

    combat_phase.attack_round(player.pets[0], pet_2)
    # Test that the pets attack each other until they are both dead
    assert player.pets[0].health == 0
    assert pet_2.health == 0


@pytest.mark.parametrize(
    "player_pet, ai_pet, expected_player_health, expected_ai_health",
    [
        (Pet("Cat", 3, 3), Pet("Dog", 3, 3), 0, 0),
        (Pet("Cat", 3, 3), Pet("Dog", 3, 1), 0, 0),
        (Pet("Cat", 3, 1), Pet("Dog", 3, 3), 0, 0),
        (Pet("Cat", 3, 3), Pet("Dog", 2, 2), 1, 0),
    ],
)
def test_attack_round_result(
    player_pet: Pet,
    ai_pet: Pet,
    expected_player_health: int,
    expected_ai_health: int,
):
    player = Player(pets=[player_pet])
    combat_phase = CombatPhase(player)

    combat_phase.attack_round(player.pets[0], ai_pet)
    # Test that the pets attack each other until one is dead
    assert player.pets[0].health == expected_player_health
    assert ai_pet.health == expected_ai_health
