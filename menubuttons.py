import arcade

class Resume:
    def __init__(self):
        self.button_scale = 1
        self.button = False
        self.sprite = "assets/resume1.png"
    def update(self):
        if button == True:
            self.sprite = "assets/resume1.png"
        else:
            self.sprite = "assets/resume2.png"
        self.sprite.draw()