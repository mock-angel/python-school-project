# config.py
res_path = "images/"
board_start_x = 50
board_start_y = 50
square_size = 50
color1 = (0, 0, 0)
color2 = (144, 144, 0)

# constants.py
path = "images/"

IDLE = 10 
SELECTED = 11
POINT_FREE = 12
POINT_CAPTURE = 13
POINT = 14

SELECTION_SCREEN = 1
GAME_SCREEN = 0

SCREEN_TITLE = "PyChess"
SCREEN_ICON = "icon.png"
SCREEN_SIZE = (850,500)
SCREEN_COLOR = (206, 206, 206)
UPDATE_FPS = 0
GRAPHICS_FPS = 60
version_name = "v1.0 (None)"
from chess import chess as main_app
