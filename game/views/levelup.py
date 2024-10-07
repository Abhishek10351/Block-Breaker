import arcade
import arcade.gui
from constants import *
import styles

from layout import StarLayout


class LevelUpView(arcade.View):
    """View to show when a level is completed"""

    def __init__(self):
        self.gui_manager = arcade.gui.UIManager()

        self.stars = 3

        self.star_layout = StarLayout(self.stars)
        self.star_anchor_layout = arcade.gui.UIAnchorLayout(
            anchor_x="center", anchor_y="center"
        )
        self.star_anchor_layout.add(self.star_layout)

        self.gui_manager.add(self.star_anchor_layout)

        super().__init__()

    @property
    def message(self):
        return (
            f"You have completed level {self.window.current_level}.\nClick to continue."
        )

    @property
    def text(self):
        return arcade.Text(
            self.message,
            300,
            400,
            bold=True,
            width=500,
            anchor_x="center",
            font_name="Kenney Future",
            font_size=40,
            multiline=True,
        )

    def on_draw(self):
        """Draw this view"""
        self.clear()
        self.text.draw()
        self.gui_manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """If the user presses the mouse button, re-start the game."""
        game_view = self.window.views["Menu"]
        self.window.show_view(game_view)
