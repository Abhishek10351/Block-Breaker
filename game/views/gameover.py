import arcade
import arcade.gui
from constants import *
import styles


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        super().__init__()
        # self.texture = arcade.load_texture(
        #     "assets/images/background.jpg")
        # arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    @property
    def message(self):
        return f"You have lost level {self.window.current_level}.\nClick to continue."

    @property
    def text(self):
        return arcade.Text(self.message, 100, 400, bold=True, width=300,
                           font_name="Kenney Future Narrow", font_size=40, multiline=True)

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
        self.text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """ If the user presses the mouse button, re-start the game. """

        game_view = self.window.views["StartScreen"]
        self.window.show_view(game_view)
