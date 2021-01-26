# Text.py
"""
AbstractTextLine : A variant of TextLIne built to be Abstract.
TextLine : The most basic method of displaying text.
"""

import pygame
from pygame.locals import *
import os

class AbstractTextLine(object):
    # Manages drawing and caching a single line of text.
    # Use as abstract class.
    
    def __init__(self, font_family="", size=22, text=""):
        
        self._aa = True 
        
        # Text related vars:
        self._aa = antialias = True
        self._text_color = text_color = Color("white")
        self._font_family = font_family
        self._font_size = font_size = size
        
        self._text = text
        
        
        self._font_family = pygame.font.match_font(font_family)
        
        try:
            
            self.font_object = pygame.font.Font(self._font_family, size)
        except IOError:
            self._font_family = pygame.font.match_font(font_family)
            self.font_object = pygame.font.SysFont(self._font_family, size)
            
        
        self.text_surface = pygame.Surface((1, 1))
        self.text_rect = self.text_surface.get_rect()
        self.cropped_rect = self.text_rect.copy()
        
        self._render()
        
    # Getter.
    ###############################################################
    @property
    def aa(self): return self._aa
    
    @property
    def text_color(self): return self._text_color
    
    @property
    def font_family(self): return self._font_family
    
    @property
    def font_size(self): return self._font_size
        
    @property
    def text(self): return self._text
    
    @property
    def bold(self): return self.font_object.get_bold()
    
    def set_text(self, text):
        self.text = text
    
    def get_size(self, text):
        return self.font_object.size(text)
        
    def get_text_rects(self):
        return self.text_rect, self.cropped_rect
    # Setter.
    ###############################################################
    @aa.setter
    def aa(self, aa):
        
        self._aa = aa
        self.dirty = True
        self._render()
    @text_color.setter
    def text_color(self, color_rgb):
        
        self._text_color = color_rgb
        self.dirty = True
        
        self._render()
        
    @font_family.setter
    def font_family(self, font_family):
        """Temporarirly sets the font family."""
        
        self._font_family = font_family
        self.remake_font_object()
        
        self.dirty = True
        self._render()
    @font_size.setter
    def font_size(self, font_size):
        
        self._font_size = font_size
        self.remake_font_object()
        self.dirty = True
        
        self._render()
        
    @text.setter
    def text(self, text):
        self._text = text
        self.dirty = True
        self._render()
        
        
    @bold.setter
    def bold(self, boolean):
        
        self.font_object.set_bold(boolean)
        self.dirty = True
        self._render()
    ###############################################################
    def remake_font_object(self):
    
        try:
            
            self.font_object = pygame.font.Font(self._font_family, self._font_size)
        except IOError:
            self._font_family = pygame.font.match_font(self._font_family)
            self.font_object = pygame.font.SysFont(self._font_family, self._font_size)
    
    def _render(self):
        # render cache.
        """no AA = automatic transparent. With AA you need to set the color key too"""
        
        self.dirty = False        
        text_surface = self.font_object.render(self._text, self._aa, self._text_color)            
        
        text_rect = text_surface.get_rect()
        cropped_rect = text_rect.copy()
        
        prev_text_rect = self.text_rect
        text_rect.x, text_rect.y = self.text_rect.x, self.text_rect.y
        self.text_rect = text_rect
        self.cropped_rect = cropped_rect
        self.text_surface = text_surface
    
    # Used for drawing the final render. Uses cache..
    def draw(self, surface):
        
        if self.dirty: self._render()
        surface.blit(self.text_surface, self.text_rect, self.cropped_rect)
        
#TODO: Need revision.
class TextLine(object):
    # Manages drawing and caching a single line of text
    # You can make font size, .color_fg etc be properties so they *automatically* 
    # toggle dirty bool.
    
    def __init__(self, font=None, size=16, text=""):        
        self.font_name = font
        self.color_fg = Color("white")
        self.color_bg = Color("gray20")

        self._aa = True 
        self._text = text                
        try:
            self.font_object = pygame.font.Font(font, size)
            
        except IOError:
            self.font_object = pygame.font.SysFont(font, size)
        self.screen = pygame.display.get_surface()

        self.dirty = True
        self.image = None
        self._render()

    def _render(self):
        # render for cache.
        """no AA = automatic transparent. With AA you need to set the color key too"""
        self.dirty = False        
        self.image = self.font_object.render(self._text, self.aa, self.color_fg)            
        self.rect = self.image.get_rect()

    def draw(self, surface):
        # Call this do draw, always prefers to use cache.
        if self.dirty or (self.image is None): self._render()
        surface.blit(self.image, self.rect)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        
        self._text = text
        self.dirty = True
        self._render()   

    @property
    def font_size(self):
        return self.font_object
     
    @font_size.setter
    def font_size(self, size):
        
        try:
            
            self.font_object = pygame.font.Font(self.font_name, size)
        except IOError:
            self.font_object = pygame.font.SysFont(self.font_name, size)
        self.dirty = True
        self._render()
    @property
    def aa(self): return self._aa

    @aa.setter
    def aa(self, aa):
        self.dirty = True
        self._aa = aa
    
    @property
    def text_color(self):
        return self.color_fg
        
    @text_color.setter
    def text_color(self, color):
        
        self.color_fg = color
        self.dirty = True
        self._render()
        
    @property
    def bold(self):
        return self.font_object.get_bold()
    
    @bold.setter
    def bold(self, boolean):
        
        self.font_object.set_bold(boolean)
        self.dirty = True
        self._render()
    
    def get_size(self, text):
        return self.font_object.size(text)
    
    def set_text(self, text):
        self.text = text
    
class TextWall(object):# Dead
    # Manages multiple lines of text / paragraphs.
    def __init__(self, font=None, size=16):
        self.font_object = font
        self.font_size = size        
        self.offset = Rect(20,20,1,1) # offset of whole wall

        self.screen = pygame.display.get_surface()
        self.dirty = True
        self.text_lines = []
        self._text_paragraph = "Empty\nText"
        self._render()
        print self._text_paragraph
        
    def _render(self):
        # render list 
        self.dirty = False

        self.text_lines = [ TextLine(self.font_object, self.font_size, line) for line in self._text_paragraph ]        

        # offset whole paragraph
        self.text_lines[0].rect.top = self.offset.top

        # offset the height of each line
        prev = Rect(0,0,0,0)        
        for t in self.text_lines:
            t.rect.top += prev.bottom
            t.rect.left = self.offset.left
            prev = t.rect

    def parse_text(self, text):
        # parse raw text to something usable
        self._text_paragraph = text.split("\n")
        self._render()

    def draw(self):
        # draw with cached surfaces    
        if self.dirty: self._render()
        for text in self.text_lines: text.draw()
    
    def get_surfaces(self):
        return self.text_lines
    
    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        self.dirty = True
        self._font_size = size

    @property
    def text(self):
        return self._text_paragraph

    @text.setter
    def text(self, text_paragraph):
        self.dirty = True
        self.parse_text(text_paragraph)
        self._render()
