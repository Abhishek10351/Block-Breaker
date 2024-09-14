
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
    window.levels = [getattr(views.levels, i)()
                     for i in dir(views.levels) if i.startswith("Level")]
    window.levels[0].setup()
    window.show_view(window.levels[0])
    arcade.set_background_color(arcade.color.SKY_BLUE)
    arcade.run()
