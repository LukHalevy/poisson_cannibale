from random import choices, randint

from fish_animation import FishAnimation
from player import Direction
import game_constants as gc

FISH_COLOR_TO_PATH = {
    1: "assets/2dfish/spritesheets/__cartoon_fish_06_black_idle.png",
    2: "assets/2dfish/spritesheets/__cartoon_fish_06_blue_idle.png",
    3: "assets/2dfish/spritesheets/__cartoon_fish_06_green_idle.png",
    4: "assets/2dfish/spritesheets/__cartoon_fish_06_purple_idle.png",
    5: "assets/2dfish/spritesheets/__cartoon_fish_06_red_idle.png",
}

FISH_SIZE_TO_SCALE = {
    'XXXXS': 0.08,
    'XXXS': 0.10,
    'XXS': 0.15,
    'XS': 0.20,
    'S': 0.25,
    'M': 0.30,
    'ML': 0.35,
    'L': 0.40,
    'XL': 0.60,
}

FISH_SCALE = list(FISH_SIZE_TO_SCALE.keys())





class EnemyFish(FishAnimation):
    """
    Enemy fish based on FishAnimation. Will have randomized size and colors.
    """

    SMALL_ENEMY_SPEED = 4.0
    MEDIUM_ENEMY_SPEED = 3.0
    LARGE_ENEMY_SPEED = 2.0

    def __init__(self, direction, spawn_point, player_weight):
        """
        Liste qui permet de modifier les chances qu'un poisson d'une certaine taille puisse être
        choisi au hasard. Si vous voulez qu'un taille ait moins de chance d'être choisi, diminuer le
        chiffre associé.
        """

        self.FISH_SCALE_WEIGHT = (
            -2 * ((player_weight - 0.1) ** 2) + 1,  # XXXXS
            -2 * ((player_weight - 0.2) ** 2) + 1,  # XXXS
            -2 * ((player_weight - 0.3) ** 2) + 1,  # XXS
            -2 * ((player_weight - 0.4) ** 2) + 1,  # XS
            -2 * ((player_weight - 0.5) ** 2) + 1,  # S
            -2 * ((player_weight - 0.6) ** 2) + 1,  # M
            -2 * ((player_weight - 0.7) ** 2) + 1,  # ML
            -2 * ((player_weight - 0.8) ** 2) + 1,  # L
            -2 * ((player_weight - 0.9) ** 2) + 1,  # XL
        )
        # Randomize the fish color and size
        fish_color = randint(1, 5)
        fish_scale = choices(FISH_SCALE, weights=self.FISH_SCALE_WEIGHT, k=1)
        flipped = False if direction == Direction.LEFT else True

        super().__init__(
            FISH_COLOR_TO_PATH[fish_color], 
            flipped, 
            FISH_SIZE_TO_SCALE[fish_scale[0]]
        )

        if fish_scale[0] in FISH_SCALE[0:3]:
            self.change_x = EnemyFish.SMALL_ENEMY_SPEED
        elif fish_scale[0] in FISH_SCALE[4:5]:
            self.change_x = EnemyFish.MEDIUM_ENEMY_SPEED
        else:
            self.change_x = EnemyFish.LARGE_ENEMY_SPEED

        self.direction = direction
        self.center_x = spawn_point[0]
        self.center_y = spawn_point[1]

    def update(self):
        if self.direction == Direction.LEFT:
            self.center_x += -self.change_x
        else:
            self.center_x += self.change_x

        # Are we going out of screen? If so, despawn
        if self.direction == Direction.LEFT:
            if self.center_x < 0:
                self.remove_from_sprite_lists()
                return
        else:
            if self.center_x > gc.SCREEN_WIDTH:
                self.remove_from_sprite_lists()
                return

        return super().on_update()