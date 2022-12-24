import arcade
import arcade.gui
from constants import *
import pymunk


class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, filename, **kwargs):
        super().__init__(filename, center_x=pymunk_shape.body.position.x,
                         center_y=pymunk_shape.body.position.y, **kwargs)
        self.pymunk_shape = pymunk_shape

    def update(self):
        if not (((self.left + self.change_x) < 0) or (self.right+self.change_x > SCREEN_WIDTH)):
            self.pymunk_shape.body.position += (
                self.change_x, 0)
        self.center_x = self.pymunk_shape.body.position.x
        self.center_y = self.pymunk_shape.body.position.y


class CircleSprite(arcade.Sprite):
    def __init__(self, filename, pymunk_shape, **kwargs):
        super().__init__(filename, center_x=pymunk_shape.body.position.x,
                         center_y=pymunk_shape.body.position.y, **kwargs)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2
        self.pymunk_shape = pymunk_shape


class Level1(arcade.View):
    def __init__(self):
        super().__init__()
        self.space = None
        self.paddle = None
        self.player = None
        self.launched = False

    def setup(self):
        self.clear()
        self.space = pymunk.Space()
        #self.space.damping = 1
        #self.space.friction = 0

        paddle_mass = 5.0
        paddle_moment = pymunk.moment_for_box(paddle_mass, size=(104.0, 28.0))
        paddle_body = pymunk.Body(
            paddle_mass, paddle_moment, body_type=pymunk.Body.KINEMATIC)
        paddle_body.position = (SCREEN_WIDTH/2, 20)
        paddle_shape = pymunk.Poly.create_box(
            paddle_body, size=(104.0, 28.0))
        paddle_shape.elasticity = 1
        self.space.add(paddle_body, paddle_shape)
        self.paddle = PhysicsSprite(
            paddle_shape, "assets/puzzlepack/paddle.png", scale=0.20, hit_box_algorithm="Detailed")

        player_mass = 1.0
        player_moment = pymunk.moment_for_circle(paddle_mass, 0, 8.25)
        player_body = pymunk.Body(
            player_mass, player_moment, body_type=pymunk.Body.DYNAMIC)
        player_body.position = (SCREEN_WIDTH/2, self.paddle.top+8.25)

        player_shape = pymunk.Circle(
            player_body, 8.25, player_body.position)
        player_shape.friction = 0
        player_shape.elasticy = 1
        self.player = CircleSprite("assets/puzzlepack/ballBlue.png", player_shape,
                                   scale=0.75, hit_box_algorithm="Detailed")
        self.player.pymunk_shape.body.velocity = (80, 0)
        self.space.add(player_body, player_shape)

        self.tilemap = arcade.TileMap(
            "assets/map.tmj", hit_box_algorithm="Detailed", scaling=0.75)
        self.blocks = self.tilemap.sprite_lists["tiles"]
        self.tiles = arcade.SpriteList()
        for tile in self.blocks:
            mass = 10.0
            moment = pymunk.moment_for_box(mass, size=(tile.width, tile.height))
            body = pymunk.Body(
                mass, moment, body_type=pymunk.Body.STATIC)
            body.position = (tile.center_x, tile.center_y)
            shape = pymunk.Poly.create_box(
                body, size=(tile.width, tile.height))
            #shape.elasticity = 1
            tile.pymunk_shape = shape
            self.space.add(body, shape)
            self.tiles.append(tile)

    def on_update(self, delta_time):
        if not self.launched:
            if self.player.right >= self.paddle.right:
                self.player.pymunk_shape.body.velocity = (-80, 0)
            elif self.player.left <= self.paddle.left:
                self.player.pymunk_shape.body.velocity = (80, 0)
        else:
            for i in arcade.check_for_collision_with_list(self.player, self.tiles):
                # if i.pymunk_shape in self.space.shapes:
                #     self.space.remove(i.pymunk_shape)
                # if i.pymunk_shape.body in self.space.bodies:
                #     self.space.remove(i.pymunk_shape.body)
                # #i.kill()
                # self.tiles.remove(i)
                print("Collision", i)
        self.player.center_x = self.player.pymunk_shape.body.position.x
        self.player.center_y = self.player.pymunk_shape.body.position.y
        self.player.update()
        self.paddle.update()

        self.space.step(1/60)

    def on_draw(self):
        self.clear()
        self.player.draw()
        self.paddle.draw()
        self.blocks.draw()
        self.tiles.draw()

    def on_key_press(self, symbol, modifiers):
        if not self.launched:
            if symbol == arcade.key.SPACE:
                self.player.pymunk_shape.body.apply_force_at_local_point(
                    [0, 20000], [self.player.center_x, self.player.bottom])
                self.launched = True
        else:
            if symbol in [arcade.key.RIGHT, arcade.key.NUM_RIGHT]:
                self.paddle.change_x = 10
            elif symbol in [arcade.key.LEFT, arcade.key.NUM_LEFT]:
                self.paddle.change_x = -10

    def on_key_release(self, symbol, modifiers):
        if symbol in [arcade.key.RIGHT, arcade.key.LEFT, arcade.key.NUM_RIGHT, arcade.key.NUM_LEFT]:
            self.paddle.change_x = 0
