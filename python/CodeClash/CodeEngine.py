# CodeEngine.py
import os
import time
from threading import Thread

import pygame
from pygame.locals import *

from CodeSprites import Rocket, Wall, Tank, Mines, Cannon, Powerplant, Deflector
from CodePlyrSprite import Base
from RandRadiant import RandRadiant
from constants import *

threads = []
class CodeEngine():
    '''All sprites run in this class.'''
    
    def __init__(self, COLOR1, COLOR2):
        
        self.defeated  = None
        
        # Used for the infinite loop in in update.
        
        self.Done = 0
        
        # Stores rects that need update at irreglar intervals of time.
        self.dirty_dirty_rects = []
        
        # DeployH ClassOBJ helps decide where to place the units.
        self.DeployH = RandRadiant()
        
        # Add the rows to the DeployH.
        for i in range(8):
            self.DeployH.create_new_branch( 'COLOR1_{}'.format(str(i)) )
            self.DeployH.create_new_branch( 'COLOR2_{}'.format(str(i)) )
        
        # --- Define Sprite Group classes.
        
        # All the units are split into different teams here.
        self.all_COLOR1_units_list = pygame.sprite.Group()
        self.all_COLOR2_units_list = pygame.sprite.Group()
        
        # All the controlls for unit selection goes here.
        self.plyr_menu = pygame.sprite.Group()
        
        # All units are stored here.
        self.all_units_list = pygame.sprite.Group()
        
        # All sprites are stored here.
        self.all_sprites_list = pygame.sprite.Group()
        
        # Define unit selection base.
        a = Base(COLOR1, 0, self.lost)
        b = Base(COLOR2, 1, self.lost)
        self.color_1_base = a
        self.color_2_base = b
        self.plyr_menu.add(a)
        self.plyr_menu.add(b)
        self.all_COLOR1_units_list.add(a)
        self.all_COLOR2_units_list.add(b)
        
        # --- Add units before game begines to test. 
        #self.add_rocket(COLOR2, 1)
        
    def start(self):
        # Start game process that updates 60 times per second.
        t1 = Thread(target=self.start_engine, args=() )
        t1.start()
        threads.append(t1)
    #######################################
    def __test_collision_of_all_units(self):
        """Checks if anything is collided."""
        self.collide_list = []
        
        for sprite_1 in self.all_COLOR1_units_list:
        
            for sprite_2 in self.all_COLOR2_units_list:
                
                if sprite_1.is_collided_with(sprite_2):
                    self.collide_list += [(sprite_1, sprite_2)]
                    
    def __process_all_sprite_unit_collisions(self):
        """If there is any registered collision, then perform operation."""
        
        def remove_sprite_from_branch(sprite):
            if not (sprite.type == "Shot") and not (sprite.type == "Base"):
            
                self.DeployH.del_element_from_branch(
                        str(sprite.row), 
                        sprite.branch
                )
        
        def add_sprite_to_screen_update_queue(sprite):
            """If sprites require an update to screen, add to queue."""
            if sprite.require_update:
                self.dirty_dirty_rects += [sprite]
        
