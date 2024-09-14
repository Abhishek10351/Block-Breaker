import arcade
import arcade.gui
from constants import *
import pymunk
from pathlib import Path


class Level1(arcade.View):
    def __init__(self):
        super().__init__()

        self.scene = arcade.Scene()
        self.score: int = 0
        self.reset_score = True

        self.player = None

        self.tile_map = None
        self.end_of_map = 0

        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(':resources:sounds/hurt5.wav')
        self.brick_hit = arcade.load_sound(':resources:sounds/hit5.wav')
        self.game_complete = arcade.load_sound(':resources:sounds/upgrade5.wav')

        arcade.set_background_color(arcade.color.BALL_BLUE)

    def setup(self):
        self.score = 0
        self.launched = False

        map_name = 'map.tmj'
        map_name = ASSETS_PATH / "levels" / map_name
        layer_options = {
            "tiles": {
                "use_spatial_hash": True
            },
        }

        self.tile_map = arcade.load_tilemap(
            map_file=map_name, scaling=1, layer_options=layer_options)
        self.scene = arcade.Scene.from_tilemap(tilemap=self.tile_map)

        self.end_of_map = self.tile_map.width * 4 * 16

        self.scene.add_sprite_list("Player")
        # self.player_path
        # add a  pad to hit the ball
        self.player_path = f"assets/puzzlepack/paddle.png"
        self.player = arcade.Sprite(
            self.player_path, scale=0.20)
        self.player.center_x = self.window.width/2 - 100             # left to right
        self.player.center_y = 50
        self.scene.add_sprite('Player', self.player)

        # add a ball to hit
        self.scene.add_sprite_list("Ball")
        self.ball_path = f"assets/puzzlepack/ballBlue.png"
        self.ball_sprite = arcade.Sprite(
            self.ball_path, scale=0.75)
        self.ball_sprite.center_x = self.player.center_x          # left to right
        self.ball_sprite.center_y = self.player.top + \
            self.ball_sprite.height/2  # up and down
        self.scene.add_sprite('Ball', self.ball_sprite)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        if self.reset_score:
            self.score = 0
        self.reset_score = True

        self.physics_engine = arcade.PymunkPhysicsEngine()
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list("Player"), body_type=arcade.PymunkPhysicsEngine.KINEMATIC, elasticity=1.0, friction=1.0, mass=1, moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF)
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list("Ball"), damping=1, friction=0, mass=2, elasticity=1, moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF)

        # make tiles static
        self.physics_engine.add_sprite_list(self.scene.get_sprite_list(
            "tiles"), body_type=arcade.PymunkPhysicsEngine.STATIC, damping=0.0, mass=10, friction=1.0, elasticity=1.0)
        self.walls = self.create_walls()
        self.scene.add_sprite_list("walls", sprite_list=self.walls)
        self.physics_engine.add_sprite_list(self.scene.get_sprite_list(
            "walls"), body_type=arcade.PymunkPhysicsEngine.STATIC, damping=0.0, mass=10, friction=1.0, elasticity=1.0)

        self.physics_engine.set_horizontal_velocity(self.ball_sprite, 100)

    def on_update(self, delta_time):

        self.physics_engine.step(1/60)
        if self.scene.get_sprite_list("tiles").__len__() == 0:
            arcade.play_sound(self.game_complete)
            self.setup()
            # show game complete screen
            self.window.show_view(self.window.views["LevelUp"])
        if self.ball_sprite.bottom <= 0:
            self.launched = False
            arcade.play_sound(self.game_over)
            self.setup()
        if not self.launched:
            # change the direction of the ball if it goes left or right of paddle
            if self.ball_sprite.right >= self.player.right:
                self.physics_engine.set_horizontal_velocity(
                    self.ball_sprite, -100)
            elif self.ball_sprite.left <= self.player.left:
                self.physics_engine.set_horizontal_velocity(
                    self.ball_sprite, 100)
        brick_hit_list = arcade.check_for_collision_with_list(
            self.ball_sprite, self.scene.get_sprite_list("tiles"))
        for brick in brick_hit_list:
            brick.remove_from_sprite_lists()
            arcade.play_sound(self.brick_hit)
            self.score += 10
        if self.player.right >= self.window.width:
            self.physics_engine.set_horizontal_velocity(self.player, 0)
        if self.player.left <= 0:
            self.physics_engine.set_horizontal_velocity(self.player, 0)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.scene.draw_hit_boxes()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.setup()
        if key == arcade.key.SPACE:
            if not self.launched:
                self.physics_engine.apply_force(self.ball_sprite, (0, 20000))
                arcade.play_sound(self.jump_sound)
            self.launched = True
        if key == arcade.key.LEFT:
            self.physics_engine.set_horizontal_velocity(
                self.player, -400) if self.player.left > 0 else None
        if key == arcade.key.RIGHT:
            self.physics_engine.set_horizontal_velocity(
                self.player, 400)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.physics_engine.set_horizontal_velocity(self.player, 0)


    def create_walls(self):
        # Create the walls on the right and left
        walls = arcade.SpriteList()
        left_wall = arcade.SpriteSolidColor(
            10, self.window.height, arcade.color.BALL_BLUE)
        left_wall.center_x = -5
        left_wall.center_y = SCREEN_HEIGHT/2
        walls.append(left_wall)
        right_wall = arcade.SpriteSolidColor(
            10, self.window.height, arcade.csscolor.RED)
        right_wall.center_x = SCREEN_WIDTH+5
        right_wall.center_y = SCREEN_HEIGHT/2
        walls.append(right_wall)
        top_wall = arcade.SpriteSolidColor(
            self.window.width, 10, arcade.csscolor.GREEN)
        top_wall.center_x = SCREEN_WIDTH/2
        top_wall.center_y = SCREEN_HEIGHT+5
        walls.append(top_wall)
        return walls
