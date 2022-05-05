from enum import Enum

import game_constants as gc

from fish_animation import FishAnimation


class Direction(Enum):
    """
    Simple direction enum for left and right.
    """
    LEFT = 0
    RIGHT = 1


class Player:
    """
    Player class for the fish!
    """
    MOVEMENT_SPEED = 5.0
    PLAYER_LIVES = 3
    
    def __init__(self, spritesheet_path):
        self.player_scale = 0.10
        self.left_animation = FishAnimation(spritesheet_path, scale=self.player_scale)
        self.right_animation = FishAnimation(spritesheet_path, flip=True, scale=self.player_scale)
        self.current_animation = None
        self.Iseconds = 0
        self.direction = Direction.LEFT
        if self.direction == Direction.LEFT:
            self.current_animation = self.left_animation
        else:
            self.current_animation = self.right_animation

        self.lives = Player.PLAYER_LIVES

    def draw(self):
        self.current_animation.draw()
        self.right_animation.scale = self.player_scale
        self.left_animation.scale = self.player_scale
    def update(self, delta_time):
        if self.current_animation.center_x + self.current_animation.change_x >= gc.SCREEN_WIDTH :
            self.current_animation.center_x = 1
        if self.current_animation.center_y + self.current_animation.change_y >= gc.SCREEN_HEIGHT - 45 :
            self.current_animation.change_y = 0
        if self.current_animation.center_x + self.current_animation.change_x <= 0:
            self.current_animation.center_x = gc.SCREEN_WIDTH - 1
        if self.current_animation.center_y + self.current_animation.change_y <= 0:
            self.current_animation.change_y = 0

        self.current_animation.center_x += self.current_animation.change_x
        self.current_animation.center_y += self.current_animation.change_y

        self.current_animation.on_update(delta_time)
    def respawn(self):
        self.current_animation.center_x = gc.SCREEN_WIDTH/2
        self.current_animation.center_y = gc.SCREEN_HEIGHT/2
        self.Iseconds = 3
        self.lives -= 1
    def change_direction(self, new_direction):
        """
        Used to update the animation according to the direction.
        :param new_direction: The new direction.
        :return: None
        """
        old_direction = self.direction
        if old_direction == new_direction:
            return
        self.direction = new_direction
        if self.direction == Direction.LEFT:
            self.left_animation.center_x = self.current_animation.center_x
            self.left_animation.center_y = self.current_animation.center_y
            self.current_animation = self.left_animation
        else:
            self.right_animation.center_x = self.current_animation.center_x
            self.right_animation.center_y = self.current_animation.center_y            
            self.current_animation = self.right_animation      
