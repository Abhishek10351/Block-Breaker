import arcade
import arcade.gui
from arcade.gui import UIImage, UIBoxLayout
from constants import *


class StarLayout(UIBoxLayout):
    def __init__(self, stars: int = 3):
        super().__init__(vertical=False, space_between=-10)
        self.stars = stars

        self.outline_path = STARS_PATH / "star_outline.png"
        self.filled_path = STARS_PATH / "star.png"
        self.star_paths = [
            self.outline_path,
            self.filled_path,
        ]
        rotate_angle = 20
        angles = [-rotate_angle, 0, rotate_angle]
        scale = 0.60
        for i in range(3):
            img_no = 1 if i < self.stars else 0
            texture = arcade.load_texture(self.star_paths[img_no])
            texture.size = (texture.width * scale, texture.height * scale)
            star = UIImage(
                texture=texture,
                center_x=100,
                center_y=100,
            )
            star.angle = angles[i]

            self.add(star)

    def do_layout(self):

        super().do_layout()

        for i, child in enumerate(self.children):
            if i == 1:
                new_rect = child.rect.align_center_y(self.center_y + 20)
                child.rect = new_rect
