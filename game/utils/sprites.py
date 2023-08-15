from pathlib import Path

import pygame


def draw_sprite(
    sprite_sheet: Path, col: int, row: int, width: int, height: int, offset: int = 2
) -> pygame.Surface:
    """Draw a sprite clipped from a sprite sheet to the screen."""
    entire_sheet = pygame.image.load(str(sprite_sheet))

    x = col * (width + offset) + offset
    y = row * (height + offset) + offset
    rect = pygame.Rect(x, y, width, height)

    return entire_sheet.subsurface(rect)
