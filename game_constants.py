from enum import Enum
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 764
SCREEN_TITLE = "It's a fish eat fish world!"
GUI_HEIGHT = SCREEN_HEIGHT - 50

class GameState(Enum):
    GAME_MENU = 0
    GAME_RUNNING = 1
    GAME_OVER = 2
    GAME_WIN = 3
    GAME_PAUSE = 4