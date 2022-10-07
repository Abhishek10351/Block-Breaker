
import pathlib
import arcade
import arcade.gui
from constants import *
import views
import styles
from window import Window
import pyglet.image

if __name__ == "__main__":
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    # window.set_icon(pyglet.image.load(
    #   'assets'))
    window.views = {"Menu": views.Menu(), "LevelUp": views.LevelUpView(
    ), "GameOver": views.GameOverView(), "HowToPlay": views.HowToPlay()}
    window.show_view(window.views["Menu"])
    window.levels = [getattr(views.levels, i)()
                     for i in dir(views.levels) if i.startswith("Level")]
    arcade.set_background_color(arcade.color.SKY_BLUE)
    arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
    arcade.run()
