import arcade
import arcade.gui
from constants import *
import styles


class HowToPlay(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        self.message ="""
        Hello, Player! Welcome to Block Breaker.
        It is quite a simple Game, all you have to do is to break all the blocks using your Paddle
        and collect items and powerups falling from them.
        Use the arrow keys to move the paddle right or left to shoot the ball and later stop it from falling.
        """

        self.text = arcade.Text(self.message, 100, 400, bold=True, width=400,  multiline=True,
                                color=arcade.color.RED, font_size=16, align="center", font_name="Kenney Future Narrow")

    def on_draw(self):
        self.clear()
        self.text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """ If the user presses the mouse button, re-start the game. """

        game_view = self.window.views["Menu"]
        self.window.show_view(game_view)