#        collide_spr_tuple = collision_sprite_tuple
        
        for collide_spr_tuple in self.collide_list:
            
            # Set everything to not be destroyed at first.
            set_kill_1 = set_kill_2 = False
            
            # Tell the sprite to which other sprite it just collided with.
            collide_spr_tuple[0].sprite_under_collision(collide_spr_tuple[1])
            collide_spr_tuple[1].sprite_under_collision(collide_spr_tuple[0])
            
            # Check whether any one sprite is invisible to the other sprite.
            if (collide_spr_tuple[0].type in collide_spr_tuple[1].invisibility_list
                or  collide_spr_tuple[1].type in collide_spr_tuple[0].invisibility_list
                or collide_spr_tuple[0].invisibility_list == ["ALL"]
                or collide_spr_tuple[1].invisibility_list == ["ALL"]
            ):
                continue
                
            # If its not immune, perform actions. 
            if not (
                collide_spr_tuple[1].type in collide_spr_tuple[0].immune_list 
                or collide_spr_tuple[0].immune_list == ["ALL"]
            ):
                if (collide_spr_tuple[0].collision_instant_self_kill 
                    or collide_spr_tuple[1].collision_instant_destroy
                ):
                    set_kill_1 = True
                collide_spr_tuple[0].health -= collide_spr_tuple[1].inflict_damage
            
            
            if not (
                collide_spr_tuple[0].type in collide_spr_tuple[1].immune_list 
                or collide_spr_tuple[1].immune_list == ["ALL"]
            ):
                if (collide_spr_tuple[1].collision_instant_self_kill 
                    or collide_spr_tuple[0].collision_instant_destroy
                ):
                    # Check whether its immune...
                    set_kill_2 = True
                collide_spr_tuple[1].health -= collide_spr_tuple[0].inflict_damage
                
            set_kill_1 = True if collide_spr_tuple[0].health <= 0 else set_kill_1
            set_kill_2 = True if collide_spr_tuple[1].health <= 0 else set_kill_2
            
            # Pause both sprites if they both are meant to be alive.
            if not (set_kill_1 or set_kill_2):
                collide_spr_tuple[0].pause()
                collide_spr_tuple[1].pause()
                # Now show the object which sprite is causing the pause.
                
            # Kill the sprites if the flag is True. 
            if set_kill_1:
                
                spr1 = collide_spr_tuple[0]
                if spr1.type == "Base": return
                try:
                    if spr1.color_no == self.color_1_base.color_no:
                        self.color_2_base.stats["destroyed"][spr1.type] += 1
                    elif spr1.color_no == self.color_2_base.color_no:
                        self.color_1_base.stats["destroyed"][spr1.type] += 1 
                except KeyError:
                    pass
                collide_spr_tuple[0].kill()
                # FIXME: This part of the code needs SEVERE FIXING.
                try:
                    remove_sprite_from_branch(collide_spr_tuple[0])
                except:
                    pass
                
            if set_kill_2:
                spr2 = collide_spr_tuple[1]
                if spr2.type == "Base": return
                try:
                    if spr2.color_no == self.color_1_base.color_no:
                        self.color_1_base.stats["destroyed"][spr2.type] += 1
                    elif spr2.color_no == self.color_2_base.color_no:
                        self.color_2_base.stats["destroyed"][spr2.type] += 1 
                except KeyError:
                    pass
                collide_spr_tuple[1].kill()
                try:
                    remove_sprite_from_branch(collide_spr_tuple[1])
                except:
                    pass
