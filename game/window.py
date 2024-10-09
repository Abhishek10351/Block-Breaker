import arcade
import pyglet.media
from pathlib import Path
from constants import MAP_PATH


class Window(arcade.Window):
    def __init__(self, width, height):
        """
        Set up the application.
        """
        super().__init__(width, height, title="Block Breaker", center_window=True)
        self.clock = arcade.clock.Clock()
        self.sound = True
        self.music = True
        self.current_level = 1  # the level currently played
        self.bg_music = pyglet.media.Player()
        self.completed = False

    @property
    def total_levels(self):
        return len(list(MAP_PATH.glob("level_*.tmx")))

    def on_update(self, delta_time):
        self.clock.tick(delta_time)
