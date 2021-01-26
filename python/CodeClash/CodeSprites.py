# CodeSprites.py

import colorsys
import time
import random

import pygame
from pygame.locals import *

from CodeSpriteShots import Shot

RED_GRAD = 1
GREEN_GRAD = 2
TEAL_GRAD = 3

# Helper function to convert hsv to rgb.
def hsv_2_rgb(h,s,v):
    return   tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h/360.,s/100.,v/100.))
tile_size = 32
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

#xxx, yyy = pygame.display.get_surface().get_size()
#screen_size = {'x':xxx, 'y':yyy}
rat = .5

# NOTE: 
# - invisibility_list- if it colides with any of this type, its termed invisible collision.
# - immune_list - no sprite defined in this list will ever harm this sprite.
#
# - type - Its the main role that defines its uniqueness to other sprites.
# - health - 0 means its destroyed.
# - inflict_damage - 0 means it deals no damage to other sprites.
# - 
# - image - Default image is loaded here.
# 
# * define_rect - Defines rect object.
# * create_inner_rect - Creates dirty_rect and opaque_rect objects.
# - rect - its used by the engine to move the sprite and display the sprite.
# - dirty_rect - its used for refreshing part of screen as param # TODO: change to dirty_rect.
# - collision_rect - defines what areas triggers collision.

class Rocket(pygame.sprite.Sprite):
    #####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, color_no):
        '''Constructor.'''
        
        super(Rocket, self).__init__()
        
        self.color_no = color_no
        self.COLOR = COLOR
        xxx, yyy = pygame.display.get_surface().get_size()
        self.screen_size = {'x':xxx, 'y':yyy}
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = [] #transparant
        self.immune_list = ["Shot"]
        
        self.type = "Rocket"
        self.health = 1000
        self.inflict_damage = 1000
        self.base_dp = 4
        
        self.collision_instant_self_kill = True
        self.collision_instant_destroy = True
        
        if self.COLOR == RED_GRAD: 
            F='r'
        elif self.COLOR == GREEN_GRAD:
            F='g'
        elif self.COLOR == TEAL_GRAD:
            F='t'
            
        self.loaded_image = pygame.image.load('data/colors/{}/Rocket.png'.format(F) ).convert_alpha()
        
        self.image = pygame.transform.flip(self.loaded_image, 1, 0) if self.color_no else self.loaded_image.copy()
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
        
        self.rect.x = self.screen_size['x'] - (tile_size * 9) if self.color_no else tile_size*(7)
        self.relative_distance = (tile_size * 9)  if self.color_no else tile_size*(7)
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        
        self.dirty_rect = self.rect.copy()
        self.dirty_rect.x += (61 if not self.color_no else 67)*rat
        self.dirty_rect.y = self.rect.y + 19*rat
        self.dirty_rect.width = 67*rat
        self.dirty_rect.height = 24*rat
        
        self.collision_rect = self.dirty_rect.copy()
        
    #####################################################################################
    # --- User scripts used by update to run these methods depending on sprite state.
    
    def __script_event_deploy(self):
        """Executes during sprite deployment phase."""
        
        pass
    
    def __script_event_operational(self):
        """Executes on normal operation after sprite is fully deployed."""
#        def add_shot_to_queue():
#        
#            shot = Shot(self.COLOR, self.color_no, self.dirty_rect.copy())
#            shot.create_inner_rect()
#            self.queue_group.add(shot)
        self.relative_distance += self.block_size * ((self.diff_t * 1.0) / self.time_per_tick) 
        self.rect.x = (self.screen_size["x"] - self.relative_distance) if self.color_no else self.relative_distance
        
        # If both are equal.
        self.collision_rect.x = self.dirty_rect.x = self.rect.x + (61 if not self.color_no else 67)*rat
    
    def __script_event_paused(self):
        """Executes when its paused."""
        
        pass
    
    def __script_event_self_decimate(self):
        """Executes when its being decimated."""
        pass
    
    def __script_event_desecrate(self):
        """Executes when its fully destroyed."""
        
        pass
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

        elif self.state == "pause": 
            self.__script_event_paused()

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
    
