import pygame

from game import Game


def test_game_initialization():
    game = Game(screen_size=(1980, 720))

    # Test that Pygame was initialized
    assert pygame.get_init() == True

    assert game.state is None

    # Test that the display window was set up
    screen_info = pygame.display.Info()
    assert screen_info.current_w == 1980
    assert screen_info.current_h == 720
