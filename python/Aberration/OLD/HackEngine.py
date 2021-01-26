import os
import time

import pygame
from pygame.locals import *

from Abberation import Abberation
from system.widgets.Panel import Panel
from threading import Thread
from system.widgets.Button import Button, ButtonGroup, create_button_theme

threads = []

engine = None

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

class HackEngine():
    '''All sprites run in this class.'''
    
    def __init__(self, surface):
        global engine
        engine = self
        self.surface = surface
        
        # Used for the infinite loop in in update.
        self.Done = 0
        
        # --- Define Sprite Group classes.
    
        self.some_group = pygame.sprite.Group()
        
        # All sprites are stored here.
        self.all_sprites_list = pygame.sprite.Group()
        
        
        # --- Add units before game begines to test. 
        
        self.panel = Panel()
        self.panel.set_primary()
        self.title_sprites_list = TitleBar(self.panel)
        
        self.abberation = Abberation()
        
        self.panel.add(self.title_sprites_list)
        
        # Start game process that updates 64 times per second.
        t1 = Thread(target=self.start_engine, args=() )
        t1.start()
        threads.append(t1)
            
    #######################################################
    def _run_updates(self):
         
        events = pygame.event.get()
        self.panel.update(events)
        
        self.abberation.update()
        
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.exit()
    
    
    #######################################################
    def draw(self, surface):
        # make sure system doesn't blit all the nodes to itself first
        
        self.title_sprites_list.draw(surface)
        
        self.abberation.draw(surface)
        
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
            #self.Frameobj.one_frame_execute()
            clock.tick(64)
        
    
    
def get_engine():
    print "exiting"
    return engine
    
class close_button(Button):
    def __init__(self, panel):
        super(close_button, self).__init__(panel)
        
        self.theme = create_button_theme(pygame.image.load("data/themes/default/titlebar/close.png").convert())

        self.rect = self.image.get_rect()
        self.rect.right = 915 - 5
        
        self.clicked(get_engine().exit, ())
        
class iconify_button(Button):
    def __init__(self, panel):
        super(iconify_button, self).__init__(panel)
        
        self.theme = create_button_theme(pygame.image.load("data/themes/default/titlebar/iconify.png").convert())
        
        self.rect = self.image.get_rect()
        self.rect.right = 915 - 5 - 15
        
        self.clicked(self.iconify, ())
        
    def iconify(self):
        pygame.display.iconify()

class title_bar(Button):
    def __init__(self, panel):
        super(title_bar, self).__init__(panel)
        
        self.theme = create_button_theme(pygame.image.load("data/themes/default/titlebar/title_bar.png").convert())
        
        self.rect = self.image.get_rect()
        

class TitleBar(ButtonGroup):
    def __init__(self, panel):
        super(TitleBar, self).__init__()
        self.title_bar = title_bar(panel)
        
        self.add(iconify_button(panel))
        self.add(close_button(panel))
    def draw(self, surface):

        surface.blit(self.title_bar.image, (0, 0))
        super(TitleBar, self).draw(surface)
        
        
        
        
    
