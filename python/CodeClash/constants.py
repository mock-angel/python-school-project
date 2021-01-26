# constants.py

import colorsys

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
BACKGROUND = (0, 45, 45)
LINES_COLOR = (0, 109, 109)

RED_GRAD = 1
GREEN_GRAD = 2
TEAL_GRAD = 3

tile_size = tile_scaling = 32
block_size = 60

PI = 3.141592653
rat = .5
# Helper function to convert hsv to rgb.
def hsv_2_rgb(h,s,v):
    return   tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h/360.,s/100.,v/100.))

# Helper function to flip image horizontally.
def flip_image_x(image):
    pass

# Gradiant color values for applying abnds of colors for both teams.
GREEN_GRAD = [
    hsv_2_rgb(100,78,55),#!
    hsv_2_rgb(100,90,47),#!
    hsv_2_rgb(100,95,45),#!
    hsv_2_rgb(100,100,43),#!
    hsv_2_rgb(100,100,43)# |
]

TEAL_GRAD = [
    hsv_2_rgb(183,78,55),
    hsv_2_rgb(183,90,47),
    hsv_2_rgb(183,95,45),
    hsv_2_rgb(183,100,43),
    hsv_2_rgb(182,100,39)
]

RED_GRAD = [
    hsv_2_rgb(335,78,55),
    hsv_2_rgb(335,90,47),
    hsv_2_rgb(335,95,45),
    hsv_2_rgb(335,100,43),
    hsv_2_rgb(335,100,39)
]

SCREEN_SIZE = (1920/2, 1080/2)
SCREEN_ICON = 'icon.png'
