# Button.py v1.1.

"""
Button 
    Usage:-
        button = Button()
    
    Can be reused to create button gadgets by inheriting Button class.
    
DragButton:
    Usage:-
        button = DragButton()
    
TextButton:
    Usage:
        button = TextButton()


"""

import pygame

from pygame.locals import *
from random import random
from Panel import Panel
from Mouse import Mouse
from Text import TextLine

def create_button_theme(default = None, hover = None, held = None, disabled = None):
    """create_button_theme() - theme Standard method of creating simple button theme."""
    
    hover = default if not hover else hover
    held = hover if not held else held
    
    dict_ = {
        "default" : default,
        "clicked" : hover,
        "rclicked" : hover,
        
        "enter" : hover,
        "hover" : hover,
        "leave" : default,
        
        "pressed" : held,
        "released" : hover,
        
        "label" : default,
    }
    if disabled: dict_["disabled"] = disabled
    
    return dict_
    
class Button(pygame.sprite.Sprite):
    def __init__(self, panel = None):
        
        super(Button, self).__init__()
        
        self.disabled = False
        self.keyboard = False
        
        if panel == None:
            
            panel = Panel.get_primary()
            
        # TODO: change alignment scheme to -1, 0, +1.
        self.align = "center"#center, right, bottom, top
        self.key = "default"
        self.rect = Rect(0, 0, 0, 0)
        self.label = ""
        self.theme = create_button_theme(pygame.Surface((0,0)))
        self.default_theme = create_button_theme(pygame.Surface((0, 0)))
        
        self.mouse_xy = 0, 0
        
        self.clicked_origin = False
            
        self.ready = False
        self.__state = "idle"
        self.clicked_start = False
        
        self.drag = False
        
        self.focus = 1
        
        self.id = str(int(random() * (10**5)))
        
        cursor_def = pygame.cursors.arrow
        cursor_hov = pygame.cursors.tri_left
        
        self.cursors = {
            "default" : cursor_def,

            "enter" : cursor_hov,
            "hover" : cursor_hov,
            "leave" : cursor_def,
            
            "pressed" : cursor_hov,
            "released" : cursor_hov,
            
            "disabled" : cursor_def
        }
        
        self.panel = panel
        self.panel.add(self)
        
        self.init_button()
        self.ready = True
    @property
    def theme(self):
        return self.theme_
        
    @theme.setter
    def theme(self, theme):
        """To Change theme."""
        
        self.theme_ = theme
        
        self.image = self.theme_[self.key]
        
        if self.align=="center":
            rect = self.image.get_rect()
            rect.center = self.rect.center
            
        if self.align=="xy":
            rect = self.image.get_rect()
            rect.x, rect.y = self.rect.x, self.rect.y
        self.rect = rect
        
    def null(self):
        """Dummy method, does nothing."""
        pass
    
    def init_button(self):
        """Sets default callback to the dummy 'null' method."""
        
        callback = self.null
        params = ()
        
        self.clicked_callback = callback
        self.clicked_params = params
        
        self.lift_callback = callback
        self.lift_params = params
        
        self.right_clicked_callback = callback
        self.right_clicked_params = params
        
        self.right_released_callback = callback
        self.right_released_params = params
        
        self.enter_callback = callback
        self.enter_params = params
        
        self.hover_callback = callback
        self.hover_params = params
        
        self.leave_callback = callback
        self.leave_params = params
        
        self.pressed_callback = callback
        self.pressed_params = params
        
        self.released_callback = callback
        self.released_params = params
        
    ##########################################
    # Sets the callback for particular events.
    def clicked(self, callback, params = ()):
        self.clicked_callback = callback
        self.clicked_params = params
    
    def lift(self, callback, params = ()):
        self.lift_callback = callback
        self.lift_params = params
    
    def right_clicked(self, callback, params = ()):
        self.right_clicked_callback = callback
        self.right_clicked_params = params
    
    def right_released(self, callback, params = ()):
        self.right_clicked_callback = callback
        self.right_clicked_params = params
    
    def enter(self, callback, params = ()):
        self.enter_callback = callback
        self.enter_params = params
        
    def hover(self, callback, params = ()):
        self.hover_callback = callback
        self.hover_params = params
    
    def leave(self, callback, params = ()):
        self.leave_callback = callback
        self.leave_params = params
        
    def pressed(self, callback, params = ()):
        self.pressed_callback = callback
        self.pressed_params = params
    
    def released(self, callback, params = ()):
        self.released_callback = callback
        self.released_params = params
    
    #################################################
    # Calls the callback when events are encountered.
    def on_event(self, event, button=1, pyevent=None):
        """on_event(event, ...) Called by Panel object."""
        
        self.event = pyevent
        
        if self.disabled: self.__state = "disabled"
            
        if self.__state == "disabled": return
            
        self.mouse_pressed_number = button
        if event == "start_clicked":
            
            if self.clicked_origin and self.__state == "pressed": return
            
            self.clicked_origin = True
            self.__state = "pressed"
            self.number = button
            
            if self.mouse_pressed_number == 3:
                self.on_right_clicked()
                self.number = 3
                self.clicked_origin = False
                
            else:
                self.on_clicked()
                self.number = 1
        
        elif event == "pressed"  and self.mouse_pressed_number==1: # left button test.
            self.__state = event
            self.on_pressed()
            
        elif event == "released" and (self.__state == "pressed"):
            if self.number == 1:
                self.on_released()
            elif self.number == 3:
                self.on_right_released()
            
            self.__state = "hover"
            
            if self.clicked_origin:
                self.clicked_origin = False
                
                if self.mouse_pressed_number == 1:
                    self.on_lift()
            
        elif event == "hover":
            if self.__state == "idle":
                self.on_enter()
                self.__state = "hover"
        
            elif self.__state == "pressed" and self.mouse_pressed_number==1:
                self.on_pressed()
                
            else:
                self.mouse_xy = pyevent.pos
                self.on_hover()
                
        elif event == "idle":
            if self.__state == "hover":
                 
                self.__state = "idle"
                self.on_leave()
            
            elif self.__state == "pressed":
                 
                self.__state = "idle"
                self.on_leave()
    
    def on_key_event(self, pyevent, key):
        """on_key_event() - Derive this to capture all keyboard events."""
        
        pass
        
    def on_clicked(self):
        self.key = "clicked"
        print "on_clicked"
        self.image = self.theme_["clicked"]
        
        self.clicked_callback(*self.clicked_params)
    
    def on_lift(self):
        self.key = "hover"
        pygame.mouse.set_cursor(*self.cursors[self.key])
        self.image = self.theme_["hover"]
        print "on_lift"
        self.lift_callback(*self.lift_params)
        
    def on_right_clicked(self):

        self.right_clicked_callback(*self.right_clicked_params)
        print self.key
        try:
            self.theme_["rclicked"]
            
        except KeyError:
            self.image = self.theme_["clicked"]
    
    def on_right_released(self):

        self.right_released_callback(*self.right_released_params)
        
        try:
            self.theme_["rreleased"]
            
        except KeyError:
            self.image = self.theme_["clicked"]
        
    def on_enter(self):
        self.key = "enter"
        pygame.mouse.set_cursor(*self.cursors[self.key])
        self.image = self.theme_["enter"]

        self.enter_callback(*self.enter_params)
        print "on_enter"
    def on_hover(self):
        self.key = "hover"
        pygame.mouse.set_cursor(*self.cursors[self.key])
        self.image = self.theme_["hover"]
    
        self.hover_callback(*self.hover_params)
        print "on_hover"
    def on_leave(self):
        self.key = "leave"
        pygame.mouse.set_cursor(*self.cursors[self.key])
        self.image = self.theme_["leave"]
        
        self.leave_callback(*self.leave_params)
        print "on_leave"
    def on_pressed(self):
        self.key = "pressed"
        pygame.mouse.set_cursor(*self.cursors[self.key])
        self.image = self.theme_["pressed"]
        
        self.pressed_callback(*self.pressed_params)
        print "on_pressed"
    def on_released(self):
        self.key = "released"
        pygame.mouse.set_cursor(*self.cursors[self.key])
        self.image = self.theme_["released"]
    
        self.released_callback(*self.released_params)
        print "on_released"
    def move(self, x, y):
        self.rect = self.rect.move(x, y)
    
    def disable(self):
        
        self.disabled = True
        self.__state = "disabled"
        
        try:
            self.key = "disabled"
            self.on_event("disabled")
            
            self.theme_["disabled"]

            self.image = self.theme_["disabled"]


            pygame.mouse.set_cursor(*self.cursors[self.key])

        except KeyError:
            pass
            
    def enable(self):
        
        self.image = self.theme_["default"]
        
        self.disabled = False
        self.__state = "idle"
        
    def draw(self, surface):
        # New feature.
        
        surface.blit(self.image, (self.rect.x, self.rect.y))
    
    def is_pressed(self):
        return self.__state == "pressed"

