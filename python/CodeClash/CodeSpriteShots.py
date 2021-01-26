# CodeSpriteShots.py
import pygame
from pygame.locals import *

import time

import colorsys

RED_GRAD = 1
GREEN_GRAD = 2
TEAL_GRAD = 3

# Helper function to convert hsv to rgb.
def hsv_2_rgb(h,s,v):
    return   tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h/360.,s/100.,v/100.))

# Gradiants - Refer Graphic Layout coment below to search for markings.
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
tile_size = 32
rat = .5
class Shot(pygame.sprite.Sprite):
    #####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, color_no, rect_arg):
        '''Constructor.'''
        
        super(Shot, self).__init__()
        
        self.rect_arg = rect_arg
        self.color_no = color_no
        self.COLOR = COLOR
        
        xxx, yyy = pygame.display.get_surface().get_size()
        self.screen_size = {'x':xxx, 'y':yyy}
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = ["Shot", "Mine"] #transparant
        self.immune_list = []
        
        self.type = "Shot"
        self.health = 1
        self.inflict_damage = 1
        self.base_dp = 1
        
        self.collision_instant_self_kill = True
        self.collision_instant_destroy = False
        
        if self.COLOR == RED_GRAD: 
            F='r'
        elif self.COLOR == GREEN_GRAD:
            F='g'
        elif self.COLOR == TEAL_GRAD:
            F='t'
            
        self.loaded_image = pygame.image.load('data/colors/{}/Shot.png'.format(F) ).convert_alpha()
        
        self.image = self.loaded_image.copy()
        rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(rect.width*rat), int(rect.height*rat)))
        self.require_update = True
        
        self.define_rect()
        self.create_inner_rect()
        
        self.current_t = time.time()
        self.prev_t = 0
        #self.prev_t = time.time() #1
        self.diff_t = (self.current_t - self.prev_t) if self.prev_t else 0 #1
        self.time_per_tick = 1 / 6.
        self.block_size = (65 - 1)*rat
        self.add_t = 0
        
        self.queue_group = pygame.sprite.Group()
        self.next_shot_time = 0
        
        self.state = "operational"
        
    def define_rect(self):
        """Create rect object for image blitting."""
        
        self.rect = self.image.get_rect()
        
        self.rect.y = (self.rect_arg.y / tile_size) * tile_size 
        self.rect.x = (self.rect_arg.x - self.rect_arg.width - 5) if self.color_no else (self.rect_arg.x + self.rect_arg.width ) 
        self.relative_distance = self.screen_size['x'] - self.rect_arg.x  if self.color_no else self.rect_arg.x + self.rect_arg.width
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        
        self.dirty_rect = self.rect.copy()
        
        self.dirty_rect.x += (9 if not self.color_no else 8)*rat
        self.dirty_rect.y += 9*rat
        self.dirty_rect.width = 48*rat
        self.dirty_rect.height += 48*rat
        
        self.collision_rect = self.dirty_rect.copy()
        
        self.collision_rect.x += (26 if not self.color_no else 26)*rat
        self.collision_rect.y += 24*rat
        self.collision_rect.width = 14*rat
        self.collision_rect.height = 14*rat
    #####################################################################################
    # --- User scripts used by update to run these methods depending on sprite state.
    
    def __script_event_deploy(self):
        """Executes during sprite deployment phase."""
        
        pass
    
    def __script_event_operational(self):
        """Executes on normal operation after sprite is fully deployed."""
#        def add_shot_to_queue(self):
#        
#            shot = Shot(self.COLOR, self.color_no, self.dirty_rect.copy())
#            shot.create_inner_rect()
#            self.queue_group.add(shot)
        self.relative_distance += self.block_size * ((self.diff_t * 1.0) / self.time_per_tick) 
        self.rect.x = (self.screen_size["x"] - self.relative_distance) if self.color_no else self.relative_distance
        
        self.dirty_rect.x = self.rect.x + (9 if not self.color_no else 8)*rat
        self.collision_rect.x = self.rect.x + (27 if not self.color_no else 26)*rat
    def __script_event_self_decimate(self):
        """Executes when its being decimated."""
        pass
    
    def __script_event_desecrate(self):
        """Executes when its fully destroyed."""
    #####################################################################################
    # --- Engine can use the following methods for stated operations.
    
    def update(self):
        """Updates the state of the sprite."""
        
        self.current_t = time.time()
        self.diff_t = (self.current_t - self.prev_t) if self.prev_t else 0 #1
        self.add_t += self.diff_t
        
        if self.state == "operational": 
            self.__script_event_operational()
            
        elif self.state == "deploying": 
            self.__script_event_deploy()
            
        elif self.state == "self_decimate": 
            self.__script_event_self_decimate()
            
        elif self.state == "Paused" and (not self.sprite_collided_with.alive()): 
            self.state = "operational"
        
        elif self.state == "Withdraw":
            # TODO: Please perform a withdraw during impact.
            pass
        
        self.prev_t = self.current_t
    
    def pause(self):
        """Change sprite state to pause."""
        
        self.state = "pause"
        
    def get_created_sprites(self):
        """Get all sprites this sprite has queued."""
        
        return self.queue_group
            
    def sprite_under_collision(self, sprite):
        """States which sprite collided with this sprite."""
        
        self.sprite_collided_with = sprite
        
    def is_collided_with(self, sprite):
        """Check whether some other sprite collided with this sprite."""
        
        return self.collision_rect.colliderect(sprite.collision_rect)
