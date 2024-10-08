import arcade
import arcade.gui
from constants import *
import styles


class LevelSelection(arcade.View):
    def __init__(self):
        super().__init__()
        self.buttons = [
            arcade.gui.UIFlatButton(text=str(i + 1), width=60)
            for i in range(self.window.total_levels)
        ]
        self.grid_layout = arcade.gui.UIGridLayout(
            padding=10,
            horizontal_spacing=10,
            vertical_spacing=10,
            column_count=5,
            row_count=2,
        )
        for i in self.buttons:
            level = int(i.text)
            column = level % 5
            row = level // 5
            self.grid_layout.add(i, column, row)

        for i in self.buttons:
            i.on_click = self.on_click

        self.manager = arcade.gui.UIManager()
        self.layout = arcade.gui.UIAnchorLayout()
        self.layout.add(self.grid_layout)
        self.manager.add(self.layout)
        self.manager.enable()

    def on_click(self, event):
        button = event.source
        self.window.current_level = int(button.text)
        self.window.views["Level"].setup()
        self.window.show_view(self.window.views["Level"])

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.clear()
        self.manager.disable()

    def on_show_view(self):
        self.clear()
        self.manager.enable()
