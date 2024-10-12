import arcade
import arcade.gui
from constants import *
import styles
from widgets import IconButton
from layout import StarLayout


class LevelUpView(arcade.View):
    """View to show when a level is completed"""

    def __init__(self):
        self.gui_manager = arcade.gui.UIManager()
        self.icons_path = UI_PATH / "icons"

        self.icons = [
            "next.png",
            "play.png",
            "levels.png",
        ]
        self.row_layout = arcade.gui.UIBoxLayout(vertical=True, space_between=50)

        self.button_layout = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        self.buttons = [IconButton(i, i) for i in self.icons]
        for i, j in enumerate(self.buttons):
            if i == 0:
                j.on_click = self.next
            elif i == 1:
                j.on_click = self.play
            elif i == 2:
                j.on_click = self.levels

        for i in self.buttons:
            self.button_layout.add(i)

        self.highscore_label = arcade.gui.UILabel(
            f"Highscore: 1000", font_size=24, font_name="Kenney Future"
        )

        self.stars = 3
        self.star_layout = StarLayout(self.stars)
        # self.star_layout.with_background(
        #     color=arcade.color.Color(237, 119, 31, 200),
        # )
        self.anchor_layout = arcade.gui.UIAnchorLayout()

        self.row_layout.add(self.star_layout)
        self.row_layout.add(self.highscore_label)
        self.row_layout.add(self.button_layout)

        self.anchor_layout.add(self.row_layout, anchor_y="top", align_y=-200)

        self.gui_manager.add(self.anchor_layout)

        super().__init__()

    @property
    def message(self):
        return (
            f"You have completed level {self.window.current_level}.\nClick to continue."
        )

    def on_draw(self):
        """Draw this view"""
        self.clear()
        self.gui_manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """If the user presses the mouse button, re-start the game."""
        game_view = self.window.views["Menu"]
        self.window.show_view(game_view)

    def on_show_view(self):
        self.gui_manager.enable()

    def on_hide_view(self):
        self.gui_manager.disable()

    def play(self, event):
        self.window.show_view(self.window.views["Level"])

    def next(self, event):
        total_levels = self.window.total_levels
        if self.window.current_level < total_levels:
            self.window.current_level += 1
            self.window.show_view(self.window.views["Level"])
        else:
            self.window.show_view(self.window.views["Menu"])

    def levels(self, event):
        self.window.show_view(self.window.views["LevelSelection"])
