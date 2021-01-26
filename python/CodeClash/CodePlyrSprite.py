# CodePlyrSprite.py.
import time

import pygame
from pygame.locals import *

from constants import *

#################################################################
class Base(pygame.sprite.Sprite):
    ####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, color_no, lost_callback):
        '''Constructor.'''
        
        super(Base, self).__init__()
        
        self.lost_c = lost_callback
        
        self.color_no = color_no
        self.COLOR = COLOR
        x, y = pygame.display.get_surface().get_size()
        
        deployed_dict = {
        "Tank" :0,
        "Cannon":0,
        "Wall":0,
        "Deflector":0,
        "Mine":0,
        "Rocket" :0,
        "PowerPlant" :0,
        }
        destroyed_dict = {
        "Tank" :0,
        "Cannon":0,
        "Wall":0,
        "Deflector":0,
        "Mine":0,
        "Rocket" :0,
        "PowerPlant" :0,
        }
        lost_dict = {
        "Tank" :0,
        "Cannon":0,
        "Wall":0,
        "Deflector":0,
        "Mine":0,
        "Rocket" :0,
        "PowerPlant" :0,
        }
        
        self.stats = {
        
        "deployed": deployed_dict,
        "destroyed": destroyed_dict,
#        "lost": lost_dict,
        "health": 0,
        "power_remaining": 0,
        }
        
        
        self.screen_size = {'x':x, 'y':y}
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = [] #transparant
        self.immune_list = ["ALL"]
        
        self.type = "Base"
        self.health = 135
        self.inflict_damage = 0
        
        self.collision_instant_self_kill = False
        self.collision_instant_destroy = True
        
        if self.COLOR == RED_GRAD: 
            F='r'
        elif self.COLOR == GREEN_GRAD:
            F='g'
        elif self.COLOR == TEAL_GRAD:
            F='t'
            
        self.loaded_image = pygame.Surface((tile_scaling*3, self.screen_size['y'])).convert()
        
        self.image = self.loaded_image.copy()
        
        self.require_update = False
        
        self.define_rect()
        self.create_inner_rect()
        
        self.current_t = time.time()
        self.prev_t = 0
        self.diff_t = (self.current_t - self.prev_t) if self.prev_t else 0 #1
        self.time_per_tick = 1
        self.block_size = (65 - 1)*rat
        self.add_t = 0
        
        self.queue_group = pygame.sprite.Group()
        self.power = 0
        
        self.init_sprites()    
            
        self.state = "operational"
    
    def init_sprites(self):
        """Initialise sprites."""
        
        # TODO: Seperate using base_part naming convention.
        
        # Declare sprite groups.
        self.all_sprites_requiring_power_param = pygame.sprite.Group()
        self.sprite_requiring_health_param = pygame.sprite.Group()
        self.all_selectors_list = pygame.sprite.Group()
        self.all_units_created_list = pygame.sprite.Group()
        self.all_sprites_in_class = pygame.sprite.Group()
        
        # BaseUnitSelection.
        self.all_selectors_list.add( BaseUnit(self.COLOR, "Special Unit Selector", self.color_no) )
        self.all_selectors_list.add( BaseUnit(self.COLOR, 'Heavy Tank Selector', self.color_no) )
        self.all_selectors_list.add( BaseUnit(self.COLOR, 'Powerplant Selector', self.color_no) )
        self.all_selectors_list.add( BaseUnit(self.COLOR, 'Mines Selector', self.color_no) )
        self.all_selectors_list.add( BaseUnit(self.COLOR, 'Deflector Selector', self.color_no) )
        self.all_selectors_list.add( BaseUnit(self.COLOR, 'Rocket Selector', self.color_no) )
        self.all_selectors_list.add( BaseUnit(self.COLOR, 'Tank Selector', self.color_no) )
        self.all_selectors_list.add( BaseUnit(self.COLOR, 'Cannon Selector', self.color_no) )
        self.all_selectors_list.add( BaseUnit(self.COLOR, 'Wall Selector', self.color_no) )
        
        self.all_sprites_requiring_power_param.add(self.all_selectors_list)
        
        # BasePowerBar.
        self.all_sprites_requiring_power_param.add( BasePowerBar(self.COLOR, self.color_no) )
        self.sprite_requiring_health_param.add( BaseHealthBar(self.COLOR, self.color_no) )
        
        self.all_sprites_in_class.add(self.all_sprites_requiring_power_param)
        self.all_sprites_in_class.add(self.sprite_requiring_health_param)
        
    def define_rect(self):
        """Create rect object for image blitting."""
        
        self.rect = self.image.get_rect()
        
        self.rect.x = self.screen_size['x'] - (tile_scaling * 3) if self.color_no else 0
        self.relative_distance = (tile_scaling * 3)  if self.color_no else 0
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        
        self.dirty_rect = self.rect.copy()
        self.collision_rect = self.dirty_rect.copy()
        
    def get_stats(self):
        
        self.stats["health"] = (self.health*100) /135
        self.stats["power"] = self.power*10
        return self.stats
    ####################################################################################
    # --- User scripts used by update to run these methods depending on sprite state.
    
    def __script_event_operational(self):
        """Executes on normal operation after sprite is fully deployed."""
        
        # Update attributes and essentials.
        self.update_power()
        self.all_sprites_requiring_power_param.update(self.power)
        self.sprite_requiring_health_param.update(self.health)
        self.all_units_created_list.update()
        if self.health <= 0: self.lost_c(self.color_no)
        
    def __script_event_paused(self):
        """Executes when its paused."""
        pass
    
    def update_power(self):
        '''Update self.power with respect to time.'''
    
        self.current_t = time.time()
        
        if self.prev_t: 
            diff_t = (self.current_t - self.prev_t)
            self.power += ((diff_t*1.0)/self.time_per_tick)
            
            # Never let power go beyond 9.
            if self.power> 9: self.power = 9
            
        self.prev_t = self.current_t
    
    def check_power_req(self, power_to_compare):
        """check_power_req(power) -> bool. returns True if the amount of
        power passed can be removed from the base, else false is returned."""
        return True if self.power >= power_to_compare else False
        
    def decrease_power(self, power_decrease_var) :
        """decrease_power(value) -> None. Decrease the power by passed value."""
        self.power -= power_decrease_var
        
    def mouse_clicked(self, mouse):
        """Check whether mouse collides with any Selection sprite."""
        return pygame.sprite.spritecollideany(mouse, self.all_selectors_list)
    ####################################################################################
    # --- Engine can use the following methods for stated operations.
    
    def update(self):
        """Updates the state of the sprite."""
        
        self.current_t = time.time()
        self.diff_t = (self.current_t - self.prev_t) if self.prev_t else 0 #1
        self.add_t += self.diff_t
        
        if self.state == "operational": self.__script_event_operational()
        elif self.state == "pause": self.__script_event_paused()
        
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
        self.health -= self.sprite_collided_with.base_dp
        
    def return_dirty_sprites(self):
        """return_dirty_sprites() -> generator.Collect sprites that
        have changed their state and requires an update in the screen."""
        
        for sprite in self.all_sprites_in_class:
            if sprite.changed_state(): yield sprite   
    
    def return_sprites(self):
        """Returns all the sprites in menu bar."""
        
        return self.all_sprites_in_class
    
    def is_collided_with(self, sprite):
        """Check whether some other sprite collided with this sprite."""
        
        return self.collision_rect.colliderect(sprite.collision_rect)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
