import arcade
import arcade.gui
from constants import *
import styles


class LevelSelection(arcade.View):
    def __init__(self):
        super().__init__()
        self.buttons = [arcade.gui.UIFlatButton(
            text=i+1, width=60, style=styles.primary_button) for i in range(self.window.total_levels)]
        self.levels = arcade.gui.UIBoxLayout(
            x=10, y=500, vertical=False, space_between=20, children=self.buttons)

        for i in self.buttons:
            i.on_click = self.on_click

        self.manager = arcade.gui.UIManager()
        self.manager.add(self.levels)
        self.manager.enable()

    def on_click(self, event):
        button = event.source
        self.window.current_level = button.text
        game_level = self.window.levels[button.text - 1]
        if self.window.current_level <= (self.window.levels_completed+1):
            game_level.setup()
            self.window.show_view(game_level)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.clear()
        self.manager.disable()

    def on_show_view(self):
        self.clear()
        self.manager.enable()
