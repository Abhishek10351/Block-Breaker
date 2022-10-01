import arcade
import arcade.gui
from constants import *
import styles
from views import levelselection


class Menu(arcade.View):
    def __init__(self):
        super().__init__()
        self.start_screen = arcade.gui.UIBoxLayout(space_between=20)
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        start_button = arcade.gui.UIFlatButton(
            text="Start Game", width=200, style=styles.dark_button)
        start_button.on_click = self.on_start_button_click
        self.start_screen.add(start_button)
        how_to_play = arcade.gui.UIFlatButton(
            text="How to Play", width=200, style=styles.dark_button)
        how_to_play.on_click = self.on_how_to_play_click
        self.start_screen.add(how_to_play)
        settings_button = arcade.gui.UIFlatButton(
            text="Settings", width=200, style=styles.dark_button)
        settings_button.on_click = self.on_settings_button_click
        self.start_screen.add(settings_button)
        quit_button = arcade.gui.UIFlatButton(
            text="Exit", width=200, style=styles.danger_button)
        self.start_screen.add(quit_button)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.start_screen)
        )

        @quit_button.event
        def on_click(self, event):
            arcade.exit()

    def on_settings_button_click(self, event):
        pass

    def on_start_button_click(self, event):
        self.window.show_view(levelselection.LevelSelection())

    def on_how_to_play_click(self, event):
        self.window.show_view(self.window.views["HowToPlay"])

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()
