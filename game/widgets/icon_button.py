import arcade
import arcade.gui
from constants import UI_PATH

ICONS_PATH = UI_PATH / "icons"


NORMAL = ICONS_PATH / "normal"
HOVER = ICONS_PATH / "hover"


class IconButton(arcade.gui.UITextureButton):
    def __init__(self, bg, hover, scale=0.75, **kwargs):
        self.bg_icon = NORMAL / bg
        self.hover_icon = HOVER / hover
        super().__init__(
            scale=scale,
            texture=arcade.load_texture(self.bg_icon),
            texture_hovered=arcade.load_texture(self.hover_icon),
            **kwargs
        )