#################################################################


#################################################################
class BasePowerBar(pygame.sprite.Sprite):
    ####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, color_no):
        '''Constructor.'''
        
        super(BasePowerBar, self).__init__()
        
        self.color_no = color_no
        self.COLOR = COLOR
        
        x, y = pygame.display.get_surface().get_size()
        
        self.screen_size = {'x':x, 'y':y}
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = [] #transparant
        self.immune_list = []
        
        self.type = "BasePowerBar"
        self.inflict_damage = 0
        
        if self.COLOR == RED_GRAD: 
            F='r'
        elif self.COLOR == GREEN_GRAD:
            F='g'
        elif self.COLOR == TEAL_GRAD:
            F='t'
            
        self.block_size = block_size
        img_load = pygame.image.load
        
        d = 'data/colors/{}/'
        dark_shade, light_shade = d+'dark_power_shade.png', d+'light_power_shade.png' 
        
        self.loaded_image_dark = img_load(dark_shade.format(F) ).convert_alpha()
        self.loaded_image_light = img_load(light_shade.format(F) ).convert_alpha()
        self.default_image = self.loaded_image_dark.copy()
        self.default_image.blit(self.loaded_image_light, (0, 0))
        self.image = pygame.Surface([20*rat, self.screen_size['y']]).convert_alpha()
        self.image.fill(self.COLOR[4])
        self.image_buffer = self.image.copy()
        
        self.define_rect()
        self.create_inner_rect()
        
        self.require_update = True
        
        self.state = "operational"
        self.prev_height = 0
        
    def define_rect(self):
        """Create rect object for image blitting."""
        
        self.rect = self.image.get_rect()
        self.rect.x = (self.screen_size['x'] - 20*rat) if self.color_no else 0
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        
        self.dirty_rect = self.rect.copy()
        self.collision_rect = self.dirty_rect.copy()
    ####################################################################################
    # --- User scripts used by update to run these methods depending on sprite state.
    
    def ____clear(self):
        if self.height == self.prev_height:
            return
        self.image_buffer=pygame.Surface([20*rat,self.screen_size['y']]).convert_alpha()
        self.image_buffer.fill(self.COLOR[4])
    
    def ____draw_height(self):
        
        if self.height == self.prev_height:
            return
        
        # Make sure the height is always positive.
        self.height = 0 if self.height < 0 else self.height
        
        self.image_buffer.blit(
            self.default_image,
            (0, self.screen_size['y'] - self.height),
            (0, self.screen_size['y'] - self.height, 20*rat, self.height)
        )
        
        self.image.blit(self.image_buffer, (0, 0))
    ####################################################################################
    # --- Engine can use the following methods for stated operations.
    
    def update(self, power):
        """Updates the state of the sprite."""
        
        self.height = int(power * self.block_size)
        
        self.____clear()
        self.____draw_height()
        
        self.prev_height = self.height
        
    def changed_state(self):
        return True
