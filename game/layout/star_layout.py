import arcade
import arcade.gui
from arcade.gui import UIAnchorLayout, UILayout, UIView
from constants import *
import math
from arcade.gui import UIImage, UIView
from PIL import Image


class StarImage(UIImage):

    def __init__(self, *, angle: float = 0, **kwargs):
        self.angle = angle
        super().__init__(**kwargs)


class StarLayout(UILayout):
    def __init__(self, stars: int = 3):
        super().__init__(padding=10, align="center", direction="row")
        self.stars = stars
        self.outline_path = STARS_PATH / "star_outline.png"
        self.outline_depth_path = STARS_PATH / "star_outline_depth.png"
        self.filled_path = STARS_PATH / "star.png"
        # self.outline_texture = arcade.Texture(self.outline_path)
        self.star_paths = [
            self.outline_path,
            self.outline_depth_path,
            self.filled_path,
        ]
        rotate_angle = 20
        angles = [-rotate_angle, 0, rotate_angle]
        scales = [0.60, 0.60, 0.60]
        for i in range(3):
            img_no = 2 if i < self.stars else 0
            texture = arcade.load_texture(self.star_paths[img_no])
            texture.size = (texture.width * scales[i], texture.height * scales[i])
            star = StarImage(
                texture=texture,
                center_x=100,
                center_y=100,
                angle=angles[i],
            )

            self.add(star)

    def do_layout(self):

        x_diff = 60
        y_diff = 20

        y_loc = self.center_y + 300

        for i, child in enumerate(self.children):
            if i == 0:
                new_rect = child.rect.align_center((self.center_x - x_diff, y_loc))
                child.rect = new_rect
            elif i == 1:
                new_rect = child.rect.align_center((self.center_x, y_loc + y_diff))
                child.rect = new_rect
            elif i == 2:
                new_rect = child.rect.align_center((self.center_x + x_diff, y_loc))
                child.rect = new_rect
