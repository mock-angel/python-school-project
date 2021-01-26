# EngineGraphics.py
import os
import time

import pygame
from pygame.locals import *

from threading import Thread
from UpdateEngine import UpdateEngine

from widgets.Frames import Frames
from widgets.Mouse import Mouse
from constants import *

class EngineGraphics():
    """Handles Graphic section of the Application.
    
    It also handles screen transformation if necessary.  It just 
    uses the main thread to call the draw opton handled by UpdateEngine."""
    
    def __init__(self):
        """"""
        # Initialise python display.
        pygame.init()
        
        pygame.display.set_caption(SCREEN_TITLE)
        if SCREEN_ICON: pygame.display.set_icon(pygame.image.load(SCREEN_ICON))
        
        # TODO: Allow users to set custom or choose.
        size = SCREEN_SIZE
        self.size = size
        
        # TODO: Allow users to choose.
        # Get highest window mode and set to it.        
        modes = pygame.display.list_modes()
        
        self.screen_color = SCREEN_COLOR
        
        # Declare all surfaces.
        self.default_surface = pygame.Surface(size)
        self.active_surface = pygame.Surface(size)
        self.alpha_surface = pygame.Surface(size)
        
        #self.splash_screen()
        
        # Set screen resolution.
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode(size, pygame.NOFRAME)
        
        # Initiate the Engine.
        self.UpdateEngine = UpdateEngine(self.screen, self)
        pygame.key.set_repeat(2000, 200)
        
        # Other variables.
        self.all_sprites_list = pygame.sprite.Group()
        
    def splash_screen(self):
        from SplashScreen.SplashScreen import SplashScreen
        ss = SplashScreen(self)
        ss.app_name = SCREEN_TITLE
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        screen = pygame.display.set_mode(ss.size, pygame.NOFRAME)
        while not ss.exit:
            ss.update()
            screen.fill(ss.screen_color)
            ss.draw(screen)
            pygame.display.update()
        
    def main_loop(self):
        done = False
        clock = pygame.time.Clock()
        
        self.Mouse = Mouse()
        
        # Make the background ready.
        self._prepare_background_defaults()
        
        frameOBJ = Frames()
        frameOBJ.init(":GraphicsEngine")
        self.screen.blit(self.default_surface, (0, 0))
        pygame.display.update()
        
        self.screen_change_queue = False
        
        self.times = 0
        while not done: 
        
            # Update all sprites.
            self.Mouse.update()
            
            # Look for Screen size change
            if self.screen_change_queue:
                
                self.UpdateEngine.pause()
                
                self.screen = pygame.display.set_mode(self.size, pygame.NOFRAME)
                
                self.screen.fill(self.screen_color)
                
                self.UpdateEngine.resume()
                self.screen_change_queue = False
                print "EngineGraphics: Screen Resolution Changed."
                
            # --- Clear Screen.
            self.screen.fill(self.screen_color)
            
            # ......
            # Draw all the sprites.
            self.UpdateEngine.draw(self.screen)
            done = self.UpdateEngine.Done
            
            
            pygame.display.update()#dirty_rects)
            
            frameOBJ.one_frame_execute()
            # --- Limit to GRAPHICS_FPS frames per second
            if GRAPHICS_FPS: clock.tick(GRAPHICS_FPS)
        
    def _prepare_background_defaults(self):
        
        self.default_surface.fill(self.screen_color)
        
    def _run_graphics(self):
        self.main_loop()
    
    def set_screen_size(self, size):
        self.size = size
        self.screen_change_queue = True
    
    def set_screen_color(self, tu_):
        self.screen_color = tu_
        
if __name__ == "__main__":
    # Test.
    graphics = EngineGraphics()
    graphics._run_graphics()
