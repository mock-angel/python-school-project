#!/usr/bin/env python2.7
# CodeGraphics.py v1.3.5 DataWorm
import time
import sys
sys.path.insert(0, '../libs')

import pygame
from pygame.locals import *


import PycCleanup

import widgets
from widgets.Text import TextLine

from widgets.Mouse import Mouse
from widgets.Frames import Frames
from CodeEngine import CodeEngine

from constants import *

class CodeGraphicsEngine():
    """This is where the sprites are initialised and drawn.
    
    This codebase is different from other sets with a graphicsengine,
    because this tries to custom initialise and handle sprites."""
    
    def __init__(self):
        # Initialise python display.
        pygame.init()
        
        # Set Caption for window.
        pygame.display.set_caption("Code Clash")
        
        # TODO: Allow users to set custom or choose.
        self.size = size = SCREEN_SIZE
        
        # TODO: Allow users to choose.
        self.color_1, self.color_2 = GREEN_GRAD, TEAL_GRAD
        
        # Declare all surfaces.
        self.default_surface = pygame.Surface(size)
        self.active_surface = pygame.Surface(size)
        self.alpha_surface = pygame.Surface(size)
        
        if SCREEN_ICON: pygame.display.set_icon(pygame.image.load(SCREEN_ICON))
        
        # Set screen resolution.
        self.screen = pygame.display.set_mode(self.size)
        
        # Initiate the code Engine.
        self.CEngine = CodeEngine(self.color_1, self.color_2)
        
        # Set alpha to opaque.
        self.alpha_surface.set_alpha(0)
        
        # Other variables.
        self.all_sprites_list = pygame.sprite.Group()
        
        self.ex = True
        
    def start_loop(self):
        from widgets.Button import create_button_theme
        self.start_done = False
        
        def exit_button_click(self): self.start_done = True
        
        pygame.display.flip()
        
        create_surf = pygame.Surface
        
        screen_size = pygame.display.get_surface().get_size()
        main_text = TextLine(text="Code Clash", size = 34, font="Serif")
        main_text.rect.center = screen_size[0] / 2, screen_size[1] / 2
        
        surf = create_surf((200, 20)).convert()
        img_load = pygame.image.load
        img_scale = pygame.transform.scale
        
        panel = widgets.Panel()
        self.loading_page("", "Starting game", 3)
        text = TextLine(text="", size = 25, font="Serif")
        size = pygame.display.get_surface().get_size()
        
        start_game_img = img_load("data/StartGame.png").convert()
        options_img = img_load("data/Options.png").convert()
        quit_img = img_load("data/Quit.png").convert()
        
        s = start_game_img.get_size()
        start_game_img = img_scale(start_game_img, (s[0]/2, s[1]/2))
        options_img = img_scale(options_img, (s[0]/2, s[1]/2))
        quit_img = img_scale(quit_img, (s[0]/2, s[1]/2))
        
        start_game_b = widgets.Button(panel)
        start_game_b.theme = create_button_theme(start_game_img)
        start_game_b.rect.center = size[0], 5 * size[1]/8
        
        start_game_b.rect.center = size[0]/2, 5 * size[1]/8
        
        def rel(): self.start_done = True
        def quit(): 
            self.start_done = True
            self.done = True
            self.ex = False
        start_game_b.released(rel, ())
        quit_b = widgets.Button(panel)
        quit_b.theme = create_button_theme(quit_img)
        quit_b.rect.center = size[0]/2, 6 * size[1]/8
        quit_b.released(quit, ())
        
        b_group = widgets.ButtonGroup()
        b_group.add([start_game_b, quit_b])
        
        text.rect.center = size[0]/2, size[1]/2
        
        clock = pygame.time.Clock()
        
        start_time = time.time()
        
        while not self.start_done:
            self.screen.fill((0, 0, 0))
            event = pygame.event.wait()
            panel.update([event])
            
            if event.type == pygame.QUIT: # If user clicked close.
                self.start_done = True
                self.exited_screen()
                return 0
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.start_done = True
                    
                    self.exited_screen()
                    return 0
            
            main_text.draw(self.screen)
            text.draw(self.screen)
            b_group.draw(self.screen)
            pygame.display.flip()
        
        return 1
        
    def exited_screen(self):
        """exited_screen() - Displays exit screen for 1 second."""
        
        self.exited_done = False
        
        def exit_button_click(self): self.end_done = True
        
        
        panel = widgets.Panel()
        text = TextLine(text="GAME EXITED", size = 25, font="Serif")
        size = pygame.display.get_surface().get_size()
        
        text.rect.center = size[0]/2, size[1]/2
        
        clock = pygame.time.Clock()
        
        start_time = time.time()
        
        pygame.display.flip()
        while not self.exited_done:
            self.screen.fill((0, 0, 0))
            event = pygame.event.wait()
            panel.update([event])
            
            if event.type == pygame.QUIT: # If user clicked close
                self.exited_done = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exited_done = True
            
            text.draw(self.screen)
            
            pygame.display.flip()
            
            if time.time() - start_time >= 1:
                # Quit after 3 sec.
                self.exited_done = True
                self.CEngine.exit()
                
    def loading_page(self, sub_text, footer, wait_time):
            self.screen.fill((0, 0, 0))
            screen_size = pygame.display.get_surface().get_size()
            
            text = TextLine(text=footer, size = 18, font="Serif")
            text.rect.center = screen_size[0] / 2, screen_size[0] / 2
            
            main_text = TextLine(text="Code Clash", size = 34, font="Serif")
            main_text.rect.center = screen_size[0] / 2, screen_size[1] / 2
            
            sub_text = TextLine(text=sub_text, size = 14, font="Serif")
            sub_text.rect.center = screen_size[0] / 2, screen_size[1] / 2 +30
            
            text.draw(self.screen)
            main_text.draw(self.screen)
            sub_text.draw(self.screen)
            
            pygame.display.flip()     
            time.sleep(wait_time)
            
    def end_loop(self):
        self.end_done = False
        lp = self.loading_page
        lp("Player "+str(self.CEngine.defeated)+" won!", "Loading Statistics...", .5)
        
        
        def exit_button_click(self): self.end_done = True
        
        pygame.display.flip()
        
        panel = widgets.Panel()
        
        size = pygame.display.get_surface().get_size()
        text_set = set()
        
        if self.message == "GAME EXITED":
            text = TextLine(text=self.message, size = 25, font="Serif")
            text.rect.center = size[0]/2, size[1]/2
        
        stat_color_1 = self.CEngine.color_1_base.stats
        stat_color_2 = self.CEngine.color_2_base.stats
        
        if self.CEngine.defeated == 1:
            color_1_end_game = "Won"
            color_2_end_game = "Lost"
            
        elif self.CEngine.defeated == 2:
            color_1_end_game = "Lost"
            color_2_end_game = "Won"
            
        else:
            color_1_end_game = ""
            color_2_end_game = ""
        
        c_1_s = color_1_stats = self.CEngine.color_1_base.stats
        c_2_s = color_2_stats = self.CEngine.color_2_base.stats
        
        # STATS PAGE.
        # Now Write the Stats page.
        page_title_text = TextLine(text="STATS PAGE", size = 25, font="Serif")
        page_title_text.rect.centerx = size[0]/2
        page_title_text.rect.centery = size[1]/5
        text_set.add(page_title_text)
        
        # Deployed/Destroyed.
        color_1_text = TextLine(text=color_1_end_game, size = 18, font="Serif")
        color_1_text.rect.centerx = 3*size[0]/10
        color_1_text.rect.centery = 2*size[0]/10
        text_set.add(color_1_text)
        
        offset_center_y = 2*size[0]/10 + 20 
        
        # Const data.
        dep_color_1_x = 5*size[0]/20
        dest_color_1_x = 7*size[0]/20
        
        color_1_text_destroyed = TextLine(text="Destroyed", size = 15, font="Serif")
        color_1_text_destroyed.rect.centerx = dest_color_1_x
        color_1_text_destroyed.rect.centery = offset_center_y + 0
        text_set.add(color_1_text_destroyed)
        
        color_1_text_deployed = TextLine(text="Deployed", size = 15, font="Serif")
        color_1_text_deployed.rect.centerx = dep_color_1_x
        color_1_text_deployed.rect.centery = offset_center_y + 0
        text_set.add(color_1_text_deployed)
        
        color_2_text = TextLine(text=color_2_end_game, size = 18, font="Serif")
        color_2_text.rect.centerx = 7*size[0]/10
        color_2_text.rect.centery = 2*size[0]/10
        text_set.add(color_2_text)
        
        # Const data.
        dep_color_2_x = 13*size[0]/20
        dest_color_2_x = 15*size[0]/20
        
        color_2_text_destroyed = TextLine(text="Destroyed", size = 15, font="Serif")
        color_2_text_destroyed.rect.centerx = dest_color_2_x
        color_2_text_destroyed.rect.centery = offset_center_y + 0
        text_set.add(color_2_text_destroyed)
        
        color_2_text_deployed = TextLine(text="Deployed", size = 15, font="Serif")
        color_2_text_deployed.rect.centerx = dep_color_2_x
        color_2_text_deployed.rect.centery = offset_center_y + 0
        text_set.add(color_2_text_deployed)
        
        f = "Serif"
        c_1_s_dep = c_1_s["deployed"]
        c_1_s_dest = c_1_s["destroyed"]
        
        # Stat.1
        tank_dep_1 = TextLine(text=str(c_1_s_dep["Tank"]), size=18, font=f)
        tank_dep_1.rect.center = dep_color_1_x, offset_center_y + 20*1
        
        rocket_dep_1 = TextLine(text=str(c_1_s_dep["Rocket"]), size=18, font=f)
        rocket_dep_1.rect.center = dep_color_1_x, offset_center_y + 20*2
        
        deflector_dep_1 = TextLine(text=str(c_1_s_dep["Deflector"]), size=18, font=f)
        deflector_dep_1.rect.center = dep_color_1_x, offset_center_y + 20*3
        
        wall_dep_1 = TextLine(text=str(c_1_s_dep["Wall"]), size=18, font=f)
        wall_dep_1.rect.center = dep_color_1_x, offset_center_y + 20*4
        
        cannon_dep_1 = TextLine(text=str(c_1_s_dep["Cannon"]), size=18, font=f)
        cannon_dep_1.rect.center = dep_color_1_x, offset_center_y + 20*5
        
        mine_dep_1 = TextLine(text=str(c_1_s_dep["Mine"]), size=18, font=f)
        mine_dep_1.rect.center = dep_color_1_x, offset_center_y + 20*6
        
        powerplant_dep_1 = TextLine(text=str(c_1_s_dep["PowerPlant"]), size=18, font=f)
        powerplant_dep_1.rect.center = dep_color_1_x, offset_center_y + 20*7
        
        text_set |= set([tank_dep_1 , rocket_dep_1, deflector_dep_1, wall_dep_1, 
                        cannon_dep_1, mine_dep_1, powerplant_dep_1])
        
        tank_dest_1 = TextLine(text=str(c_1_s_dest["Tank"]), size=18, font=f)
        tank_dest_1.rect.center = dest_color_1_x, offset_center_y + 20*1
        
        rocket_dest_1 = TextLine(text=str(c_1_s_dest["Rocket"]), size=18, font=f)
        rocket_dest_1.rect.center = dest_color_1_x, offset_center_y + 20*2
        
        deflector_dest_1 = TextLine(text=str(c_1_s_dest["Deflector"]), size=18, font=f)
        deflector_dest_1.rect.center = dest_color_1_x, offset_center_y + 20*3
        
        wall_dest_1 = TextLine(text=str(c_1_s_dest["Wall"]), size=18, font=f)
        wall_dest_1.rect.center = dest_color_1_x, offset_center_y + 20*4
        
        cannon_dest_1 = TextLine(text=str(c_1_s_dest["Cannon"]), size=18, font=f)
        cannon_dest_1.rect.center = dest_color_1_x, offset_center_y + 20*5
        
        mine_dest_1 = TextLine(text=str(c_1_s_dest["Mine"]), size=18, font=f)
        mine_dest_1.rect.center = dest_color_1_x, offset_center_y + 20*6
        
        powerplant_dest_1 = TextLine(text=str(c_1_s_dest["PowerPlant"]), size=18,font=f)
        powerplant_dest_1.rect.center = dest_color_1_x, offset_center_y + 20*7
        
        power_dest_1 = TextLine(text=str(c_1_s["power_remaining"])+"/9", size=18,font=f)
        power_dest_1.rect.center = ((dest_color_1_x + dep_color_1_x)/2, 
                                                    offset_center_y + 20*8.5)
        
        health_dest_1 = TextLine(text=str(c_1_s["health"])+("/135"), size=18, font=f)
        health_dest_1.rect.center = ((dest_color_1_x + dep_color_1_x)/2, 
                                                    offset_center_y + 20*9.5)
        
        text_set |= set([tank_dest_1 , rocket_dest_1, deflector_dest_1, wall_dest_1,
         cannon_dest_1, mine_dest_1, powerplant_dest_1, power_dest_1, health_dest_1])
        
        c_2_s_dep = c_2_s["deployed"]
        c_2_s_dest = c_2_s["destroyed"]
        # Stat.2
        tank_dep_2 = TextLine(text=str(c_2_s_dep["Tank"]), size=18, font=f)
        tank_dep_2.rect.center = dep_color_2_x, offset_center_y + 20*1
        
        rocket_dep_2 = TextLine(text=str(c_2_s_dep["Rocket"]), size=18, font=f)
        rocket_dep_2.rect.center = dep_color_2_x, offset_center_y + 20*2
        
        deflector_dep_2 = TextLine(text=str(c_2_s_dep["Deflector"]), size=18, font=f)
        deflector_dep_2.rect.center = dep_color_2_x, offset_center_y + 20*3
        
        wall_dep_2 = TextLine(text=str(c_2_s_dep["Wall"]), size=18, font=f)
        wall_dep_2.rect.center = dep_color_2_x, offset_center_y + 20*4
        
        cannon_dep_2 = TextLine(text=str(c_2_s_dep["Cannon"]), size=18, font=f)
        cannon_dep_2.rect.center = dep_color_2_x, offset_center_y + 20*5
        
        mine_dep_2 = TextLine(text=str(c_2_s_dep["Mine"]), size=18, font=f)
        mine_dep_2.rect.center = dep_color_2_x, offset_center_y + 20*6
        
        powerplant_dep_2 = TextLine(text=str(c_2_s_dep["PowerPlant"]), size=18, font=f)
        powerplant_dep_2.rect.center = dep_color_2_x, offset_center_y + 20*7
        
        text_set |= set([tank_dep_2 , rocket_dep_2, deflector_dep_2, wall_dep_2, 
                        cannon_dep_2, mine_dep_2, powerplant_dep_2])
        
        tank_dest_2 = TextLine(text=str(c_2_s_dest["Tank"]), size=18, font=f)
        tank_dest_2.rect.center = dest_color_2_x, offset_center_y + 20*1
        
        rocket_dest_2 = TextLine(text=str(c_2_s_dest["Rocket"]), size=18, font=f)
        rocket_dest_2.rect.center = dest_color_2_x, offset_center_y + 20*2
        
        deflector_dest_2 = TextLine(text=str(c_2_s_dest["Deflector"]), size=18, font=f)
        deflector_dest_2.rect.center = dest_color_2_x, offset_center_y + 20*3
        
        wall_dest_2 = TextLine(text=str(c_2_s_dest["Wall"]), size=18, font=f)
        wall_dest_2.rect.center = dest_color_2_x, offset_center_y + 20*4
        
        cannon_dest_2 = TextLine(text=str(c_2_s_dest["Cannon"]), size=18, font=f)
        cannon_dest_2.rect.center = dest_color_2_x, offset_center_y + 20*5
        
        mine_dest_2 = TextLine(text=str(c_2_s_dest["Mine"]), size=18, font=f)
        mine_dest_2.rect.center = dest_color_2_x, offset_center_y + 20*6
        
        powerplant_dest_2 = TextLine(text=str(c_2_s_dest["PowerPlant"]), size=18,font=f)
        powerplant_dest_2.rect.center = dest_color_2_x, offset_center_y + 20*7
        
        power_dest_2 = TextLine(text=str(c_2_s["power_remaining"])+"/9", size=18,font=f)
        power_dest_2.rect.center = ((dest_color_2_x + dep_color_2_x)/2, 
                                                    offset_center_y + 20*8.5)
        
        health_dest_2 = TextLine(text=str(c_2_s["health"])+"/135", size=18, font=f)
        health_dest_2.rect.center = ((dest_color_2_x + dep_color_2_x)/2, 
                                                    offset_center_y + 20*9.5)
        
        text_set |= set([tank_dest_2 , rocket_dest_2, deflector_dest_2, wall_dest_2,
            cannon_dest_2, mine_dest_2, powerplant_dest_2, power_dest_2, health_dest_2])
        
        # Unit text.
        tank_text = TextLine(text="Tank", size = 17, font=f)
        tank_text.rect.center = size[0]/2, offset_center_y + 20*1
        
        rocket_text = TextLine(text="Rocket", size = 17, font=f)
        rocket_text.rect.center = size[0]/2, offset_center_y + 20*2
        
        deflector_text = TextLine(text="Deflector", size = 17, font=f)
        deflector_text.rect.center = size[0]/2, offset_center_y + 20*3
        
        wall_text = TextLine(text="Wall", size = 17, font=f)
        wall_text.rect.center = size[0]/2, offset_center_y + 20*4
        
        cannon_text = TextLine(text="Cannon", size = 17, font=f)
        cannon_text.rect.center = size[0]/2, offset_center_y + 20*5
        
        mine_text = TextLine(text="Mine", size = 17, font=f)
        mine_text.rect.center = size[0]/2, offset_center_y + 20*6
        
        powerplant_text = TextLine(text="PowerPlant", size = 17, font=f)
        powerplant_text.rect.center = size[0]/2, offset_center_y + 20*7
        
        power_remaining_text = TextLine(text="Power Remaining", size = 17, font=f)
        power_remaining_text.rect.center = size[0]/2, offset_center_y + 20*8.5
        
        health_remaining_text = TextLine(text="Health Remaining", size = 17, font=f)
        health_remaining_text.rect.center = size[0]/2, offset_center_y + 20*9.5
        
        li = set([tank_text, rocket_text, deflector_text, wall_text, cannon_text, mine_text, powerplant_text, power_remaining_text, health_remaining_text ])
        text_set |= li
        
        while not self.end_done:
            self.screen.fill((0, 0, 0))
            event = pygame.event.wait()
            panel.update([event])
            
            # Handle enents.
            if event.type == pygame.QUIT: # If user clicked close
                self.end_done = True
                 
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.end_done = True
                    
            # Draw now.
            for text in text_set:
                text.draw(self.screen)
            
            pygame.display.flip()
        if self.ex: self.exited_screen()
        
    def main_loop(self):
        self.done = False
        
        if not self.start_loop(): return
        
        self.CEngine.start()
        
        self.message = ""
        clock = pygame.time.Clock()
        
        self.Mouse = Mouse()
        
        # Make the background ready.
        self._prepare_background_using_defaults(self.color_1, self.color_2)
        
        f = Frames()
        f.init("CodeGraphics:")
        
        # Create Sprites.
        # ........
        
        self.screen.blit(self.default_surface, (0, 0))
        pygame.display.update()
        
        while not self.done: 
            
            # Processes all events for exit ect.
            self.done = self.__process_user_events()
            
            # --- Game logic should go here.
            dirty_rects = []
            
            # Update all sprites.
            self.Mouse.update()
            
            # --- Clear Screen.
            self.screen.blit(self.default_surface, (0, 0))
            
            # Draw all the sprites.
            # ......
            
            self.CEngine.draw(self.screen)
            self.done = self.CEngine.is_exited()

            # --- Update the screen.
            pygame.display.flip()
            
            # --- Limit to 1000 frames per second
            clock.tick(1000)
            
            f.one_frame_execute()
        if self.ex: self.end_loop()
    def __process_user_events(self):
        # TODO: Interchange True and False.
        
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT: # If user clicked close
                self.CEngine.exit()
                self.message = ""
                return True
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                self.CEngine.cursor_clicked(self.Mouse)
                
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.CEngine.exit()
                    self.message = ""
                    return True
                else:
                    self.CEngine.key_pressed(pygame.key.name(event.key))
                    
            return False

    ############################################################
    # Calculates necessary data based on display size.
    def __calculate_prerequisites(self):
        
        # Divide the screen's height with float(17).
        
        float_y = (self.size[1] / 17.0)
        
        # Round off the derived value and check how much it defers
        # from the original variable.
        
        rounded_y = int(round(float_y))
        
        diff_y = round((float_y - rounded_y) * 17)
        
        # NOTE: Now diff_y contains the space left unrendered, or the 
        # amount the box exceeds on either the top or bottom due
        # to the rounded_xy.
        
        # Now set tile scaling.
        
        self.tile_scaling = rounded_y
        
        # Calculate where the tiles should start rendering.
        
        Xposition = (self.size[0] - (rounded_y * 24) ) / 2
        Yposition =  diff_y / 2
        
        self.tile_start_position = (Xposition, Yposition)
        
    def __draw_color_menu_defaults(self, COLOR1, COLOR2):
        if COLOR1 == GREEN_GRAD:
            f1 = 'g'
        elif COLOR1 == TEAL_GRAD:
            f1 = 't'
        elif COLOR1 == RED_GRAD:
            f1 = 'r'
            
        if COLOR2 == GREEN_GRAD:
            f2 = 'g'
        elif COLOR2 == TEAL_GRAD:
            f2 = 't'
        elif COLOR2 == RED_GRAD:
            f2 = 'r'
    
        size_of_new_plyr_surface_tuple = (self.tile_scaling * 3, self.size[1])
        
        # --- Draw now.
        
        # Set surface to draw on.
        
        self.default_left_surface = pygame.Surface(size_of_new_plyr_surface_tuple)
        self.default_right_surface = pygame.Surface(size_of_new_plyr_surface_tuple)
        self.default_left_surface.fill(BACKGROUND)
        self.default_right_surface.fill(BACKGROUND)
        ###############################################################
        # Easier to draw from left and flip and draw and flip again.
        # TODO: Why not draw everything from left instead of flipping twice?
        draw_rect = pygame.draw.rect
        # LEFT
        draw_rect(self.default_left_surface, COLOR1[3], (8*0*rat, 0, 8, 1080*rat))
        draw_rect(self.default_left_surface, COLOR1[2], (8*1*rat, 0, 8, 1080*rat))
        draw_rect(self.default_left_surface, COLOR1[1], (8*2*rat, 0, 8, 1080*rat))
        draw_rect(self.default_left_surface, COLOR1[0], (8*3*rat, 0, 8, 1080*rat))
        draw_rect(self.default_left_surface, COLOR1[4], (8*4*rat, 0, 20*rat, 1080*rat))
        
        # RIGHT
        draw_rect(self.default_right_surface, COLOR2[3], (8*0*rat, 0, 8, 1080*rat))
        draw_rect(self.default_right_surface, COLOR2[2], (8*1*rat, 0, 8, 1080*rat))
        draw_rect(self.default_right_surface, COLOR2[1], (8*2*rat, 0, 8, 1080*rat))
        draw_rect(self.default_right_surface, COLOR2[0], (8*3*rat, 0, 8, 1080*rat))
        draw_rect(self.default_right_surface, COLOR2[4], (8*4*rat, 0, 20*rat, 1080*rat))
        ###############################################################
        
        # Now flip both surfaces to draw another bar
        flip = pygame.transform.flip
        self.default_left_surface = flip(self.default_left_surface, 1, 0)
        self.default_right_surface = flip(self.default_right_surface, 1, 0)
        
        # Draw bars.
        
        draw_rect(self.default_left_surface, COLOR1[4], (0, 0, 20*rat, 1080*rat))
        draw_rect(self.default_right_surface, COLOR2[4], (0, 0, 20*rat, 1080*rat))
        
        # Now flip left surface.
        
        self.default_right_surface = flip(self.default_right_surface, 1, 0)
        
    def __draw_board_pattern_defaults(self):
        
        # --- Load and set vars first.
        
        # Load default pattern and alpha images.
        img_load = pygame.image.load
        img_scale = pygame.transform.scale
        
        tile_pattern_alpha=img_load('data/board/tile_pattern_shade.png').convert_alpha()
        left_tile_alpha = img_load('data/board/left_tile_shade.png').convert_alpha()
        right_tile_alpha = pygame.transform.flip(left_tile_alpha, 1, 0)
        
        # Scale all the images to the required size.
        
        tile_scaling_tuple = (self.tile_scaling, self.tile_scaling)
        
        tile_pattern_alpha_scaled = pygame.transform.scale(tile_pattern_alpha, 
                                                           tile_scaling_tuple)
        left_tile_alpha_scaled = pygame.transform.scale(left_tile_alpha,
                                                        tile_scaling_tuple)
        right_tile_alpha_scaled = pygame.transform.scale(right_tile_alpha,
                                                        tile_scaling_tuple)
        
        # Derve start position and surface size.
        
        size_of_default_tile_surface_tuple =(self.tile_scaling*24, self.tile_scaling*17)
        
        # --- Draw now.
        
        # Set surface to draw on.
        self.default_tile_surface = pygame.Surface(size_of_default_tile_surface_tuple)
        self.default_tile_surface.fill(BACKGROUND)
         
        # Derive required variables from self classOBJ.
        
        X = Y = self.tile_scaling
        
        # Render all rows.
        for I in range(0, 18):
            # Render Row.
            for J in range(0, 24):
                self.default_tile_surface.blit(tile_pattern_alpha_scaled, (X*J, Y*I))
        
            self.default_tile_surface.blit(left_tile_alpha_scaled, (0, Y * I))
            self.default_tile_surface.blit(right_tile_alpha_scaled, (X * 23, Y * I))
    
    def __merge_all_default_surfaces(self):
        self.default_surface.blit(self.default_tile_surface, [self.tile_scaling * 3, 0])
        self.default_surface.blit(self.default_left_surface, [0, 0])
        self.default_surface.blit(self.default_right_surface, [self.tile_scaling*27, 0])
        
        self.default_surface.convert()
        
    def _prepare_background_using_defaults(self, COLOR1, COLOR2):
        self.__calculate_prerequisites()
        
        self.__draw_color_menu_defaults(COLOR1, COLOR2)
        self.__draw_board_pattern_defaults()
        self.__merge_all_default_surfaces()
    ############################################################
    
    def _run_graphics(self):
        self.main_loop()
    
    def refresh_active_screen(self):
        self.active_surface.blit(self.default_surface, [0, 0])
        
    def _draw_in_order(self):
        pass
    
if __name__ == "__main__":
    CG = CodeGraphicsEngine()
    CG._run_graphics()
    PycCleanup.clean()
