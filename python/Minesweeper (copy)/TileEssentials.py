# TileEssentials.py
"""Not revised."""

import pygame
from widgets.Button import create_button_theme
src_default = "data/themes/bgcolors/Tile/"

get_surface = pygame.image.load
scale = pygame.transform.scale

tile_size = (64, 64)
tile_number_size = (21*2, 21*2)

def scale_template_collection(collection, size):
    C = dict()
    
    for key in collection:
        C[key] = scale_template(collection[key], size)
    
    return C

def scale_template(template, size):
    T = dict()
    
    for key in template:

        T[key] = scale_theme(template[key], size)
    
    return T

def scale_theme(theme, size):
    T = dict()
    
    for key in theme:

        T[key] = scale(theme[key], size)
    
    return T

class MineImages():
    def __init__(self):
        
        self.generated = False
        self.tile_info = dict()#info for colors and default tiles
        self.default_colors = dict()

        
    def load_surfaces(self, t_tile_size = (32, 32), t_number_size = (32, 32)):
        if t_tile_size:
            self.tile_size = t_tile_size
            self.number_size = t_number_size
        else:
            self.tile_size = t_tile_size
            self.number_size = t_number_size
        #load defaults.
        frame = get_surface(src_default + "frame.png").convert_alpha()
        
        self.tile_info = {
            
            "TILEFRAME" : scale(get_surface(src_default + "frame.png").convert_alpha(), tile_size),
            "held_tile_alpha" : scale(get_surface(src_default + "held_alpha.png").convert_alpha(), tile_size),
            "covered_lost" : (136, 138, 133),
            "uncovered_lost" : ( 222, 222, 220),
            "default_covered" : ( 186, 189, 182),
            "default_uncovered" : ( 222, 222, 220),
            "default_hover" : ( 211, 215, 207),
        }
        
        self.held_alpha = scale(self.tile_info["held_tile_alpha"], tile_size)
        
        #load Flags.
        #########################################################
        self.flag_raw = dict()
        
        self.flag_raw["incorrect"] = get_surface(src_default + "incorrect.png")
        
        self.flag_raw["flag"] = get_surface(src_default + "flag.png")
        
        self.flag_raw["maybe"] = get_surface(src_default + "maybe.png")
        
        #Load Mines raw .
        #########################################################
        self.mine_raw = dict()
        self.mine_raw["mine"] = get_surface(src_default + "mine.png")
        
        self.mine_raw["exploded"] = get_surface(src_default + "exploded.png")
        
        #load colored numbers raw.
        #########################################################
        self.colored_numbers_raw = dict()
        self.colored_numbers_raw["1"] = get_surface(src_default + "1mines.png").convert_alpha()
        
        self.colored_numbers_raw["2"] = get_surface(src_default + "2mines.png").convert_alpha()
        
        self.colored_numbers_raw["3"] = get_surface(src_default + "3mines.png").convert_alpha()
        
        self.colored_numbers_raw["4"] = get_surface(src_default + "4mines.png").convert_alpha()
        
        self.colored_numbers_raw["5"] = get_surface(src_default + "5mines.png").convert_alpha()
        
        self.colored_numbers_raw["6"] = get_surface(src_default + "6mines.png").convert_alpha()
        
        self.colored_numbers_raw["7"] = get_surface(src_default + "7mines.png").convert_alpha()
        
        self.colored_numbers_raw["8"] = get_surface(src_default + "8mines.png").convert_alpha()
        
        self.colored_numbers_raw["13"] = get_surface(src_default + "mine.png").convert_alpha()
        
        self.colored_numbers_raw["12"] = get_surface(src_default + "exploded.png").convert_alpha()
        
        # generate flag template(set of themes.)
        #########################################################
        self.flag_template_collection_unscaled = dict()
        
        for key in self.flag_raw:
            self.flag_template_collection_unscaled[key] = self.gen_template(scale(self.flag_raw[key], tile_number_size).convert_alpha())
        
        self.mine_template_unscaled = dict()
        
        for key in self.mine_raw:
            self.mine_template_unscaled[key] = self.gen_template(scale(self.mine_raw[key], tile_number_size).convert_alpha())
        
        #########################################################
        self.mine_template_set_unscaled = dict()
        for key in self.colored_numbers_raw:
            self.mine_template_set_unscaled[key] = self.gen_template(scale(self.colored_numbers_raw[key], tile_number_size))
        
        #self.flag_template["cursor_exploded"] = self.gen_theme(self.flag_raw["exploded"])
        
        #load colored numbers.
        #########################################################
        self.colored_numbers_template_set_unscaled = dict()
        
        surf = pygame.Surface(tile_size).convert_alpha()

        surf.fill((0, 0,0, 0), None, pygame.BLEND_RGBA_MULT)
        
        self.colored_numbers_template_set_unscaled["0"] = self.generate_number_template_set(surf)
        
        for key in self.colored_numbers_raw:
            self.colored_numbers_template_set_unscaled[key] = self.generate_number_template_set(scale(self.colored_numbers_raw[key], tile_number_size))
            
            
        t_surf = scale(self.colored_numbers_raw["13"], tile_number_size)
        r = t_surf.get_rect()
        if r.width == tile_size[0] and r.height == tile_size[1]:
            print "NOt centered"
        else:
            r.center = tile_size[0]/2  , tile_size[1]/2 
        
        pos =  r.x, r.y
        
        surf = pygame.Surface(tile_size)
        frame_surf = self.tile_info["TILEFRAME"]
        u_default, u_held = surf.copy(), surf.copy()
        u_default.fill(self.tile_info["covered_lost"])
        u_default.blit(t_surf, pos)
        u_default.blit(frame_surf, (0, 0))
        u_held.fill(self.tile_info["covered_lost"])
        u_held.blit(t_surf, pos)
        u_held.blit(frame_surf, (0, 0))
        u_held.blit(self.held_alpha, (0, 0))
        
        self.colored_numbers_template_set_unscaled["13"]["lost"]["uncovered"] = \
                                      create_button_theme(u_default, u_default, u_held)
        # Scale everything.
        #########################################################
        self.mine_template_set = dict()
        
        self.flag_template_collection = dict()
        
        self.flag_template_collection = scale_template_collection(\
                                self.flag_template_collection_unscaled, self.tile_size)
        
        self.colored_numbers_template_set = dict()
        
        for key in self.colored_numbers_template_set_unscaled:
            self.colored_numbers_template_set[key] = scale_template_collection(\
                        self.colored_numbers_template_set_unscaled[key],self.tile_size)
        
    def generate_number_template_set(self, t_surf):
        
        t_surf
        r = t_surf.get_rect()
        if r.width == tile_size[0] and r.height == tile_size[1]:
            print "Not centered"
        else:
            r.center = tile_size[0]/2  , tile_size[1]/2 
        
        pos =  r.x, r.y
        
        surf = pygame.Surface(tile_size)
        frame_surf = self.tile_info["TILEFRAME"]