#Focuses on appearances.
class DragButton(Button):
    """DragButton - Make a button that you can drag and move, but doesn't disturb
    the actual properties of the Button Class."""
    def __init__(self, panel = None):
        Button.__init__(self)
        
        self.drag = False
        self.mouse = Mouse()
        self.held_cursor = pygame.image.load("../libs/widgets/cursor_held.png")
        
        self.clicked(self.start_drag, (self,))
        self.hover(self.end_drag, ())
        self.released(self.end_drag, ())
        
        self.dragcallback = self.null
        self.dragparam = ()
        self.drag_cords = (0, 0)
        
    def on_clicked(self):

        Button.on_clicked(self)
        self.start_drag(self)
        
    def on_hover(self):
        if self.drag:
            self.__state = "pressed"
            self.on_pressed
            return
            
        Button.on_hover(self)
        self.end_drag()
    
    def on_released(self):
        
        Button.on_released(self)
        self.end_drag()
    
    def start_drag(self, button):

        self.drag = True
        
        # Makes cursor invisible.
        pygame.mouse.set_visible(0)
        
        self.mouse.update()
        self.prev_x, self.prev_y = self.mouse.get_pos()
        
    def end_drag(self):
        # End drag is repeatedly called when its hovering and not dragging.
        
        self.drag = False
        
        # Changes cursor back to visible.
        pygame.mouse.set_visible(1)
    
    def dragging(self, callback, param):
        self.dragcallback = callback
        self.dragparam = param
    def on_drag(self):
        """Operations during drag."""
        
        self.dragcallback(*self.dragparam)
        
    def update(self):
        if not self.drag: return
        
        self.mouse.update()
        x, y = self.mouse.get_pos()
        
        self.drag_cords = (x - self.prev_x, y - self.prev_y)
        self.move(x - self.prev_x, y - self.prev_y)
        self.prev_x, self.prev_y = x, y
        
        self.on_drag()
    def draw(self, surface):
     
        Button.draw(self, surface)
        
        # Draws cursor
        if self.drag == True:
            surface.blit(self.held_cursor, (self.mouse.rect.x, self.mouse.rect.y))
    def change_layer(self, layer):
        Panel.get_primary().change_layer(self, layer)

