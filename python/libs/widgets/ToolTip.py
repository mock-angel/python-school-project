# ToolTip.py
import pygame
from pygame.locals import *

class ToolTip():
    def __init__(self):
        self.tip_dict = dict()
        self.rect = Rect(0, 0, 0, 0)
        self.engaged = False
        self.tick = 0
        self.sticky_frames = 10
    def add_tip(self, key, surface_value):
        self.tip_dict[key] = surface_value
        
    def add_tipdict(self, tooltip_dict):
        for key in tooltip_dict:
            self.tip_dict[key] = tooltip_dict[key]
        
    def change_tip(self, key):
        self.engaged = True
        self.tick = 0
        self.set_surface(self.tip_dict[key].copy())
        
    def set_surface(self, surface):
        
        prev_rect = self.rect.copy()
        rect = surface.get_rect()
        
        rect.center = prev_rect.center
        
        self.rect = rect
        self.image = surface
        
        
    def draw(self, surface):
        if not self.engaged:
            self.tick += 1
            if self.tick >= self.sticky_frames:
                self.change_tip("transparant")
                self.tick = 0
                
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
    def disengage(self):
        self.engaged = False