#################################################################

#################################################################
class BaseHealthBar(pygame.sprite.Sprite):
    ####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, color_no):
        '''Constructor.'''
        
        super(BaseHealthBar, self).__init__()
        
        self.color_no = color_no
        self.COLOR = COLOR
        
        x, y = pygame.display.get_surface().get_size()
        
        self.screen_size = {'x':x, 'y':y}
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = [] # Transparant.
        self.immune_list = []
        
        self.type = "BasePowerBar"
        self.inflict_damage = 0
        
        if self.COLOR == RED_GRAD: F='r'
        elif self.COLOR == GREEN_GRAD: F='g'
        elif self.COLOR == TEAL_GRAD: F='t'
            
        self.block_size = block_size
        h = 'data/board/red_health_bar.png'
        self.loaded_image = pygame.image.load(h.format(F) ).convert_alpha()
        
        self.image = pygame.Surface([20*rat, self.screen_size['x']]).convert_alpha()
        self.image.fill(self.COLOR[4])
        self.image_buffer = self.image.copy()
        
        
        self.define_rect()
        self.create_inner_rect()
        
        self.require_update = True
        
        self.state = "operational"
        
        self.prev_height = 0
        
    def define_rect(self):
        """Create rect object for image blitting."""
        
        self.rect = self.image.get_rect()
        
        self.rect.x = (self.screen_size['x'] - block_size - (40*rat)) \
                                            if self.color_no else block_size + (20*rat)
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        
        self.dirty_rect = self.rect.copy()
        
        self.collision_rect = self.dirty_rect.copy()
    ####################################################################################
    # --- User scripts used by update to run these methods depending on sprite state.
    
    def ____clear(self):
    
        if self.height == self.prev_height:
            return
            
        self.image_buffer=pygame.Surface([20*rat,self.screen_size['y']]).convert_alpha()
        self.image_buffer.fill(self.COLOR[4])
    
    def ____draw_height(self):
        
        if self.height == self.prev_height:
            return
        
        # Make sure the height is always positive.
        self.height = 0 if self.height < 0 else self.height
        
        self.image_buffer.blit(
            self.loaded_image,
            (0, self.screen_size['y'] - self.height),
            (0, self.screen_size['y'] - self.height, 20*rat, self.height)
        )
        
        self.image.blit(self.image_buffer, (0, 0))
    ####################################################################################
    # --- Engine can use the following methods for stated operations.
    
    def update(self, health):
        """Updates the state of the sprite."""

        self.height = int((135 - health) * 8) *rat
        
        self.____clear()
        self.____draw_height()
        
        self.prev_height = self.height
        
    def changed_state(self):
        return True