class TextButton(Button):
    '''TextButton - A button containing text. The text part is also a theme and
     can be set to react to mouse events.
    
    requires to set drect(i.e. the diamensions of the button with modified center) 
    and call set_theme.'''
    
    def __init__(self, panel = None):
        
        Button.__init__(self)
        
        text_theme = create_button_theme("default", "hover", "press")
        
        color_theme = create_button_theme((255,255,255))
        
        self.text = TextLine(size=20, text="world")
            
        
        self.image = pygame.Surface((0,0)).convert()
        self.rect_ = Rect((0,0,0,0))
        self.text
#        self.set_theme(text_theme, color_theme)
        self.ready = True
        
    @property
    def drect(self):
        return self.rect_
    @drect.setter
    def drect(self, rect):
        
        self.theme = self.regenerate_theme(rect)
        self.image = self.theme[self.key]
        self.rect = rect
        
    def set_theme(self, text_theme, color_theme):
        self.text_theme = text_theme
        self.color_theme = color_theme
        
        self.theme = self.regenerate_theme(self.rect)
    
    def regenerate_theme(self, rect):
        
        gen_dict = dict()

        for key in self.color_theme:
            surf = pygame.Surface((rect.width, rect.height)).convert()
            surf.fill(self.color_theme[key])

            gen_dict[key] = surf
            
        for key in self.text_theme:
            self.text.text = self.text_theme[key]
            rect = gen_dict[key].get_rect()
            
            center = rect.width/2, rect.height/2
            
            self.text.rect.center = center
            self.text.draw(gen_dict[key])
        return gen_dict
     
    def draw(self, surface):
        Button.draw(self, surface)

# ButtonGroup        
class ButtonGroup(pygame.sprite.Group):
    """ButtonGroup - Container class for Button Sprites."""
    
    def __init__(self):
        super(ButtonGroup, self).__init__()
    # TODO: Complete th9is section please
    def clicked(self, callback, params = ()):
        sprite_list = self.sprites()
        for sprite in sprite_list:
            self.clicked_callback = callback
            self.clicked_params = params
        
    def enter(self, callback, params = ()):
        sprite_list = self.sprites()
        for sprite in sprite_list:
            self.enter_callback = callback
            self.enter_params = params
        
    def hover(self, callback, params = ()):
        sprite_list = self.sprites()
        for sprite in sprite_list:
            self.hover_callback = callback
            self.hover_params = params
            sprite.hover(callback, params)
            
    def leave(self, callback, params = ()):
        sprite_list = self.sprites()
        for sprite in sprite_list:
            self.leave_callback = callback
            self.clicked_params = params
            
    def pressed(self, callback, params = ()):
        sprite_list = self.sprites()
        for sprite in sprite_list:
            self.pressed_callback = callback
            self.pressed_params = params
            
    def released(self, callback, params = ()):
        sprite_list = self.sprites()
        for sprite in sprite_list:
            self.released_callback = callback
            self.released_params = params
    def draw(self, surface):    

        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            if spr.ready:
                self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []
    
    def disable(self):
        sprite_list = self.sprites()
        for sprite in sprite_list:
            sprite.disable()
    def change_layer(self, layer):
        sprites = self.sprites()
        panel = Panel.get_primary()
        for spr in sprites:
            panel.change_layer(spr, layer)
            
    def move(self, x, y):
        sprites = self.sprites()
        for spr in sprites:
            
            spr.rect = spr.rect.move(x, y)
