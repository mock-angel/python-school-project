# ChessEssentials.py
import config
import pygame
from widgets.Button import create_button_theme

from constants import *

class ChessEssentials():
    def __init__(self):
        
        self.init_background_tiles()
    
        self.init_piece_theme()
        
    def init_background_tiles(self):
        
        """
        Tile Frames: 
            These frames are to be blit on the tiles.
            The following are the temporary frames serving different purposes.
            
        colorh_square_img - The selected unit contains this frame.      (Cyan filled.)
        colorf_square_img - The selected unit can move on tiles with this frame.
                                                                        (Cyan Bordered.)
        colorcf_square_img - The selected unit can capture tiles with this frame.
                                                                        (Red Bordered.)
        The respective themes are generated to be used by tiles when necessary.
        """
        
        img_load = pygame.image.load
        
        default_color_1 = img_load(path + "color1_square.png").convert()
        default_color_2 = img_load(path + "color2_square.png").convert()
        colorh_square_img = img_load(path + "colorh_square.png").convert_alpha()
        colorf_square_img = img_load(path +"colorf_square.png").convert_alpha()
        colorcf_square_img = img_load(path +"colorcf_square.png").convert_alpha()
        
        selected_color_1 = default_color_1.copy()
        selected_color_2 = default_color_2.copy()
        selected_color_1.blit(colorh_square_img, (0, 0))
        selected_color_2.blit(colorh_square_img, (0, 0))
        
        self.color_1_theme_idle = create_button_theme(default_color_1)
        self.color_2_theme_idle = create_button_theme(default_color_2)
        
        self.color_1_theme_selected = create_button_theme(selected_color_1)
        self.color_2_theme_selected = create_button_theme(selected_color_2)
        
        point_color_1 = default_color_1.copy()
        point_color_2 = default_color_2.copy()
        point_color_1.blit(colorf_square_img, (0, 0))
        point_color_2.blit(colorf_square_img, (0, 0))
        
        self.color_1_theme_point = create_button_theme(point_color_1)
        self.color_2_theme_point = create_button_theme(point_color_2)
        
        point_capture_color_1 = default_color_1.copy()
        point_capture_color_2 = default_color_2.copy()
        point_capture_color_1.blit(colorcf_square_img, (0, 0))
        point_capture_color_2.blit(colorcf_square_img, (0, 0))
        
        self.color_1_theme_point_capture = create_button_theme(point_capture_color_1)
        self.color_2_theme_point_capture = create_button_theme(point_capture_color_2)
        
    def init_piece_theme(self):
        
        dark_dict = dict()
        light_dict = dict()
        
        dict_ = {'dark': dark_dict, 'light': light_dict}
        
        img_load = pygame.image.load
        img_scale = pygame.transform.scale
        
        size_tuple = config.square_size, config.square_size
        
        dark_dict["p"] = img_load(config.res_path + "Chess_tile_pd.png").convert_alpha()
        dark_dict["R"] = img_load(config.res_path + "Chess_tile_rd.png").convert_alpha()
        dark_dict["N"] = img_load(config.res_path + "Chess_tile_nd.png").convert_alpha()
        dark_dict["B"] = img_load(config.res_path + "Chess_tile_bd.png").convert_alpha()
        dark_dict["K"] = img_load(config.res_path + "Chess_tile_kd.png").convert_alpha()
        dark_dict["Q"] = img_load(config.res_path + "Chess_tile_qd.png").convert_alpha()
        
        dark_dict["p"] = img_scale(dark_dict["p"], (size_tuple))
        dark_dict["R"] = img_scale(dark_dict["R"], (size_tuple))
        dark_dict["N"] = img_scale(dark_dict["N"], (size_tuple))
        dark_dict["B"] = img_scale(dark_dict["B"], (size_tuple))
        dark_dict["K"] = img_scale(dark_dict["K"], (size_tuple))
        dark_dict["Q"] = img_scale(dark_dict["Q"], (size_tuple))
        
        light_dict["p"] = img_load(config.res_path + "Chess_tile_pl.png").convert_alpha()
        light_dict["R"] = img_load(config.res_path + "Chess_tile_rl.png").convert_alpha()
        light_dict["N"] = img_load(config.res_path + "Chess_tile_nl.png").convert_alpha()
        light_dict["B"] = img_load(config.res_path + "Chess_tile_bl.png").convert_alpha()
        light_dict["K"] = img_load(config.res_path + "Chess_tile_kl.png").convert_alpha()
        light_dict["Q"] = img_load(config.res_path + "Chess_tile_ql.png").convert_alpha()
        
        light_dict["p"] = img_scale(light_dict["p"], (size_tuple))
        light_dict["R"] = img_scale(light_dict["R"], (size_tuple))
        light_dict["N"] = img_scale(light_dict["N"], (size_tuple))
        light_dict["B"] = img_scale(light_dict["B"], (size_tuple))
        light_dict["K"] = img_scale(light_dict["K"], (size_tuple))
        light_dict["Q"] = img_scale(light_dict["Q"], (size_tuple))
        
        self.themes = dict_
        self.transparant_piece = pygame.Surface((size_tuple)).convert_alpha()
        self.transparant_piece.fill((0, 0, 0, 0), None, pygame.BLEND_RGBA_MULT)
        
    def get_tile_theme(self, (r, c), state):
        
        if state == IDLE:
            theme = (self.color_1_theme_idle if (r + c)%2 == 0 else self.color_2_theme_idle)
            
        elif state == SELECTED:
            theme = (self.color_1_theme_selected if (r + c)%2 == 0 else self.color_2_theme_selected)
            
        elif state == POINT_FREE:
            theme = (self.color_1_theme_point if (r + c)%2 == 0 else self.color_2_theme_point)
        
        elif state == POINT_CAPTURE:
            theme = (self.color_1_theme_point_capture if (r + c)%2 == 0 else self.color_2_theme_point_capture)
        
        return theme
        
    def get_piece(self, piece_name):
        if piece_name == "e": return self.transparant_piece
        
        color = "light" if piece_name[0] == "l" else "dark"
        return self.themes[color][piece_name[1]]