class Wall(pygame.sprite.Sprite):
    #####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, color_no):
        '''Constructor.'''
        
        super(Wall, self).__init__()
        xxx, yyy = pygame.display.get_surface().get_size()
        self.screen_size = {'x':xxx, 'y':yyy}
        self.color_no = color_no
        self.COLOR = COLOR
        
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = [] #transparant
        self.immune_list = []
        
        self.type = "Wall"
        self.health = 7
        self.inflict_damage = 0
        
        self.collision_instant_self_kill = False
        self.collision_instant_destroy = False
        
        if self.COLOR == RED_GRAD: 
            F='r'
        elif self.COLOR == GREEN_GRAD:
            F='g'
        elif self.COLOR == TEAL_GRAD:
            F='t'
            
        self.loaded_image = pygame.image.load('data/colors/{}/Wall.png'.format(F) ).convert_alpha()
        
        self.image = pygame.transform.flip(self.loaded_image, 1, 0) if self.color_no else self.loaded_image.copy()
        
        rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(rect.width*rat), int(rect.height*rat)))
        self.require_update = True
        
        self.define_rect()
        self.create_inner_rect()
        
        self.current_t = time.time()
        self.prev_t = 0
        #self.prev_t = time.time() #1
        self.diff_t = (self.current_t - self.prev_t) if self.prev_t else 0 #1
        self.time_per_tick = 1
        self.block_size = (65 - 1)*rat
        self.add_t = 0
        
        self.queue_group = pygame.sprite.Group()
        self.next_shot_time = 0
        
        self.state = "operational"
        
    def define_rect(self):
        """Create rect object for image blitting."""
        
        self.rect = self.image.get_rect()
        
        self.rect.x = self.screen_size['x'] - (tile_size * 7) if self.color_no else tile_size*(6)
        self.relative_distance = ((tile_size * 7)  if self.color_no else tile_size*(6))
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        
        self.dirty_rect = self.rect.copy()
        self.dirty_rect.x += (11 if not self.color_no else 23)*rat
        self.dirty_rect.y = self.rect.y + 61*rat
        self.dirty_rect.width = 31*rat
        self.dirty_rect.height = (68)*rat
        
        self.collision_rect = self.dirty_rect.copy()
        
    #####################################################################################
    # --- User scripts used by update to run these methods depending on sprite state.
    
    def __script_event_deploy(self):
        """Executes during sprite deployment phase."""
        
        pass
    
    def __script_event_operational(self):
        """Executes on normal operation after sprite is fully deployed."""
        
        pass
        
    def __script_event_pause(self):
        """Executes when its paused."""
        
        pass
    
    def __script_event_self_decimate(self):
        """Executes when its being decimated."""
        pass
    
    def __script_event_desecrate(self):
        """Executes when its fully destroyed."""
        
        pass
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
            
        elif self.state == "pause": 
            self.__script_event_pause()
        
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
    
class Tank(pygame.sprite.Sprite):
    #####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, color_no):
        '''Constructor.'''
        
        super(Tank, self).__init__()
        
        self.color_no = color_no
        self.COLOR = COLOR
        xxx, yyy = pygame.display.get_surface().get_size()
        self.screen_size = {'x':xxx, 'y':yyy}
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = [] #transparant
        self.immune_list = []
        
        self.type = "Tank"
        self.health = 3
        self.inflict_damage = 0
        self.base_dp = 3
        
        self.collision_instant_self_kill = False
        self.collision_instant_destroy = False
        
        if self.COLOR == RED_GRAD: 
            F='r'
        elif self.COLOR == GREEN_GRAD:
            F='g'
        elif self.COLOR == TEAL_GRAD:
            F='t'
            
        self.loaded_image = pygame.image.load('data/colors/{}/Tank.png'.format(F) ).convert_alpha()
        
        self.image = pygame.transform.flip(self.loaded_image, 1, 0) if self.color_no else self.loaded_image.copy()
        rect = self.image.get_rect()
        
        self.image = pygame.transform.scale(self.image, (int(rect.width*rat), int(rect.height*rat)))
        self.require_update = True
        
        self.define_rect()
        self.create_inner_rect()
        
        self.current_t = time.time()
        self.prev_t = 0
        #self.prev_t = time.time() #1
        self.diff_t = (self.current_t - self.prev_t) if self.prev_t else 0 #1
        self.time_per_tick = 1
        self.block_size =  (65 - 1)*rat
        self.add_t = 0
        
        self.queue_group = pygame.sprite.Group()
        self.next_shot_time = 0
        
        self.state = "operational"
        
    def define_rect(self):
        """Create rect object for image blitting."""
        
        self.rect = self.image.get_rect()
        
        self.rect.x = self.screen_size['x'] - (tile_size * 10) if self.color_no else tile_size*(7)
        self.relative_distance = ((tile_size * 10)  if self.color_no else tile_size*(7))
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        import time
        self.dirty_rect = self.rect.copy()
        
        self.dirty_rect.x += (53 + 100  if not self.color_no else 60 + 20)*rat
        
