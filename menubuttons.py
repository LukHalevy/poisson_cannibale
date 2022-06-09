import arcade
import game_constants as gc
class Resume:
    def __init__(self):
        self.button_scale = 1
        self.button = False
        self.sprite = arcade.Sprite("assets/resume1.png")
    def update(self):
        if self.button == True:
            self.sprite = arcade.Sprite("assets/resume2.png")
        else:
            self.sprite = arcade.Sprite("assets/resume1.png")
        self.sprite.center_x = gc.SCREEN_WIDTH / 2
        self.sprite.center_y = gc.SCREEN_HEIGHT / 1.5
        self.sprite.draw()

class Quit:
    def __init__(self):
        self.button_scale = 1
        self.button = False
        self.sprite = arcade.Sprite("assets/Quit1.png")
    def update(self):
        if self.button == True:
            self.sprite = arcade.Sprite("assets/Quit2.png")
        else:
            self.sprite = arcade.Sprite("assets/Quit1.png")
        self.sprite.center_x = gc.SCREEN_WIDTH / 2
        self.sprite.center_y = gc.SCREEN_HEIGHT / 2.5
        self.sprite.draw()



class Newgame:
    def __init__(self):
        self.button_scale = 0.5
        self.button = False
        self.sprite = arcade.Sprite("assets/Newgame1.png.png")
    def update(self):
        if self.button == True:
            self.sprite = arcade.Sprite("assets/Newgame2.png.png")
        else:
            self.sprite = arcade.Sprite("assets/Newgame1.png.png")
        self.sprite.center_x = gc.SCREEN_WIDTH / 2
        self.sprite.center_y = gc.SCREEN_HEIGHT / 0.5
        self.sprite.draw()

class QuitGame:
    def __init__(self):
        self.button_scale = 0.5
        self.button = False
        self.sprite = arcade.Sprite("assets/QuitGame1.png")
    def update(self):
        if self.button == True:
            self.sprite = arcade.Sprite("assets/QuitGame2.png")
        else:
            self.sprite = arcade.Sprite("assets/QuitGame1.png")
        self.sprite.center_x = gc.SCREEN_WIDTH / 2
        self.sprite.center_y = gc.SCREEN_HEIGHT / 1
        self.sprite.draw()

class LeaderboardButton:
    def __init__(self):
        self.button_scale = 0.5
        self.button = False
        self.sprite = arcade.Sprite("assets/Leaderboard1.png")
    def update(self):
        if self.button == True:
            self.sprite = arcade.Sprite("assets/Leaderboard2.png")
        else:
            self.sprite = arcade.Sprite("assets/Leaderboard1.png")
        self.sprite.center_x = gc.SCREEN_WIDTH / 2
        self.sprite.center_y = gc.SCREEN_HEIGHT / 1.5
        self.sprite.draw()

class Options:
    def __init__(self):
        self.button_scale = 0.5
        self.button = False
        self.sprite = arcade.Sprite("assets/Options1.png")
    def update(self):
        if self.button == True:
            self.sprite = arcade.Sprite("assets/Options2.png")
        else:
            self.sprite = arcade.Sprite("assets/Options1.png")
        self.sprite.center_x = gc.SCREEN_WIDTH / 2
        self.sprite.center_y = gc.SCREEN_HEIGHT / 2
        self.sprite.draw()