import arcade
import arcade.gui
from constants import *
import styles


class LevelUpView(arcade.View):
    """ View to show when a level is completed """

    def __init__(self):
        super().__init__()
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    @property
    def message(self):
        return f"You have completed level {self.window.current_level}.\nClick to continue."

    @property
    def text(self):
        return arcade.Text(self.message, 100, 400, bold=True, width=300,
                           font_name="Kenney Future Narrow", font_size=40, multiline=True)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = self.window.views["Menu"]
        self.window.show_view(game_view)
