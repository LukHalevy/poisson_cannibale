"""
Simple jeu fait avec arcade.
Le jeu consiste a ce que notre poisson mange des poissons plus petits que lui pour grossir.
L'utilisateur doit aussi éviter les poissons plus gros afin de ne pas perdre de vie.
"""
import random

import arcade

from game_time import GameElapsedTime
from player import Player, Direction
from enemy_fish import EnemyFish
import game_constants as gc
from game_constants import GameState

"""
1) map border
2) find when player touch other fish
3) get both fish sizes
4) if player bigger: use algorithm to increase size and despawn fish, if enemy bigger: remove life and return player to middle with i-frames
"""


class MyGame(arcade.Window):
    """
    La classe principale de l'application

    NOTE: Vous pouvez effacer les méthodes que vous n'avez pas besoin.
    Si vous en avez besoin, remplacer le mot clé "pass" par votre propre code.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLUE_YONDER)

        self.back_ground = None

        # Player related attributes.
        self.player = None
        self.player_move_up = False
        self.player_move_down = False
        self.player_move_left = False
        self.player_move_right = True
        self.GAMESTATE = GameState.GAME_MENU
        self.enemy_list = None
        self.score = 0
        self.final_score = 0
        self.fishes_hit = 0
        self.game_camera = None
        self.gui_camera = None
        self.shortcut = 0
        self.game_timer = GameElapsedTime()

    def setup(self):
        """
        Configurer les variables de votre jeu ici. Il faut appeler la méthode une nouvelle
        fois si vous recommencer une nouvelle partie.
        """
        self.player = Player("assets/2dfish/spritesheets/__cartoon_fish_06_yellow_idle.png")
        self.player.current_animation.center_x = gc.SCREEN_WIDTH / 2
        self.player.current_animation.center_y = gc.SCREEN_HEIGHT / 2 - 50

        self.back_ground = arcade.Sprite("assets/Background.png")
        self.back_ground.center_x = gc.SCREEN_WIDTH / 2
        self.back_ground.center_y = gc.SCREEN_HEIGHT / 2

        self.enemy_list = arcade.SpriteList()

        self.game_camera = arcade.Camera(gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT)

        # Each two seconds, a new enemy fish will spawn.
        arcade.schedule(self.spawn_enemy_fish, 2)

    def spawn_enemy_fish(self, delta_time):
        """
        Callback method to spawn a new fish.
        :param delta_time: The elapsed time.
        :return: None
        """
        direction = Direction.LEFT if random.randint(0, 1) == 1 else Direction.RIGHT
        x = -50 if direction == Direction.RIGHT else gc.SCREEN_WIDTH + 50
        y = random.randrange(50, gc.SCREEN_HEIGHT - 150)
        enemy = EnemyFish(direction, (x, y))

        self.enemy_list.append(enemy)

    def on_draw(self):
        """
        C'est la méthode que Arcade invoque à chaque "frame" pour afficher les éléments
        de votre jeu à l'écran.
        """
        arcade.start_render()

        # Game camera rendering
        self.game_camera.use()
        self.back_ground.draw()
        if self.player.Iseconds > 0:
            arcade.draw_ellipse_filled(self.player.current_animation.center_x, self.player.current_animation.center_y,
                                       self.player.player_scale + self.player.player_scale,
                                       self.player.player_scale + self.player.player_scale / 2,
                                       arcade.color.WHITE_SMOKE)
        self.player.draw()

        self.enemy_list.draw()

        # Gui camera rendering
        self.gui_camera.use()
        arcade.draw_rectangle_filled(gc.SCREEN_WIDTH // 2, gc.SCREEN_HEIGHT - 25, gc.SCREEN_WIDTH, 50,
                                     arcade.color.BLEU_DE_FRANCE)

        arcade.draw_text(f"Lives : {self.player.lives}", 5, gc.SCREEN_HEIGHT - 35, arcade.color.WHITE_SMOKE, 20,
                         width=120, align="center")
        arcade.draw_text(f"Size : {round(self.player.player_scale * 100)}", 200, gc.SCREEN_HEIGHT - 35,
                         arcade.color.WHITE_SMOKE, 20, width=120, align="center")
        arcade.draw_text(f"Time played : {self.game_timer.get_time_string()}",
                         gc.SCREEN_WIDTH - 350,
                         gc.SCREEN_HEIGHT - 35,
                         arcade.color.WHITE_SMOKE,
                         20, width=400, align="center")

    def on_update(self, delta_time):
        """
        Toute la logique pour déplacer les objets de votre jeu et de
        simuler sa logique vont ici. Normalement, c'est ici que
        vous allez invoquer la méthode "update()" sur vos listes de sprites.
        Paramètre:
            - delta_time : le nombre de milliseconde depuis le dernier update.
        """
        # Calculate elapsed time
        self.score = self.game_timer / 2 + self.fishes_hit
        self.game_timer.accumulate()
        self.player.Iseconds -= 1 / 60
        self.player.update(delta_time)
        self.enemy_list.update()
        self.fish_hit_list = arcade.check_for_collision_with_list(self.player.current_animation,
                                                                  self.enemy_list)
        if len(self.fish_hit_list) > 0 and self.player.Iseconds <= 0:
            for EnemyFish in self.fish_hit_list:

                if EnemyFish.scale <= self.player.player_scale:
                    if EnemyFish.scale / self.player.player_scale * 0.05 < 0.01:
                        pass
                    else:
                        self.fishes_hit += 1
                        self.player.player_scale += EnemyFish.scale / self.player.player_scale * 0.05
                        EnemyFish.remove_from_sprite_lists()
                else:
                    self.player.respawn()
        if self.player.lives <= 2:
            self.GAMESTATE = GameState.GAME_OVER
        if self.GAMESTATE == GameState.GAME_OVER:
            self.final_score = self.score
            self.game_timer = 0
            self.player.current_animation.center_y = 1000
            for EnemyFish in self.enemy_list:
                EnemyFish.remove_from_sprite_lists()

    def update_player_speed(self):
        """
        Will update player position according to various movement flags.
        :return: None
        """
        self.player.current_animation.change_x = 0
        self.player.current_animation.change_y = 0

        if self.player_move_left and not self.player_move_right:
            self.player.change_direction(Direction.LEFT)
            self.player.current_animation.change_x = -Player.MOVEMENT_SPEED
        elif self.player_move_right and not self.player_move_left:
            self.player.change_direction(Direction.RIGHT)
            self.player.current_animation.change_x = Player.MOVEMENT_SPEED

        if self.player_move_up and not self.player_move_down:
            self.player.current_animation.change_y = Player.MOVEMENT_SPEED
        elif self.player_move_down and not self.player_move_up:
            self.player.current_animation.change_y = -Player.MOVEMENT_SPEED

    def on_key_press(self, key, key_modifiers):
        """
        Cette méthode est invoquée à chaque fois que l'usager tape une touche
        sur le clavier.
        Paramètres:
            - key: la touche enfoncée
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?

        Pour connaître la liste des touches possibles:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.A:
            self.player_move_left = True
            self.update_player_speed()
        elif key == arcade.key.D:
            self.player_move_right = True
            self.update_player_speed()
        elif key == arcade.key.W:
            self.player_move_up = True
            self.update_player_speed()
        elif key == arcade.key.S:
            self.player_move_down = True
            self.update_player_speed()
        """
        dev shortcut
        """
        if key == arcade.key.C:
            self.shortcut = 1
        if key == arcade.key.L and self.shortcut == 1:
            self.shortcut = 2
        if key == arcade.key.NUM_1 and self.shortcut == 2:
            self.player.player_scale = 0.1
            self.shortcut = 0
        elif key == arcade.key.NUM_2 and self.shortcut == 2:
            self.player.player_scale = 0.2
            self.shortcut = 0
        elif key == arcade.key.NUM_3 and self.shortcut == 2:
            self.player.player_scale = 0.3
            self.shortcut = 0
        elif key == arcade.key.NUM_4 and self.shortcut == 2:
            self.player.player_scale = 0.4
            self.shortcut = 0
        elif key == arcade.key.NUM_5 and self.shortcut == 2:
            self.player.player_scale = 0.5
            self.shortcut = 0
        elif key == arcade.key.NUM_6 and self.shortcut == 2:
            self.player.player_scale = 0.6
            self.shortcut = 0
        elif key == arcade.key.NUM_7 and self.shortcut == 2:
            self.player.player_scale = 0.7
            self.shortcut = 0
        elif key == arcade.key.NUM_8 and self.shortcut == 2:
            self.player.player_scale = 0.8
            self.shortcut = 0
        elif key == arcade.key.NUM_9 and self.shortcut == 2:
            self.player.player_scale = 0.9
            self.shortcut = 0

    def on_key_release(self, key, key_modifiers):
        """
        Méthode invoquée à chaque fois que l'usager enlève son doigt d'une touche.
        Paramètres:
            - key: la touche relâchée
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
        """
        if key == arcade.key.A:
            self.player_move_left = False
            self.update_player_speed()
        elif key == arcade.key.D:
            self.player_move_right = False
            self.update_player_speed()
        elif key == arcade.key.W:
            self.player_move_up = False
            self.update_player_speed()
        elif key == arcade.key.S:
            self.player_move_down = False
            self.update_player_speed()


def main():
    """ Main method """
    game = MyGame(gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT, gc.SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
