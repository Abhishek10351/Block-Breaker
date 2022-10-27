import arcade
import arcade.gui
from arcade.pymunk_physics_engine import PymunkPhysicsEngine as physics_engine
from constants import *
import pymunk

class Level1(arcade.View):
    def __init__(self):
        super().__init__()
        self.physics_engine = None
        self.paddle = None
        self.player = None
        self.launched = False
        

    def setup(self):
        self.physics_engine = physics_engine()
        self.paddle = arcade.Sprite("assets/puzzlepack/paddle.png", scale=0.20,
                                    center_y=20, center_x=SCREEN_WIDTH/2, hit_box_algorithm="Detailed")
        self.player = arcade.Sprite("assets/puzzlepack/ballBlue.png", scale=0.75, center_x=SCREEN_WIDTH/2, center_y=self.paddle.top)
        self.player.boundary_left = 0
        self.tilemap = arcade.TileMap(
            "assets/map.tmj", hit_box_algorithm="Detailed")
        self.blocks = self.tilemap.sprite_lists["base"]

        self.physics_engine.add_sprite_list(
            self.blocks, collision_type="wall", body_type=physics_engine.STATIC, friction=0)
        self.physics_engine.add_sprite(
            self.player, collision_type="player", body_type=physics_engine.DYNAMIC, moment_of_inertia=float("inf"), friction=0)
        self.physics_engine.add_sprite(
            self.paddle, body_type=physics_engine.KINEMATIC, friction=0)
        
        
        self.physics_engine.set_horizontal_velocity(self.player, 80)

    def on_update(self, delta_time):
        for i in arcade.check_for_collision_with_list(self.player, self.blocks):
            self.player.velocity = (self.player.velocity[0]*5, self.player.velocity[1]*5)
            self.physics_engine.set_velocity(self.player, (self.player.velocity[0], self.player.velocity[1]))
            #self.physics_engine.apply_force(self.player, (self.player.velocity[0], -self.player.velocity[1]))
            i.kill()

        if not self.launched:
            if self.player.right >= self.paddle.right:
                self.physics_engine.set_horizontal_velocity(self.player, -80)
            elif self.player.left <= self.paddle.left:
                self.physics_engine.set_horizontal_velocity(self.player, 80)
        self.paddle.update()
        self.physics_engine.set_position(self.paddle, self.paddle.position)
        #self.physics_engine.set_position(self.player, self.player.position)
        self.player.update()
        self.physics_engine.step()

    def on_draw(self):
        self.clear()
        self.blocks.draw()
        self.paddle.draw()
        self.player.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if not self.launched:
                self.physics_engine.apply_force(self.player, (0, 50000))
                #self.physics_engine.set_velocity(self.player, (0,500))
            # else:
            #     self.physics_engine.apply_force(self.player, (0,50000))
            self.launched=True
        
        if self.launched:
            if key == arcade.key.RIGHT:
                self.paddle.change_x = 5
            if key == arcade.key.LEFT:
                self.paddle.change_x = -5

    def on_key_release(self, key, modifiers):
        if self.launched:
            if key == arcade.key.RIGHT:
                self.paddle.change_x = 0
            if key == arcade.key.LEFT:
                self.paddle.change_x = 0
