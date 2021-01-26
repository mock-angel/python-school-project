# UpdateEngine.py
import os
import time
from threading import Thread

import pygame
from pygame.locals import *

from widgets.Button import Button, ButtonGroup, create_button_theme
from widgets.Panel import Panel
from widgets.Loading import Loading
from widgets.Frames import Frames
from widgets.Mouse import Mouse

from constants import *

threads = []

engine = None

class UpdateEngine():
    '''All sprites run in this class.'''
    
    def __init__(self, surface, graphics_engine):
        global engine
        engine = self
        self.surface = surface
        self.graphics_engine = graphics_engine
        
        self.paused = False
        self.pause_initiated = False
        # Used for the infinite loop in in update.
        self.Done = 0
        
        # --- Define Sprite Group classes.
        
        self.some_group = pygame.sprite.Group() # Dummy statement.
        
        # All sprites are stored here. 
        self.all_sprites_list = pygame.sprite.Group() # Dummy statement.
        
        # --- Add units before game begines to test. 
        
        self.panel = Panel()
        self.panel.set_primary()
#        self.title_sprites_list = TitleBar(self.panel) # for titlebar if required.
        
        self.loading = Loading()
        self.main_app = main_app(self)
        
        self.main_app.load(self.loading) # Loading.
        
        # Start game process that updates 64 times per second.
        t1 = Thread(target=self.start_engine, args=() )
        t1.start()
        threads.append(t1)
        
    def __del__(self):
        for thread in threads:
            thread.join()
    
    def pause(self):
        self.paused = True
        while not self.pause_initiated:
            pass
            
    def resume(self):
        self.paused = False
        while not self.running:
            pass
        
        self.pause_initiated = False
    #######################################################
    def _run_updates(self):
        
        if self.paused:
            self.running = False
            self.pause_initiated = True
            return
        self.running = True
        
        events = pygame.event.get()
        self.panel.update(events)
        self.main_app.handle_event(events)
        
        self.main_app.update()
        
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.exit()
    
    
    #######################################################
    
    def set_screen_color(self, tu_):
        self.graphics_engine.set_screen_color(tu_)
        
    def draw(self, surface):
        pass
        # make sure system doesn't blit all the nodes to itself first.
        
        self.main_app.draw(surface)
        
    def set_surface(self, surface):
        self.surface = surface
        
    def exit(self):
        self.Done = 1
        
    def start_engine(self):
        clock = pygame.time.Clock()
        self.Frameobj = Frames()
        self.Frameobj.init(":GameEngine")
        while not self.Done:
      
            self._run_updates()
            self.Frameobj.one_frame_execute()
            
            if UPDATE_FPS: clock.tick(UPDATE_FPS)
        
def get_engine():
    return engine
