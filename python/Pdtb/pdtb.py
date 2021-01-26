"""
    VERSION: alpha 0.3a (Flying Virus)
    
    Authors: Anantha Krishna R.
"""
import discoverer
import period
import group
import group_color
import series
import block

from periodictable import elements
import pygame
from pygame.locals import *

from widgets.Panel import PanelLayered 
from widgets.Button import Button, ButtonGroup, create_button_theme
from widgets.Text import TextLine
from widgets.ToolTip import ToolTip
from widgets.Window import AbstractWindow
import widgets

def hexa_to_rgb(hexa):
    return tuple(int(hexa.lstrip('#')[i:i+2], 16) for i in (0, 2 ,4))

class ElementButton(Button):
    layer = -5
    def __init__(self, el):
        super(ElementButton, self).__init__()
        
        self.element = el
        
        self.text = TextLine(size=18)
        
        self.init()
        
    def init(self):
        PanelLayered.get_primary().change_layer(self, self.layer)
        PanelLayered.get_primary().move_to_back(self)
        
        el = self.element
        
        # Spacing.
        sp = 0
        left = 0
        top = 55
        
        surf = pygame.Surface((38+10,45+10)).convert_alpha()
        surf.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
        surf_rect = surf.get_rect()
        
        box = pygame.Surface((38,45))
        
        g_color = hexa_to_rgb(el.group_color)
        box.fill(g_color)
        box_rect = box.get_rect()
        box_rect.center = surf_rect.width/2, surf_rect.height/2
        
        self.rect = surf.get_rect()
        
        g = self.element.group
        p = self.element.period
        g_fac = p_fac = 0
        
        if not g and not p:
            g_fac = 1

        elif not g:
            p_fac = 2.5
            g_fac = 3 + (el.number - 57) % 16

        self.rect.center = ((g+g_fac)*(self.rect.width+sp)+left, (p+p_fac)*(self.rect.height+sp)+top)

        self.text.text=str(el.symbol)
        self.text.rect.center = box_rect.width/2, (box_rect.height-5)/2
        self.text.draw(box)
        
        self.text.text=str(el.number)
        self.text.font_size = 16
        self.text.rect.center = box_rect.width/2, (box_rect.height+22)/2
        self.text.draw(box)
        
        surf.blit(box, (box_rect.x, box_rect.y))
        self.image = surf.copy()
        self.theme = create_button_theme(self.image)
        
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))    
    
class Pdtb(ButtonGroup):
    def __init__(self, engineobj):
        
        
        ButtonGroup.__init__(self)
        
        
    def update(self):
        self.AbstractWindow.update()
        
    def load(self, loading=None):
        # Setting loading surfaces for this load.
        
        panel = PanelLayered()
        panel.set_primary()
        
        if loading:
            #loading.add_text(0, "Loading all elements...")
            loading.add_text(1, "Loading surfaces...")
            loading.change_state(1)
            
        self.ToolTip = ToolTip()
        self.ToolTip.add_tip("transparant", gen_tip_surface())
        
        self.ToolTip.change_tip("transparant")
        self.ToolTip.rect.center = 7*(38+10), 2.5*(45+10)
        
        #loading.change_state(1)
        
        for el in elements: 
            eb = ElementButton(el)
            self.add(eb)
            
            self.ToolTip.add_tip(el, gen_tip_surface(el))
            
            eb.clicked(self.dialogue_box, (el,))
            eb.hover(self.ToolTip.change_tip, (el,))
            eb.leave(self.ToolTip.disengage, ())
        
        if loading:
            loading.done()
        
        self.AbstractWindow = AbstractWindow()
        #self.AbstractWindow.focus = 3
        
    def handle_event(self, event):
        PanelLayered.get_primary().update(event)
        
    def draw(self, surface):
        """Draws all the elements."""
        
        sprites = self.sprites()
        
        for spr in sprites:
            spr.draw(surface)
        
        self.ToolTip.draw(surface)
        self.AbstractWindow.draw(surface)
    ####################################################################
    # callbacks.
    def dialogue_box(self, el):# clicked.
        # TODO: Write the dialogue box script here.
        self.AbstractWindow.init(el)
        
def gen_tip_surface(el = None):
    # TODO: Include symbolic_color.
    
    surface = pygame.Surface((400,200)).convert_alpha()
    surface.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
    surface_rect = surface.get_rect()
    
    if el == None: return surface
        
    box = pygame.Surface((63, 75)).convert_alpha()
    box.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
    box_rect = box.get_rect()
    box_rect.centery = surface_rect.height/2 -20
    box_rect.right = (surface_rect.width/2)-0

#    box.fill(el.symbolic_color)
    g_color = hexa_to_rgb(el.group_color)
    box.fill(g_color)
    
    text = TextLine(size=30, text=el.symbol)
    
    # Symbol.
    text.bold = 1
    text.rect.center = box_rect.width/2, (box_rect.height+22)/2
    text.draw(box)
    text.bold = 0
    
    # Number.
    text.text=str(el.number)
    text.font_size = 22
    text.rect.center = box_rect.width/2, (box_rect.height-17)/2
    text.draw(box)
        
    surface.blit(box, (box_rect.x, box_rect.y))
    
    writing_box = pygame.Surface((200, 75)).convert_alpha()
    writing_box.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)
    writing_box_rect = writing_box.get_rect()
    writing_box_rect.left = box_rect.x + box_rect.width
    writing_box_rect.centery = box_rect.centery
    
    # Name.
    text.bold = 1
    text.font_size = 27
    text.text=str(el.name.title())
    text.rect.left = 15
    text.rect.centery = (writing_box_rect.height-20)/2
    text.draw(writing_box)
    text.bold = 0
    
    # Series.
    text.text=str(el.series)
    text.font_size = 23
    text.rect.left = 15
    text.rect.centery = (writing_box_rect.height+23)/2
    text.draw(writing_box)
    
    
    surface.blit(writing_box, (writing_box_rect.x, writing_box_rect.y))
    
    return surface
