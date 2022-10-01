import arcade
import pyglet.media


class Window(arcade.Window):
    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.sound = True
        self.music = True
        self.total_levels = 2
        self.levels_completed = 0  # the last level completed
        self.current_level = 1  # the level currently played
        self.bg_music = pyglet.media.Player()
        self.completed = False

    def on_update(self, delta_time):
        self.total_time += delta_time