#        time.sleep(10000)
        self.dirty_rect.y = self.rect.y + (13 - 1)*rat
        self.dirty_rect.width = (82+2)*rat
        self.dirty_rect.height = (41+2)*rat
        
        self.collision_rect = self.dirty_rect.copy()
        self.collision_rect.x += 1
        self.collision_rect.y += 1
        self.collision_rect.width -= 2
        self.collision_rect.height -= 2
    #####################################################################################
    # --- User scripts used by update to run these methods depending on sprite state.
    
    def __script_event_deploy(self):
        """Executes during sprite deployment phase."""
        
        pass
    
    def __script_event_operational(self):
        """Executes on normal operation after sprite is fully deployed."""
        
        def _add_shot_to_queue():
            rect = self.collision_rect.copy()
#            rect.width -=770
            
            shot = Shot(self.COLOR, self.color_no, rect.copy())
            shot.create_inner_rect()
            self.queue_group.add(shot)
        self.relative_distance += self.block_size * ((self.diff_t * 1.0) / self.time_per_tick) 
        self.rect.x = (self.screen_size["x"] - self.relative_distance) if self.color_no else self.relative_distance
        
        # If both are equal.
        self.collision_rect.x = self.dirty_rect.x = self.rect.x + (53 if not self.color_no else 60)*rat
        
        if self.add_t >= self.next_shot_time:
            _add_shot_to_queue()
            self.next_shot_time += 5
    
    def __script_event_paused(self):
        """Change sprite state to pause."""
        
        def _add_shot_to_queue():
            rect = self.collision_rect.copy()
            rect.width -=20
            shot = Shot(self.COLOR, self.color_no, rect.copy())
            shot.create_inner_rect()
            self.queue_group.add(shot)
        
        if (not self.sprite_collided_with.alive()):
            self.state = "operational"
        
        if self.add_t >= self.next_shot_time:
            _add_shot_to_queue()
            self.next_shot_time += 5
    
    def __script_event_self_decimate(self):
        """Executes when its being decimated."""
        
        pass
    
    def __script_event_desecrate(self):
        """Executes when its fully destroyed."""
        
        pass
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
            
        elif self.state == "pause": 
            self.__script_event_paused()
            
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
        
        
class Mines(pygame.sprite.Sprite):
    #####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, color_no):
        '''Constructor.'''
        
        super(Mines, self).__init__()
        xxx, yyy = pygame.display.get_surface().get_size()
        self.screen_size = {'x':xxx, 'y':yyy}
        self.color_no = color_no
        self.COLOR = COLOR
        
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = ["Shots"] #transparant
        self.immune_list = []
        
        self.type = "Mine"
        self.health = 1
        self.inflict_damage = 1000
        
        self.collision_instant_self_kill = True
        self.collision_instant_destroy = True
        
        if self.COLOR == RED_GRAD: 
            F='r'
        elif self.COLOR == GREEN_GRAD:
            F='g'
        elif self.COLOR == TEAL_GRAD:
            F='t'
        
        # Unique compared to other sprites.
        foo = ['0', '1', '2', '3']
        self.loaded_image = pygame.image.load('data/colors/{}/Mines{}.png'.format(F, random.choice(foo))).convert_alpha()
        
        self.image = pygame.transform.flip(self.loaded_image, 1, 0) if self.color_no else self.loaded_image.copy()
        
        rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(rect.width*rat), int(rect.height*rat)))
        self.require_update = True
        
        self.define_rect()
        self.create_inner_rect()
        
        self.current_t = time.time()
        self.prev_t = 0
        #self.prev_t = time.time() #1
        self.diff_t = (self.current_t - self.prev_t) if self.prev_t else 0 #1
        self.time_per_tick = 1
        self.block_size = (65 - 1)*rat
        self.add_t = 0
        
        self.queue_group = pygame.sprite.Group()
        self.next_shot_time = 0
        
        self.state = "operational"
        
    def define_rect(self):
        """Create rect object for image blitting."""
        
        self.rect = self.image.get_rect()
        
        self.rect.x = self.screen_size['x'] - (tile_size * 8) if self.color_no else tile_size*(7)
        self.relative_distance = (tile_size * 8)  if self.color_no else tile_size*(7)
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        
        self.dirty_rect = self.rect.copy()
        
        self.dirty_rect.x += (7 if not self.color_no else 19)*rat
        self.dirty_rect.y = self.rect.y + 13*rat
        self.dirty_rect.width = 39*rat
        self.dirty_rect.height = 42*rat
        
        self.collision_rect = self.dirty_rect.copy()
        
        # Unique to sprite.
        self.collision_rect.height -= 2
    #####################################################################################
    # --- User scripts used by update to run these methods depending on sprite state.
    
    def __script_event_deploy(self):
        """Executes during sprite deployment phase."""
        
        pass
    
    def __script_event_operational(self):
        """Executes on normal operation after sprite is fully deployed."""
        pass
    
    def __script_event_paused(self):
        """Change sprite state to pause."""
        
        pass
        
    def __script_event_self_decimate(self):
        """Executes when its being decimated."""
        
        pass
    
    def __script_event_desecrate(self):
        """Executes when its fully destroyed."""
        
        pass
    #####################################################################################
    # --- Engine can use the following methods for stated operations.
    
    def update(self):
        """Updates the state of the sprite."""
        
        # Unique to this sprite.
        return
        
        self.current_t = time.time()
        self.diff_t = (self.current_t - self.prev_t) if self.prev_t else 0 #1
        self.add_t += self.diff_t
        
        if self.state == "operational": 
            self.__script_event_operational()
            
        elif self.state == "deploying": 
            self.__script_event_deploy()
            
        elif self.state == "self_decimate": 
            self.__script_event_self_decimate()
            
        elif self.state == "pause" and (not self.sprite_collided_with.alive()): 
            self.__script_event_paused()
        
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
        
