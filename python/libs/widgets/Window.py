# Window.py
"""
Abstract window and popup not built for animation. The surface is being
prepared and is blitted to the screen.

"""
from Panel import Panel
from widgets.Button import DragButton, Button,create_button_theme,ButtonGroup,TextButton
from widgets.Mouse import Mouse
import pygame
from Panel import Panel
from Colors import *

from Text import TextLine
from pygame.locals import *

class DynamicMenu(): # Pdtb.
    def __init__(self, width, height):
        self.surface_dict = dict()
        self.key = 0
        self.text = TextLine()
        
        self.key_i = 0
        self.button_group = ButtonGroup()
        self.menu_height = 40
        
        
        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect()
        self.default = self.image.copy()
        
        self.fake_button = Button()
        self.fake_button.theme = create_button_theme(pygame.Surface((1, 1)).convert())
        self.fake_button.rect = self.rect.copy()
        
    @property
    def drect(self):

        return self.rect
    
    @drect.setter
    def drect(self, rect):

        self.rect = rect.copy()
        
        y = self._rect.y - self.menu_height
        for b in self.button_group:
            brect = b.rect.copy()
            
            brect.x = b.relative_offsetx + self.rect.x
            brect.y = y

            b.rect = brect
            
    def add_surface(self, button, surface):
        """Standard way to relate the state to a surface."""
        
        self.button_group.add(button)
        self.button_group.change_layer(0)
        
        button.clicked(self.change_state, (self.key_i,))
        button.index = self.key_i
        self.surface_dict[self.key_i] = surface
        
        # Now do rect correcton.
        max_width = self.rect.width
        max_height = self.rect.height
        
        b_width = max_width/(self.key_i+1)
        
        for b in self.button_group:

            b_rect = b.rect.copy()
            b_rect.width = b_width
            b_rect.height = self.menu_height
            b_rect.x = b_width * b.index
            b.relative_offsetx = b_width * b.index
            
            b.drect = b_rect

        self.key_i+=1
        
    def change_state(self, key):
        """Changes label state."""
        self.key = key

        img = self.surface_dict[key]
        rect = img.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        
        image = self.default.copy()
        image.blit(img, (0,0))
        self.image = image
    
    def draw(self, surface):
        
        surface.blit(self.image, (self.rect.x, self.rect.y))
        self.button_group.draw(surface)
        
    def reconfigure_button_pos(self):
        rect = self.rect.copy()
        
        y = self.rect.y - self.menu_height
        for b in self.button_group:
            brect = b.rect.copy()
            
            brect.x = b.relative_offsetx + rect.x
            brect.y = y
            
            b.rect = brect
        self.fake_button.rect.x, self.fake_button.rect.y = rect.x, rect.y
        
class AbstractWindow(pygame.sprite.Sprite):
    def __init__(self):
        """Abstract to popup, and other normal inline windows."""
        super(AbstractWindow, self).__init__()
        
        self.drag = False
        self.active = False
        rect = pygame.display.get_surface().get_rect()
        self.start_pos = rect.width/2, rect.height/2
        
    def init(self, element):
        self.destroy()
        el = element
        self.mouse = Mouse()
        
        # The top of the window that you can drag.
        self.button = DragButton()
        
        self.close_button = close_button()
        self.close_button.clicked(self.destroy, ())
        
        surf = pygame.Surface((300,30))
        surf.fill((62,61,57))
        
        text = TextLine(text = el.name.title(), size = 30)
        text.rect.center = surf.get_rect().width/2, surf.get_rect().height/2
        text.draw(surf)
        
        self.held_cursor = pygame.image.load("../libs/widgets/cursor_held.png")
        
        self.button.theme = create_button_theme(surf)
        self.button.change_layer(0)
        self.button.layer = 0
        
        self.button.rect.center = self.start_pos
        
        self.dynamic_menu = DynamicMenu(300,200)
        # add all the menus
        surface = pygame.Surface((100,100))
        
        default_color = hexa_to_rgb(element.group_color)
        hover_color = adjust_color(default_color[0] - 20,default_color[1] - 20,default_color[2] - 20)
        
        hover_color = adjust_color(default_color[0] + 20,default_color[1] + 20,default_color[2] + 20)
        
        surface.fill(hexa_to_rgb(element.group_color))
        
        # Add. Menu buttons General, Physical and Chemical to window.
        gen = general_menu_button = TextButton()
        tt = create_button_theme("General")
        ct = create_button_theme(default_color, hover = hover_color)
        
        general_menu_button.set_theme(tt, ct)
        
        phy = phsical_menu_button = TextButton()
        tt = create_button_theme("Physical")
        ct = create_button_theme(default_color, hover = hover_color)
        phsical_menu_button.set_theme(tt, ct)
        
        chem = chemical_menu_button = TextButton()
        tt = create_button_theme("Chemical")
        
        ct = create_button_theme(default_color, hover = hover_color)
        chemical_menu_button.set_theme(tt, ct)
        
        
        self.dynamic_menu.add_surface(gen, create_general_info(el, (300,200)))
        self.dynamic_menu.add_surface(phy, create_physical_info(el, (300,200)))
        self.dynamic_menu.add_surface(chem, create_chemical_info(el, (300,200) ))
        self.dynamic_menu.change_state(0)
        self.button.dragging(self.configure_positions, (self.button,))
        self.configure_positions(self.button)
        self.active = True
        
    def update(self):
        if self.active:
            self.button.update()
            
    def draw(self, surface):
        """Window drawing sequence."""
        if self.active:
            self.button.draw(surface)
            self.dynamic_menu.draw(surface)
            self.close_button.draw(surface)
            
    def configure_positions(self, button):
        
        rect = button.rect

        rrect = self.dynamic_menu.rect.copy()
        self.dynamic_menu.drect.x = rect.x
        self.dynamic_menu.drect.y = rect.y +rect.height +self.dynamic_menu.menu_height
        
        self.close_button.rect.x = rect.x +rect.width - self.close_button.rect.width
        self.close_button.rect.centery = rect.y + rect.height/2
        self.dynamic_menu.reconfigure_button_pos()
        
    def destroy(self):
        """A kill switch that terminates the contents of the window and resets all
        necessary surface variables."""
        if self.active:

            for spr in self.dynamic_menu.button_group:
                spr.kill()
            
            self.dynamic_menu.fake_button.kill()
            self.active = False
            
            self.start_pos = (self.button.rect.x+self.button.rect.width/2, 
                                self.button.rect.y+self.button.rect.height/2)
                
    def replace(self, el):
        if self.active:

            for spr in self.dynamic_menu.button_group:
                spr.kill()
                
            print "killing"
            self.dynamic_menu.fake_button.kill()

            self.dynamic_menu.surface_dict = dict()
            self.close_button.kill()

            self.active = False
            
            # variation in v0.3b version.
            self.kill()
            
