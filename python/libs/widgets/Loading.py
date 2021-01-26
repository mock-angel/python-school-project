# Loading.py
"""
Blits a text or image to the loading screen at the center(can be changed on the fly
by altering the self.center values.)

#Uses the lock method of handling abortion of drawing during  

Usage requirements.
    pygame window to be initialised and display screen to be set.
"""
# Recently removed the lock attribute of Loading.

import pygame
from pygame.locals import *

from Text import TextLine

class Loading():
    def __init__(self):
        self.surface_dict = dict()
        self.key = None
        
        self.text = TextLine()
        
        self.image = pygame.Surface((0,0))
        self.rect = self.image.get_rect()
        
        screen_rect = pygame.display.get_surface().get_rect()
        self.center = screen_rect.width/2, screen_rect.height/2
        
        #self.lock = False
        self.loading = True
        
    def add_surface(self, key, surface):
        """Standard way to relate the state to a surface."""
        self.surface_dict[key] = surface
    
    def add_text(self, state, text, color=Color("White"), font_size=35, bold=1):
        self.text.text = text
        self.bold = bold
        self.text.color = color
        self.text.font_size = font_size
        
        self.surface_dict[state] = self.text.image.copy()
        
    def change_state(self, key):
        self.key = key
        #self.lock = True
        image = self.surface_dict[key]
        rect = image.get_rect()
        rect.center = self.center
        
        self.image = image
        self.rect = rect
        pygame.display.get_surface().blit(self.image, (self.rect.x, self.rect.y))
        
        pygame.display.update()#dirty_rects)
        #self.lock = False
    
    def draw(self, surface):
        #if self.lock:
        #    return
        # This may not be necessary for loading on multiple threads.
        surface.blit(self.image, (self.rect.x, self.rect.y))
    
    def done(self):
        self.loading = False