#################################################################


class BaseUnit(pygame.sprite.Sprite):
    ####################################################################################
    # --- Sprite initialisation.
    
    def __init__(self, COLOR, unit, color_no):
        """The player base the player units can interac with.
        
        THe player who defeatsthe opponent's base wins the game."""
        
        super(BaseUnit, self).__init__()
        
        self.unit = unit
        self.color_no = color_no
        self.COLOR = COLOR
        
        x, y = pygame.display.get_surface().get_size()
        
        self.screen_size = {'x':x, 'y':y}
        
        self.__init()
        
    def __init(self):
        """Initialises all variables and sets everything to its default.."""
        
        self.invisibility_list = [] # is invisible to list of sprites.
        self.immune_list = []
        
        self.type = "Selector"
        
        if self.unit == 'Special Unit Selector':
            u = '9'
        if self.unit == 'Heavy Tank Selector':
            u = '8'
        if self.unit == 'Powerplant Selector':
            u = '7'
        if self.unit == 'Mines Selector':
            u = '6'
        if self.unit == 'Deflector Selector':
            u = '5'
        if self.unit == 'Rocket Selector':
            u = '4'
        if self.unit == 'Tank Selector':
            u = '3'
        if self.unit == 'Cannon Selector':
            u = '2'
        if self.unit == 'Wall Selector':
            u = '1'
        
        self.number = u
        
        if self.COLOR == RED_GRAD: F = 'r'
        if self.COLOR == GREEN_GRAD: F = 'g'
        if self.COLOR == TEAL_GRAD: F = 't'
        
        # Set surface to draw on.
        self.alpha = 160
        f = 'data/colors/{}/{}.png'.format(F, u)
        self.loaded_image = pygame.image.load(f).convert()
        
        self.image = pygame.transform.scale(self.loaded_image, (block_size, block_size))
        self.image.set_alpha(self.alpha)
        
        self.require_update = True
        
        self.define_rect()
        self.create_inner_rect()
        
        self.state = "operational"
        
    def define_rect(self):
        """Create rect object for image blitting."""
        
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_size['x'] - self.rect.width - 20*rat \
                                                        if self.color_no else 20*rat
        self.rect.y = (9-int(self.number)) * self.rect.height
        
    def create_inner_rect(self):
        """Creates dirty_rect and collision_rect objects."""
        
        self.dirty_rect = self.rect.copy()
        self.collision_rect = self.dirty_rect.copy()
    ####################################################################################
    # --- Engine can use the following methods for stated operations.
    
    def update(self, power):
        '''Update Image State.'''
        
        # Make image dim if the reqired power isn't available.
        if int(self.number) <= power and not (self.alpha == 255):
            self.alpha = 255
            self.require_update = True
        elif int(self.number) > power and not (self.alpha == 160):
            self.alpha = 160
            self.require_update = True
                    
        self.image.set_alpha(self.alpha)
        
    def changed_state(self): # Dead.
        """Tells the graphics module when the updates are required."""
        
        if self.require_update == True:
            self.require_update = False
            val = True
            
        else: val = False
        return val
#################################################################
