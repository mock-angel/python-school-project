# Colors.py
def hexa_to_rgb(hexa):
    return tuple(int(hexa.lstrip('#')[i:i+2], 16) for i in (0, 2 ,4))
    
def adjust_color(*rgb):
    rgb = list(rgb)
    if rgb[0] > 255: rgb[0] = 255
    if rgb[1] > 255: rgb[1] = 255
    if rgb[2] > 255: rgb[2] = 255

    if rgb[0] < 0: rgb[0] = 0
    if rgb[1] < 0: rgb[1] = 0
    if rgb[2] < 0: rgb[2] = 0
    
    return tuple(rgb)
