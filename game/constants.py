"""
All the constants needed for the game
"""

from pathlib import Path

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


ASSETS_PATH = Path(".").parent / "assets"
MAP_PATH = ASSETS_PATH / "levels"


TILE_SCALING = 1.2

SPRITE_PIXEL_SIZE = 32
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING


# LAYER_NAME_SOLID = "Solid"
# LAYER_NAME_BRICKS = "Bricks"
# LAYER_NAME_BALL = "Ball"
# LAYER_NAME_PADDLE = "Paddle"
# LAYER_NAME_POWERUPS = "Powerups"
