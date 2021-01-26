import pygame
from pygame.locals import *

import os

import time
from threading import Thread

from HackEngine import HackEngine

#class Frames():
#    def __init__(self):
#        pass
#    def init(self, message):
#        self.message = message
#        self.prev_time = time.time()
#        self.current_time = time.time()
#        
#        self.second = False
#        
#        self.total_time = 0
#        self.frames = 0
#        
#    def one_frame_execute(self):
#    
#        self.current_time = time.time()
#        
#        self.time_difference = self.current_time - self.prev_time
#        self.total_time += self.time_difference
#        self.frames += 1
#        
#        if self.total_time >=1:
#            self.total_time = 0

#            self.text = "{:15} {:10}".format(str(self.frames)+ " fps", self.message)
#            if self.second:
#                os.system("clear")
#                print self.second.text
#                print self.text
#                print
#            else:
#                print self.text
#            self.fps = self.frames
#            self.frames = 0
#        
#        self.prev_time = self.current_time
#    
#    def secondary(self, frameobj):
#        self.second = frameobj
class Frames():
    def __init__(self):
        pass
    def init(self, message):
        self.message = message
        self.prev_time = time.time()
        self.current_time = time.time()
        
        self.total_time = 0
        self.frames = 0
        self.text = ""
    def one_frame_execute(self):
    
        self.current_time = time.time()
        
        self.time_difference = self.current_time - self.prev_time
        self.total_time += self.time_difference
        self.frames += 1
        
        if self.total_time >=1:
            self.total_time = 0
            print "{:15} {:10}".format(str(self.frames)+ " fps", self.message)
            self.fps = self.frames
            self.frames = 0
        
        self.prev_time = self.current_time

class HackGraphics():
    """Handles Graphic section of the game.
    
    It also handles screen transformation if necessary.  It just 
    uses the main thread to call the draw opton handled by HackingEngine."""
    
    def __init__(self):
    
        # Initialise python display.
        pygame.init()
        
        pygame.display.set_caption("C Hacking.")
        
        # TODO: Allow users to set custom or choose.
        size = (915, 635)
        self.size = size
        
        # TODO: Allow users to choose.
        # Get highest window mode and set to it.        
        modes = pygame.display.list_modes()
        
        # Declare all surfaces.
        self.default_surface = pygame.Surface(size)
        self.active_surface = pygame.Surface(size)
        self.alpha_surface = pygame.Surface(size)
        
        # Set screen resolution.
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode(size, pygame.NOFRAME)
        
         # Initiate the Hacking Engine.
        self.HackingEngine = HackEngine(self.screen)

        # Other variables.
        self.all_sprites_list = pygame.sprite.Group()
        
    def main_loop(self):
        done = False
        
        clock = pygame.time.Clock()
        
        self.Mouse = Mouse()
        
        # Make the background ready.
        self._prepare_background_defaults()
        
        frameOBJ = Frames()
        frameOBJ.init(":GraphicsEngine")
        frameOBJ.init("")
        self.screen.blit(self.default_surface, (0, 0))
        pygame.display.update()
        
        self.times = 0
        while not done: 
        
            # Update all sprites.
            self.Mouse.update()
            
            # --- Clear Screen.
            self.screen.fill((3, 3, 3))
            
            # ......
            # Draw all the sprites.
            self.HackingEngine.draw(self.screen)
            done = self.HackingEngine.Done
            
            pygame.display.update()#dirty_rects)
            
            #frameOBJ.one_frame_execute()
            # --- Limit to 60 frames per second
            clock.tick(60)
            
        
    def _prepare_background_defaults(self):
        self.default_surface.fill((3, 3, 3))
        
    def _run_graphics(self):
        self.main_loop()
        
class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super(Mouse, self).__init__()
        
        self.image = pygame.Surface([1, 1])
        self.image.fill((5,50,255))
        
        (self.point) = self.rect = self.image.get_rect()
        self.update()
        
    def update(self):
        (self.point) = (self.rect.x, self.rect.y) = pygame.mouse.get_pos()
        
    def changed_state(self):
        return False
        
        
if __name__ == "__main__":

    hack = HackGraphics()
    hack._run_graphics()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
