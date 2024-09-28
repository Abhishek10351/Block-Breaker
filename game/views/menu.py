import arcade
import arcade.gui
from constants import *
import styles
from views import levelselection


class Menu(arcade.View):
    def __init__(self):
        super().__init__()
        self.start_screen = arcade.gui.UIBoxLayout(space_between=20)
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200, style=arcade.gui.UIFlatButton.STYLE_BLUE)
        start_button.on_click = self.on_start_button_click
        self.start_screen.add(start_button)
        how_to_play = arcade.gui.UIFlatButton(text="How to Play", width=200,height=60, style=arcade.gui.UIFlatButton.STYLE_BLUE)
        how_to_play.on_click = self.on_how_to_play_click
        self.start_screen.add(how_to_play)
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200, style=arcade.gui.UIFlatButton.STYLE_BLUE)
        settings_button.on_click = self.on_settings_button_click
        self.start_screen.add(settings_button)
        quit_button = arcade.gui.UIFlatButton(text="Exit", width=200, style=arcade.gui.UIFlatButton.STYLE_RED)
        self.start_screen.add(quit_button)

        self.manager = arcade.gui.UIManager()
        self.layout = arcade.gui.UIAnchorLayout()
        self.layout.add(self.start_screen)
        self.manager.add(self.layout)

        self.manager.enable()

        @quit_button.event
        def on_click(event):
            arcade.exit()

    def on_settings_button_click(self, event):
        pass

    def on_start_button_click(self, event):
        self.window.show_view(self.window.views["LevelSelection"])

    def on_how_to_play_click(self, event):
        self.window.show_view(self.window.views["HowToPlay"])

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.clear()
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()
