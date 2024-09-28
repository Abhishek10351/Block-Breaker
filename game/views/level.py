import arcade
import arcade.gui
from constants import *
import pymunk
from pathlib import Path
import math


class Level(arcade.View):
    def __init__(self):
        super().__init__()

        self.scene = arcade.Scene()
        self.score: int = 0
        self.reset_score = True

        self.paddle = None

        self.tile_map = None
        self.end_of_map = 0

        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.brick_hit = arcade.load_sound(":resources:sounds/hit5.wav")
        self.game_complete = arcade.load_sound(":resources:sounds/upgrade5.wav")

        arcade.set_background_color(arcade.color.BALL_BLUE)

    def setup(self):
        # ! TODO :  ADD A MAXIMUM VELOCITY TO THE BALL
        # ! (WHEN IT BECOMES TOO FAST)
        self.score = 0
        self.launched = False

        map_name = f"level_{self.window.current_level}.tmx"
        map_name = ASSETS_PATH / "levels" / map_name
        layer_options = {
            "tiles": {"use_spatial_hash": True},
        }

        self.map_offset = (100, 300)

        self.tile_map = arcade.load_tilemap(
            map_file=map_name,
            scaling=TILE_SCALING,
            layer_options=layer_options,
            offset=self.map_offset,
            hit_box_algorithm=arcade.hitbox.PymunkHitBoxAlgorithm(detail=10),
        )
        self.scene = arcade.Scene.from_tilemap(tilemap=self.tile_map)
        # self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        self.scene.add_sprite_list("Paddle")
        self.paddle_path = f"assets/puzzlepack/paddle.png"
        self.paddle = arcade.Sprite(self.paddle_path, scale=0.20)
        self.paddle.center_x = self.window.width / 2
        # self.paddle.center_x += self.paddle.width / 2
        self.paddle.center_y = 50
        self.scene.add_sprite("Paddle", self.paddle)

        # add a ball to hit
        self.scene.add_sprite_list("Ball")
        self.ball_path = f"assets/puzzlepack/ballBlue.png"
        self.ball = arcade.Sprite(self.ball_path, scale=0.75)
        self.ball.center_x = self.paddle.center_x
        self.ball.center_y = self.paddle.top + self.ball.height / 2
        self.scene.add_sprite("Ball", self.ball)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        if self.reset_score:
            self.score = 0
        self.reset_score = True

        self.physics_engine = arcade.PymunkPhysicsEngine()
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list("Paddle"),
            body_type=arcade.PymunkPhysicsEngine.KINEMATIC,
            elasticity=1.0,
            friction=1.0,
            mass=1,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="paddle",
        )
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list("Ball"),
            damping=1,
            friction=0,
            mass=2,
            elasticity=1,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="ball",
        )

        self.shield = self.create_shield()
        self.scene.add_sprite_list("shield", sprite_list=self.shield)
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list("shield"),
            body_type=arcade.PymunkPhysicsEngine.STATIC,
            damping=0.0,
            mass=10,
            friction=1.0,
            elasticity=1.0,
        )

        # make tiles static
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list("tiles"),
            body_type=arcade.PymunkPhysicsEngine.STATIC,
            damping=0.0,
            mass=10,
            friction=1.0,
            elasticity=1.0,
            collision_type="tile",
        )
        self.walls = self.create_walls()
        self.scene.add_sprite_list("walls", sprite_list=self.walls)
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list("walls"),
            body_type=arcade.PymunkPhysicsEngine.STATIC,
            damping=0.0,
            mass=10,
            friction=1.0,
            elasticity=1.0,
            collision_type="walls",
        )

        self.physics_engine.add_collision_handler(
            "ball", "tile", begin_handler=self.ball_tile_collision
        )

        self.physics_engine.add_collision_handler(
            "walls", "paddle", pre_handler=self.test
        )
        self.physics_engine.set_horizontal_velocity(self.ball, 100)

    def test(self, wall, paddle, arbiter, space, data):
        self.physics_engine.set_horizontal_velocity(self.paddle, 0)
        return False
        return True

    def on_update(self, delta_time):

        max_velocity = 500
        # if velocity of ball becomes large, reduce it to a constant value
        ball_phys = self.physics_engine.get_physics_object(self.ball).body
        if abs(ball_phys.velocity.x) > max_velocity:
            self.physics_engine.set_horizontal_velocity(self.ball, max_velocity)    
        if abs(ball_phys.velocity.y) > max_velocity:
            self.physics_engine.set_velocity(self.ball, (ball_phys.velocity.x, max_velocity))
        if self.scene.get_sprite_list("tiles").__len__() == 0:
            arcade.play_sound(self.game_complete)
            self.setup()
            # show game complete screen
            self.window.show_view(self.window.views["LevelUp"])
        if self.ball.bottom <= 0:
            self.launched = False
            arcade.play_sound(self.game_over)
            self.setup()
        if not self.launched:
            # change the direction of the ball if it goes left or right of paddle
            if self.ball.right >= self.paddle.right:
                self.physics_engine.set_horizontal_velocity(self.ball, -100)
            elif self.ball.left <= self.paddle.left:
                self.physics_engine.set_horizontal_velocity(self.ball, 100)
        self.physics_engine.step(1 / 60)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.scene.draw_hit_boxes(names=["tiles", "Ball"], line_thickness=1.2)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.setup()
        if key == arcade.key.SPACE:
            if not self.launched:
                self.physics_engine.apply_force(self.ball, (0, 80000))
                arcade.play_sound(self.jump_sound)
            self.launched = True
        if self.launched:
            if key == arcade.key.LEFT:
                (
                    self.physics_engine.set_horizontal_velocity(self.paddle, -800)
                    if self.paddle.left > 0
                    else None
                )
            if key == arcade.key.RIGHT:
                (
                    self.physics_engine.set_horizontal_velocity(self.paddle, 800)
                    if self.paddle.right < self.window.width
                    else None
                )

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.physics_engine.set_horizontal_velocity(self.paddle, 0)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.window.show_view(self.window.views["Menu"])

    def create_walls(self):
        walls = arcade.SpriteList()
        left_wall = arcade.SpriteSolidColor(
            10, self.window.height, arcade.color.BALL_BLUE
        )
        left_wall.center_x = -5
        left_wall.center_y = SCREEN_HEIGHT / 2
        walls.append(left_wall)
        right_wall = arcade.SpriteSolidColor(
            10, self.window.height, arcade.csscolor.RED
        )
        right_wall.center_x = SCREEN_WIDTH + 5
        right_wall.center_y = SCREEN_HEIGHT / 2
        walls.append(right_wall)
        top_wall = arcade.SpriteSolidColor(self.window.width, 10, arcade.csscolor.GREEN)
        top_wall.center_x = SCREEN_WIDTH / 2
        top_wall.center_y = SCREEN_HEIGHT + 5
        walls.append(top_wall)
        return walls

    def create_shield(self, color: arcade.color = arcade.csscolor.WHITE):
        shield = arcade.SpriteList()
        shield_sprite = arcade.SpriteSolidColor(self.window.width, 10, color)
        shield_sprite.center_x = self.window.width / 2
        shield_sprite.center_y = self.paddle.bottom - shield_sprite.height / 2
        shield.append(shield_sprite)
        return shield

    def ball_tile_collision(self, ball, tile_sprite, arbiter, space, data):
        arcade.play_sound(self.brick_hit)
        tile_sprite.remove_from_sprite_lists()
        self.score += 10
        return True
        # return False if we want to move through the tiles (as in a powerup)