class Cannon(pygame.sprite.Sprite):###
    #####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, color_no):
        '''Constructor.'''
        
        super(Cannon, self).__init__()
        
        self.color_no = color_no
        self.COLOR = COLOR
        xxx, yyy = pygame.display.get_surface().get_size()
        self.screen_size = {'x':xxx, 'y':yyy}
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = [] #transparant
        self.immune_list = []
        
        self.type = "Cannon"
        self.health = 2
        self.inflict_damage = 0
        
        self.collision_instant_self_kill = False
        self.collision_instant_destroy = False
        
        if self.COLOR == RED_GRAD: 
            F='r'
        elif self.COLOR == GREEN_GRAD:
            F='g'
        elif self.COLOR == TEAL_GRAD:
            F='t'
        
        # Unique compared to other sprites.
        self.loaded_image = pygame.image.load('data/colors/{}/Cannon.png'.format(F)).convert_alpha()
        
        self.image = pygame.transform.flip(self.loaded_image, 1, 0) if self.color_no else self.loaded_image.copy()
        
        rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(rect.width*rat), int(rect.height*rat)))
        self.require_update = True
        
        self.define_rect()
        self.create_inner_rect()
        
        self.current_t = time.time()
        self.prev_t = 0
        #self.prev_t = time.time() #1
        self.diff_t = (self.current_t - self.prev_t) if self.prev_t else 0 #1
        self.time_per_tick = 1
        self.block_size = (65 - 1)*rat
        self.add_t = 0
        
        self.queue_group = pygame.sprite.Group()
        self.next_shot_time = 13
        
        self.state = "operational"
        
    def define_rect(self):
        """Create rect object for image blitting."""
        
        self.rect = self.image.get_rect()
        
        self.rect.x = self.screen_size['x'] - (tile_size * 7) if self.color_no else tile_size*(4)
        self.relative_distance = (tile_size * 7)  if self.color_no else tile_size*(4)
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        
        self.dirty_rect = self.rect.copy()
        
        self.dirty_rect.x += (59 if not self.color_no else 66)*rat
        self.dirty_rect.y = self.rect.y + 9*rat
        self.dirty_rect.width = 68*rat
        self.dirty_rect.height = 45*rat
        
        self.collision_rect = self.dirty_rect.copy()
    #####################################################################################
    # --- User scripts used by update to run these methods depending on sprite state.
    
    def __script_event_deploy(self):
        """Executes during sprite deployment phase."""
        
        pass
    
    def __script_event_operational(self):
        """Executes on normal operation after sprite is fully deployed."""
        
        def _add_shot_to_queue():
        
            shot = Shot(self.COLOR, self.color_no, self.dirty_rect.copy())
            shot.create_inner_rect()
            self.queue_group.add(shot)
        
        if self.add_t >= self.next_shot_time:
            _add_shot_to_queue()
            self.next_shot_time += 20
            
    def __script_event_paused(self):
        """Change sprite state to pause."""
        
        self.__script_event_operational()
        
    def __script_event_self_decimate(self):
        """Executes when its being decimated."""
        
        pass
    
    def __script_event_desecrate(self):
        """Executes when its fully destroyed."""
        
        pass
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
            
        elif self.state == "pause": 
            self.__script_event_paused()
        
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
    
    
class Powerplant(pygame.sprite.Sprite):
    #####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, color_no):
        '''Constructor.'''
        
        super(Powerplant, self).__init__()
        
        self.color_no = color_no
        self.COLOR = COLOR
        xxx, yyy = pygame.display.get_surface().get_size()
        self.screen_size = {'x':xxx, 'y':yyy}
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = [] #transparant
        self.immune_list = []
        
        self.type = "Powerplant"
        self.health = 5
        self.inflict_damage = 0
        
        self.collision_instant_self_kill = False
        self.collision_instant_destroy = False
        
        if self.COLOR == RED_GRAD: 
            F='r'
        elif self.COLOR == GREEN_GRAD:
            F='g'
        elif self.COLOR == TEAL_GRAD:
            F='t'
        
        # Unique compared to other sprites.
        self.loaded_image = pygame.image.load('data/colors/{}/Powerplant.png'.format(F)).convert_alpha()
        
        self.image = pygame.transform.flip(self.loaded_image, 1, 0) if self.color_no else self.loaded_image.copy()
        rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(rect.width*rat), int(rect.height*rat)))
        self.require_update = True
        
        self.define_rect()
        self.create_inner_rect()
        
        self.current_t = time.time()
        self.prev_t = 0
        self.diff_t = (self.current_t - self.prev_t) if self.prev_t else 0 #1
        self.time_per_tick = 1
        self.block_size = (65 - 1)*rat
        self.add_t = 0
        
        self.queue_group = pygame.sprite.Group()
        self.next_shot_time = 13
        
        self.state = "operational"
        
    def define_rect(self):
        """Create rect object for image blitting."""
        
        self.rect = self.image.get_rect()
        
        self.rect.x = self.screen_size['x'] - (tile_size * 5) if self.color_no else tile_size*(3)
        self.relative_distance = (tile_size * 5)  if self.color_no else tile_size*(3)
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        
        self.dirty_rect = self.rect.copy()
        
        self.dirty_rect.x += (59 if not self.color_no else 66)*rat
        self.dirty_rect.y += 9*rat
        self.dirty_rect.width = 68*rat
        self.dirty_rect.height = 45*rat
        
        self.collision_rect = self.dirty_rect.copy()
    #####################################################################################
    # --- User scripts used by update to run these methods depending on sprite state.
    
    def __script_event_deploy(self):
        """Executes during sprite deployment phase."""
        
        pass
    
    def __script_event_operational(self):
        """Executes on normal operation after sprite is fully deployed."""
        
        # TODO: Need to increase base power building speed.
        
        pass
    
    def __script_event_paused(self):
        """Change sprite state to pause."""
        
        self.__script_event_operational()
    
    def __script_event_self_decimate(self):
        """Executes when its being decimated."""
        
        pass
    
    def __script_event_desecrate(self):
        """Executes when its fully destroyed."""
        
        pass
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
            
        elif self.state == "pause": 
            self.__script_event_paused
        
        elif self.state == "Withdraw":
            # TODO: Please perform a withdraw during impact.
            pass
        
        self.prev_t = self.current_t
    
    def pause(self):
        """Change sprite state to pause."""

        pass
        
    def get_created_sprites(self):
        """Get all sprites this sprite has queued."""
        return self.queue_group
            
    def sprite_under_collision(self, sprite):
        """States which sprite collided with this sprite."""
        
        self.sprite_collided_with = sprite
        
    def is_collided_with(self, sprite):
        """Check whether some other sprite collided with this sprite."""
        
        return self.collision_rect.colliderect(sprite.collision_rect)