#        held_tile_alpha = self.tile_info["held_tile_alpha"]
        
        if self.generated == False:
            u_default, u_hover, u_held = surf.copy(), surf.copy(), surf.copy()
            u_default.fill(self.tile_info["default_covered"])
            u_default.blit(frame_surf, (0, 0)) 
            u_hover.fill(self.tile_info["default_hover"])
            u_hover.blit(frame_surf, (0, 0)) 
            u_held.fill(self.tile_info["default_hover"])
            u_held.blit(frame_surf, (0, 0))
            u_held.blit(self.held_alpha, (0, 0))
            
            self.norm_covered_theme = create_button_theme(u_default, u_hover, u_held)
            
            w_default, w_held = surf.copy(), surf.copy()
            w_default.fill(self.tile_info["covered_lost"])
            w_default.blit(frame_surf, (0, 0))
            w_held.fill(self.tile_info["covered_lost"])
            w_held.blit(t_surf, pos)
            w_held.blit(frame_surf, (0, 0))
            w_held.blit(self.held_alpha, (0, 0))
            self.lost_covered_theme = create_button_theme(w_default, w_default, w_held)
            self.generated = True        
        
        else:
            pass
        
        b_default, b_held = surf.copy(), surf.copy()
        b_default.fill(self.tile_info["default_uncovered"])
        b_default.blit(t_surf, pos)
        b_default.blit(frame_surf, (0, 0))
        b_held.fill(self.tile_info["default_uncovered"])
        b_held.blit(t_surf, pos)
        b_held.blit(frame_surf, (0, 0))
        b_held.blit(self.held_alpha, (0, 0))
        
        
        u_default, u_held = surf.copy(), surf.copy()
        u_default.fill(self.tile_info["uncovered_lost"])
        u_default.blit(t_surf, pos)
        u_default.blit(frame_surf, (0, 0))
        u_held.fill(self.tile_info["uncovered_lost"])
        u_held.blit(t_surf, pos)
        u_held.blit(frame_surf, (0, 0))
        u_held.blit(self.held_alpha, (0, 0))
        
        covered = self.norm_covered_theme
        uncovered = create_button_theme(b_default, b_default, b_held)
        covered_lost = self.lost_covered_theme
        uncovered_lost = create_button_theme(u_default, u_default, u_held)
        return {
            "norm" : {
                "covered" : covered,
                "uncovered" : uncovered
            },

            "lost" : {
                "covered" : covered_lost,
                "uncovered" : uncovered_lost
            }
        }
        
    def gen_template(self,t_surf):
        
        r = t_surf.get_rect()
        r.center = tile_size[0]/2, tile_size[1]/2
        
        pos =  r.x, r.y
        
        surf = pygame.Surface(tile_size)
        frame_surf = self.tile_info["TILEFRAME"]
        
        u_default, u_hover, u_held = surf.copy(), surf.copy(), surf.copy()
        u_default.fill(self.tile_info["default_covered"])
        u_default.blit(t_surf, pos)
        u_default.blit(frame_surf, (0, 0))
        u_hover.fill(self.tile_info["default_hover"])
        u_hover.blit(t_surf, pos)
        u_hover.blit(frame_surf, (0, 0)) 
        u_held.fill(self.tile_info["default_hover"])
        u_held.blit(t_surf, pos)
        u_held.blit(frame_surf, (0, 0))
        u_held.blit(self.held_alpha, (0, 0))
        
        norm = create_button_theme(u_default, u_hover, u_held)
        
        v_default, v_hover, v_held = surf.copy(), surf.copy(), surf.copy()
        v_default.fill(self.tile_info["covered_lost"])
        v_default.blit(t_surf, pos)
        v_default.blit(frame_surf, (0, 0))
        v_hover.fill(self.tile_info["covered_lost"])
        v_hover.blit(t_surf, pos)
        v_hover.blit(frame_surf, (0, 0)) 
        v_held.fill(self.tile_info["covered_lost"])
        v_held.blit(t_surf, pos)
        v_held.blit(frame_surf, (0, 0))
        v_held.blit(self.held_alpha, (0, 0))
        
        norm = create_button_theme(u_default, u_hover, u_held)
        lost = create_button_theme(v_default, v_hover, v_held)
        
        return {
            "norm" : norm,
            "lost" : lost,
        }
    
    def get_number_template(self, number):
        return self.colored_numbers_template_set[str(number)]
    
    def get_flag_template(self):
        return self.flag_template_collection
    
    def reset(self):
        self.generated = False