#            add_sprite_to_screen_update_queue(collide_spr_tuple[0])
#            add_sprite_to_screen_update_queue(collide_spr_tuple[1])
    #######################################
    
    def include_all_sprites_in_queue(self):
        for sprite in self.all_units_list:
            created_sprites = sprite.get_created_sprites()
            
            if created_sprites == None:
                continue
                
            for created_sp in created_sprites:
                self.add_sprite(created_sp, created_sp.color_no)
            
    '''_run_updates'''
    #######################
    def _run_updates(self):
        self.plyr_menu.update()
        self.all_sprites_list.update()
        
        self.include_all_sprites_in_queue()
        
        # Collision thingy.
        self.__test_collision_of_all_units()
        self.__process_all_sprite_unit_collisions()
    #######################
    
    def lost(self, plyr_color):
        """Action if any player is defeated."""
        
        self.defeated = plyr_color
        
        _1, _2 = self.color_1_base.stats, self.color_2_base.stats
        
        _1["power_remaining"] = int(self.color_1_base.power)
        _1["health"] = self.color_1_base.health if self.color_1_base.health>0 else 0
        _2["power_remaining"] = int(self.color_2_base.power)
        _2["health"] = self.color_2_base.health if self.color_2_base.health>0 else 0
        
        self.exit()
        
    #######################################################
    # TODO: Try to use a common method for processing this.
    def add_rocket(self, COLOR, color_no):
        
        rocket = Rocket(COLOR, color_no)
        
        write_random = self.DeployH.write_random_number_to_branch_by_range
        
        # Check whether its possible to proceed with aquired power.
        # Now reduce the power.
        for base_sprite in self.plyr_menu:
            if base_sprite.color_no == color_no:
                if not base_sprite.check_power_req(4): return
                r = write_random((1, 15), 'COLOR{}_6'.format(str(color_no + 1)))
                if not r:return
                base_sprite.decrease_power(4)
                break
        
        

        rocket.rect.y = tile_size*int(r)
        rocket.row = int(r)
        rocket.branch = 'COLOR{}_6'.format(str(color_no + 1))
        rocket.create_inner_rect()
        #self.deployed(rocket)
        
        
        # --- Add units to sprite Group now.
        self.add_sprite(rocket, color_no)
        
    def add_wall(self, COLOR, color_no):
        wall = Wall(COLOR, color_no)
        
        write_random = self.DeployH.write_random_number_to_branch_by_range
        
        # Check whether its possible to proceed with aquired power.
        # Now reduce the power.
        for base_sprite in self.plyr_menu:
            if base_sprite.color_no == color_no:
                if not base_sprite.check_power_req(1): return
                r = write_random((1, 15), 'COLOR{}_4'.format(str(color_no + 1)))
                if not r:return
                base_sprite.decrease_power(1)
                break
        
        self.DeployH.DisplayAll()
        wall.rect.y = tile_size*(int(r) - 1)
        wall.row = int(r)
        wall.branch = 'COLOR{}_4'.format(str(color_no + 1))
        wall.create_inner_rect()
        
        # --- Add units to sprite Group now.
        self.add_sprite(wall, color_no)
        
    def add_tank(self, COLOR, color_no):
        tank = Tank(COLOR, color_no)
        
        write_random = self.DeployH.write_random_number_to_branch_by_range
        
        # Check whether its possible to proceed with aquired power.
        # Now reduce the power.
        for base_sprite in self.plyr_menu:
            if base_sprite.color_no == color_no:
                if not base_sprite.check_power_req(3): return
                
                r = write_random((1, 15), 'COLOR{}_6'.format(str(color_no + 1)))
                
                if not r:return
                base_sprite.decrease_power(3)
                break
        
        
        
        tank.rect.y = tile_size*int(r)
        tank.row = int(r)
        tank.branch = 'COLOR{}_6'.format(str(color_no + 1))
        tank.create_inner_rect()
        
        # --- Add units to sprite Group now.
        self.add_sprite(tank, color_no)
        
    def add_mines(self, COLOR, color_no):
        mines = [Mines(COLOR, color_no) for i in range(3)]
        
        del_ele = self.DeployH.del_element_from_branch
        write_random = self.DeployH.write_random_number_to_branch_by_range
        
        # Check whether its possible to proceed with aquired power.
        # Now reduce the power.
        for base_sprite in self.plyr_menu:
            if base_sprite.color_no == color_no:
                if not base_sprite.check_power_req(6): return
                r1 = write_random((1, 15), 'COLOR{}_5'.format(str(color_no + 1)))
                r2 = write_random((1, 15), 'COLOR{}_5'.format(str(color_no + 1)))
                r3 = write_random((1, 15), 'COLOR{}_5'.format(str(color_no + 1)))
                
                safe = False if not r1 or not r2 or not r3 else True
                
                if not safe:
                    if r1: del_ele(str(r1), 'COLOR{}_5'.format(str(color_no + 1)))
                    if r2: del_ele(str(r2), 'COLOR{}_5'.format(str(color_no + 1)))
                    if r3: del_ele(str(r3), 'COLOR{}_5'.format(str(color_no + 1)))
                    return
                base_sprite.decrease_power(6)
                
                break
        
        mines[0].rect.y = tile_size*int(r1)
        mines[1].rect.y = tile_size*int(r2)
        mines[2].rect.y = tile_size*int(r3)
        
        mines[0].row = int(r1)
        mines[1].row = int(r2)
        mines[2].row = int(r3)
        
        mines[0].branch = 'COLOR{}_5'.format(str(color_no + 1))
        mines[1].branch = 'COLOR{}_5'.format(str(color_no + 1))
        mines[2].branch = 'COLOR{}_5'.format(str(color_no + 1))
        
        mines[0].create_inner_rect()
        mines[1].create_inner_rect()
        mines[2].create_inner_rect()
        
        # --- Add units to sprite Group now.
        self.add_sprite(mines, color_no)

    def add_cannon(self, COLOR, color_no):
        cannon = Cannon(COLOR, color_no)
        
        write_random = self.DeployH.write_random_number_to_branch_by_range
        
        # Check whether its possible to proceed with aquired power.
        # Now reduce the power.
        for base_sprite in self.plyr_menu:
            if base_sprite.color_no == color_no:
                if not base_sprite.check_power_req(2): return
                
                r = write_random((1, 15), 'COLOR{}_3'.format(str(color_no + 1)))
                
                if not r:return
                base_sprite.decrease_power(2)
                break
        
        cannon.rect.y = tile_size * int(r)
        cannon.row = int(r)
        cannon.branch = 'COLOR{}_3'.format(str(color_no + 1))
        cannon.create_inner_rect()
        
        # --- Add units to sprite Group now.
        self.add_sprite(cannon, color_no)
        
        
    def add_powerplant(self, COLOR, color_no):
        powerplant = Powerplant(COLOR, color_no)

        write_random = self.DeployH.write_random_number_to_branch_by_range

        # Check whether its possible to proceed with aquired power.
        # and reduce the power.
        for base_sprite in self.plyr_menu:
            if base_sprite.color_no == color_no:
                if not base_sprite.check_power_req(7): return
                
                r = write_random([3, 7, 11], 'COLOR{}_1'.format(str(color_no + 1)))
                
                if not r: return 
                base_sprite.decrease_power(7)
                break

        powerplant.rect.y = tile_size*int(r)
        powerplant.row = int(r)
        powerplant.branch = 'COLOR{}_1'.format(str(color_no + 1))
        powerplant.create_inner_rect()
        
        # --- Add units to sprite Group now.
        self.add_sprite(powerplant, color_no)
    
    def add_deflector(self, COLOR, color_no):
        deflector = Deflector(COLOR, color_no)
        
        write_random = self.DeployH.write_random_number_to_branch_by_range
        
        # Check whether its possible to proceed with aquired power.
        # Now reduce the power.
        for base_sprite in self.plyr_menu:
            if base_sprite.color_no == color_no:
                if not base_sprite.check_power_req(5): return
                
                r = write_random((1, 15), 'COLOR{}_6'.format(str(color_no + 1)))
                
                if not r: return
                base_sprite.decrease_power(5)
                break
        
        deflector.rect.y = tile_size*((int(r)-1))
        deflector.row = int(r)
        deflector.branch = 'COLOR{}_6'.format(str(color_no + 1))
        deflector.create_inner_rect()
        
        # --- Add units to sprite Group now.
        self.add_sprite(deflector, color_no)
    
    def add_sprite(self, sprite, color_no):
        
        # --- Add units to sprite Group.
        c1_u_l, c2_u_l = self.all_COLOR1_units_list, self.all_COLOR2_units_list
        (c1_u_l if not color_no else c2_u_l).add(sprite)
        
        self.all_units_list.add(sprite)
        self.all_sprites_list.add(sprite)
        
        # FIXME: Find a way out of this thing.
        try:
            if self.color_1_base.color_no == sprite.color_no:
                self.color_1_base.stats["deployed"][sprite.type] += 1
                
            elif self.color_2_base.color_no == sprite.color_no:
                self.color_2_base.stats["deployed"][sprite.type] += 1
                
        except KeyError: # For every unadded sprites, including Shots.
            pass
            
        except AttributeError:# For Mines.
            for spr in sprite:
                if self.color_1_base.color_no == spr.color_no:
                    self.color_1_base.stats["deployed"][spr.type] += 1
                    
                elif self.color_2_base.color_no == spr.color_no:
                    self.color_2_base.stats["deployed"][spr.type] += 1
    #######################################################
    
    def process_sprite_selected(self, selected_spr):
        
        # Player menu.
        pm = []
        for sprite in self.plyr_menu: pm.append(sprite)

        if selected_spr == None: return
        
        if selected_spr.type == 'Selector':
            pass
        else: return None
        
        if selected_spr.unit == 'Rocket Selector' and pm[selected_spr.color_no]:
            self.add_rocket(selected_spr.COLOR, selected_spr.color_no)
            
        elif selected_spr.unit == 'Wall Selector' and pm[selected_spr.color_no]:
            self.add_wall(selected_spr.COLOR, selected_spr.color_no)
            
        elif selected_spr.unit == 'Tank Selector' and pm[selected_spr.color_no]:
            self.add_tank(selected_spr.COLOR, selected_spr.color_no)
            
        elif selected_spr.unit == 'Mines Selector' and pm[selected_spr.color_no]:
            self.add_mines(selected_spr.COLOR, selected_spr.color_no)
            
        elif selected_spr.unit == 'Cannon Selector' and pm[selected_spr.color_no]:
            self.add_cannon(selected_spr.COLOR, selected_spr.color_no)
            
        elif selected_spr.unit == 'Powerplant Selector' and pm[selected_spr.color_no]:
            self.add_powerplant(selected_spr.COLOR, selected_spr.color_no)
        
        elif selected_spr.unit == 'Deflector Selector' and pm[selected_spr.color_no]:
            self.add_deflector(selected_spr.COLOR, selected_spr.color_no)
            
    def calculate_dirty_dirty_rects_frm_plyr_menu_and_return_sprites(self):
        self.sprites = []
        
        for menu in self.plyr_menu:
            self.sprites += list(menu.return_sprites()) 
        
        for sprite in self.sprites:
            self.dirty_dirty_rects += [sprite.rect]

        return self.sprites
        
    def draw(self, surface):
    
        temp_sprite_group = pygame.sprite.Group()
        
        calc_dirty = self.calculate_dirty_dirty_rects_frm_plyr_menu_and_return_sprites()
        
        temp_sprite_group.add(*calc_dirty )
        
        temp_sprite_group.draw(surface)
        temp_sprite_group.empty()

        self.all_sprites_list.draw(surface)
        
    def get_dirty_rects(self):
        """Collect all the rects that have the sprites for updating."""
        
        for dirty_sprite in self.all_sprites_list:
            if dirty_sprite.require_update: yield dirty_sprite.rect
            
            else: continue

        for dirty_rect in self.dirty_dirty_rects: 
            yield dirty_rect

        self.dirty_dirty_rects = []
        
        
    def cursor_clicked(self, Mouse):
        
        copied_group = pygame.sprite.Group()
        
        copied_group.add([sprite for sprite in self.plyr_menu])
        
        # Checks whether the mouse hit any base.
        selected_option_sprite = pygame.sprite.spritecollideany(Mouse, copied_group)
        
        # If it hits any base, then send the sprite its related to, to add if possible.
        if selected_option_sprite: 
            self.process_sprite_selected(selected_option_sprite.mouse_clicked(Mouse))
        
        copied_group.empty()
    
    def key_pressed(self, key):
        """key_pressed(key) - Called on keypress and adds units based on the numpress"""
        digits = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
        spr_fun = None
        
        # For normal numbers above alphabets on keyboard.
        if len(key) == 1 and key in digits:
            tu_ = self.color_1_base.COLOR, self.color_1_base.color_no
            if key == '1': spr_fun = self.add_wall
            if key == '2': spr_fun = self.add_cannon
            if key == '3': spr_fun = self.add_tank
            if key == '4': spr_fun = self.add_rocket
            if key == '5': spr_fun = self.add_deflector
            if key == '6': spr_fun = self.add_powerplant
        
        # For numpress events on the numpad.
        if len(key) == 3 and key[1] in digits:
            tu_ = self.color_2_base.COLOR, self.color_2_base.color_no
            if key[1] == '1': spr_fun = self.add_wall
            if key[1] == '2': spr_fun = self.add_cannon
            if key[1] == '3': spr_fun = self.add_tank
            if key[1] == '4': spr_fun = self.add_rocket
            if key[1] == '5': spr_fun = self.add_deflector
            if key[1] == '6': spr_fun = self.add_powerplant
            
        if spr_fun: spr_fun(tu_[0], tu_[1])
        
    def exit(self):
        self.Done = 1

    def start_engine(self):
        clock = pygame.time.Clock()
      
        while not self.Done:
            
            self._run_updates()
            
            clock.tick(64)
            
    def is_exited(self):
        return self.Done