def create_general_info(el, size): # pdtb only.
    surf = pygame.Surface(size)
    surf.fill(hexa_to_rgb(el.group_color))
    
    spacing = 18
    
    text = TextLine(size = 20)
    text.text = "Series: "+ str(el.series)
    text.rect.x = spacing
    text.rect.y = 10
    text.draw(surf)
    
    
    text.text = "Group:  "+ str(el.group)
    text.rect.x = spacing
    text.rect.y = 10+14*1
    text.draw(surf)
    
    text.text = "Period:  "+ str(el.period)
    text.rect.x = spacing
    text.rect.y = 10+14*2
    text.draw(surf)
    
    
    text.text = "Block:  "+ str(el.block)
    text.rect.x = spacing
    text.rect.y = 10+14*3
    text.draw(surf)
    
    text.bold = 1
    text.text = "Missellaneous"
    text.rect.x = spacing
    text.rect.y = 10+14*5
    text.draw(surf)
    text.bold = 0
    
    text.text = "Symbolic color:  "+ str(el.group_color)
    text.rect.x = spacing
    text.rect.y = 10+14*6
    text.draw(surf)
    
    return surf
    
def create_physical_info( el, size): # pdtb only.
    surf = pygame.Surface(size)
    surf.fill(hexa_to_rgb(el.group_color))
    
    spacing = 18
    
    text = TextLine(size = 20)
    text.text = "Mass:  " + str(el.mass) + "" + str(el.mass_units)
    text.rect.x = spacing
    text.rect.y = 10
    text.draw(surf)
    
    text.text = "Density:  "+ str(el.density) + str(el.density_units)
    text.rect.x = spacing
    text.rect.y = 10+14*1
    text.draw(surf)
    
    text.text = "interatomic distance: "+ str(el.interatomic_distance)[0:10]+" "+ str(el.interatomic_distance_units)
    text.rect.x = spacing
    text.rect.y = 10+14*2
    text.draw(surf)
    
    text.text = "Block:  "+ str(el.block)
    text.rect.x = spacing
    text.rect.y = 10+14*3
    text.draw(surf)
    
    return surf
    
def create_chemical_info(el, size):    
    surf = pygame.Surface(size)
    surf.fill(hexa_to_rgb(el.group_color))
    
    text = TextLine()
    
    text.text = ""
    
    text.draw(surf)
    return surf
    
class WindowGadgetGroup(pygame.sprite.Group): 
    # Used only in pdtb.
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        pass
    def draw(self, surface):
        """Every sprite draw() method is invoked."""
        
        sprites = self.sprites()    
        for spr in sprites:
            spr.draw(surface)
            
class close_button(Button):# Pdtb.
    """Close for window."""
    def __init__(self):
        
        Button.__init__(self)
        
        dir_ = "data/themes/default/titlebar/"
        img_load = pygame.image.load
        self.theme = create_button_theme(img_load(dir_+"close.png").convert_alpha(),
        hover = img_load(dir_+"close_hover.png").convert_alpha())

        self.rect = self.image.get_rect()
        self.rect.right = pygame.display.get_surface().get_rect().width - 20
        
