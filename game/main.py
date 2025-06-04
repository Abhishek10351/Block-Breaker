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
    window.views = {
        "Menu": views.Menu(),
        "LevelUp": views.LevelUpView(),
        "GameOver": views.GameOverView(),
        "HowToPlay": views.HowToPlay(),
        "Level": views.Level(),
        "LevelSelection": views.LevelSelection(),
        "Settings": views.SettingsView(),
    }
    window.views["Level"].setup()

    window.show_view(window.views["Menu"])

    arcade.set_background_color(arcade.color.SKY_BLUE)
    arcade.run()