class Deflector(pygame.sprite.Sprite):
    #####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, color_no):
        '''Constructor.'''
        
        super(Deflector, self).__init__()
        
        self.color_no = color_no
        self.COLOR = COLOR
        xxx, yyy = pygame.display.get_surface().get_size()
        self.screen_size = {'x':xxx, 'y':yyy}
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = [] #transparant
        self.immune_list = ["Shot"]
        
        self.type = "Rocket"
        self.health = 1000
        self.inflict_damage = 0
        self.base_dp = 4
        
        self.collision_instant_self_kill = False
        self.collision_instant_destroy = False
        
        if self.COLOR == RED_GRAD: 
            F='r'
        elif self.COLOR == GREEN_GRAD:
            F='g'
        elif self.COLOR == TEAL_GRAD:
            F='t'
            
        self.loaded_image = pygame.image.load('data/colors/{}/Deflector.png'.format(F) ).convert_alpha()
        
        self.image = pygame.transform.flip(self.loaded_image, 1, 0) if self.color_no else self.loaded_image.copy()
        rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(rect.width*rat), int(rect.height*rat)))
        self.require_update = True
        
        self.define_rect()
        self.create_inner_rect()
        
        self.current_t = time.time()
        self.prev_t = 0
        #self.prev_t = time.time() #1
        self.diff_t = (self.current_t - self.prev_t) if self.prev_t else 0 #1
        self.time_per_tick = 1
        self.block_size = (65 - 1)*rat
        self.add_t = 0
        
        self.queue_group = pygame.sprite.Group()
        
        self.state = "operational"
        
    def define_rect(self):
        """Create rect object for image blitting."""
        
        self.rect = self.image.get_rect()
        
        self.rect.x = self.screen_size['x'] - (tile_size * 9) if self.color_no else tile_size*(7)
        self.relative_distance = (tile_size * 9)  if self.color_no else tile_size*(7)
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        
        self.dirty_rect = self.rect.copy()
        self.dirty_rect.x += (58 if not self.color_no else 73)*rat
        self.dirty_rect.y = self.rect.y + 87 *rat
        self.dirty_rect.width = 64*rat
        self.dirty_rect.height = 20*rat
        
        self.collision_rect = self.dirty_rect.copy()
        
        self.collision_rect_wing_top = self.rect.copy()
        
        self.collision_rect_wing_top.x += (120 if not self.color_no else 68)*rat
        self.collision_rect_wing_top.y = self.rect.y + 59*rat
        self.collision_rect_wing_top.width = 5*rat
        self.collision_rect_wing_top.height = 9*rat
        
        self.collision_rect_wing_bottom = self.rect.copy()
        
        self.collision_rect_wing_bottom.x += (120 if not self.color_no else 68)*rat
        self.collision_rect_wing_bottom.y = self.rect.y + 121*rat
        self.collision_rect_wing_bottom.width = 5*rat
        self.collision_rect_wing_bottom.height = 9*rat
    #####################################################################################
    # --- User scripts used by update to run these methods depending on sprite state.
    
    def __script_event_deploy(self):
        """Executes during sprite deployment phase."""
        
        pass
    
    def __script_event_operational(self):
        """Executes on normal operation after sprite is fully deployed."""

        self.relative_distance += self.block_size * ((self.diff_t * 1.0) / self.time_per_tick) 
        self.rect.x = (self.screen_size["x"] - self.relative_distance) if self.color_no else self.relative_distance
        
        # If both are equal.
        self.collision_rect.x = self.dirty_rect.x = self.rect.x + ((58 if not self.color_no else 73))*rat
        self.collision_rect_wing_bottom.x = self.collision_rect_wing_top.x = self.rect.x + (120 if not self.color_no else 68)*rat
    
    def __script_event_paused(self):
        """Executes when its paused."""
        
        if (not self.sprite_collided_with.alive()):
            self.state = "operational"
    
    def __script_event_self_decimate(self):
        """Executes when its being decimated."""
        
        pass
    
    def __script_event_desecrate(self):
        """Executes when its fully destroyed."""
        
        pass
    
    def add_shot_to_queue(self):
        
        shot = Shot(self.COLOR, self.color_no, self.dirty_rect.copy())
        shot.create_inner_rect()
        self.queue_group.add(shot)
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

        elif self.state == "pause": 
            self.__script_event_paused()

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
        
        if sprite.type == "Shot":
            sprite.kill()
            self.add_shot_to_queue()
            return 
        self.sprite_collided_with = sprite
        
    def is_collided_with(self, sprite):
        """Check whether some other sprite collided with this sprite."""
        
        return True if (self.collision_rect.colliderect(sprite.collision_rect)
            or self.collision_rect_wing_top.colliderect(sprite.collision_rect)
            or self.collision_rect_wing_bottom.colliderect(sprite.collision_rect)
        ) else False
