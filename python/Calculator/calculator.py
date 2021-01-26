'''
    VERSION: v1.0 (Sagitta Chronos)
    
    Authors: Anantha Krishna R.
'''

"""
    Completion Date 5 Nov, 10:45PM.
"""
from math import *

from widgets.Clock import Clock
import pygame

from widgets.Text import TextLine
from widgets.TextBox import AutoScrollingTextBox
from widgets.TextField import TextFieldSingleLine, TextField
from widgets.Button import Button, ButtonGroup, create_button_theme
        
class calculator():
    def __init__(self, engineobj):
        self.g = engineobj
        
        self.init_buttons()
        self.result = 0
        
    def init_buttons(self):
        
        d_size = pygame.display.get_surface().get_size()
        
        self.push_button_group = ButtonGroup()
        
        img_load = pygame.image.load 
        dir_ = "data/"
        default_surf = img_load(dir_ + "default.png")
        hover_surf = img_load(dir_ + "hover.png")
        held_surf = img_load(dir_ + "held.png")
        
        text = TextLine()
        text.text_color = (45, 45, 45)
        
        size = default_surf.get_size()
        center = size[0]/2, size[1]/2
        
        def gen_button(i):
            button = Button()
            button.label = i
            
            text.text = str(i)
            text.rect.center = center
            
            surf_default = default_surf.copy()
            surf_hover = hover_surf.copy()
            surf_held = held_surf.copy()
            
            text.draw(surf_default)
            text.draw(surf_hover)
            text.draw(surf_held)
            
            button.released(self.input_char, (i,))
            
            button.theme = create_button_theme(surf_default, surf_hover, surf_held)
            return button
        
        # init numbers.
        for i in range(0, 10):
            button = gen_button(i)
            cx, cy = d_size[0]/2, d_size[1]/2
            
            if i == 0:
                cx, cy = d_size[0]/6 - size[0]/2 -5, 8*d_size[1]/9
                
            if i in (1, 2, 3):
                cx, cy = i*d_size[0]/6 - size[0]/2 -5, 7*d_size[1]/9
                
            if i in (4, 5, 6):
                cx, cy = (i - 3)*d_size[0]/6 - size[0]/2 -5, 6*d_size[1]/9
                
            if i in (7, 8, 9):
                cx, cy = (i - 6)*d_size[0]/6 - size[0]/2 -5, 5*d_size[1]/9
            
            button.rect.center = cx, cy
            
            self.push_button_group.add(button)
        
        # init symbols.
        symbols = ["/", "x", "-", "+", "%", "(", ")","X**2","X**(1/2)","=",'.',"C",'<-']
        for i in symbols:
            button = gen_button(i)
            
            x_off, y_off = 1, 1
            
            if i == '.': x_off, y_off = 2, 8
            if i == '%': x_off, y_off = 3, 8
            if i == '=': x_off, y_off = 5, 8
            if i == '+': x_off, y_off = 4, 8
            if i == '-': x_off, y_off = 4, 7
            if i == 'x': x_off, y_off = 4, 6
            if i == '(': x_off, y_off = 5, 6
            if i == ')': x_off, y_off = 6, 6
            if i == 'C': x_off, y_off = 6, 5
            if i == 'X**2': x_off, y_off = 5, 7
            if i == 'X**(1/2)': x_off, y_off = 6, 7 
            if i == 'C': x_off, y_off = 6, 5
            if i == '<-': x_off, y_off = 5, 5
            if i == '/': x_off, y_off = 4, 5
            
            cx, cy = x_off*d_size[0]/6 - size[0]/2 -5, y_off*d_size[1]/9
            
            button.rect.center = cx, cy
            
            self.push_button_group.add(button)
            
        rect = pygame.Rect((0, 0, 300, 100))
        rect.center = d_size[0]/2, 2*d_size[1]/10
        self.text_box = AutoScrollingTextBox(rect, font_name="Sans")
        self.text_field = TextFieldSingleLine(size=(300, 20))
        self.text_field.max_display_length = 45
        
        self.text_field.rect.center =  d_size[0]/2, 4*d_size[1]/10
        self.text_field.on_focus_gained()
        self.field_group = TextField()
        self.field_group.add(self.text_field)
        
        self.field_group.returned(self.evaluate_expression, ())
        
    def input_char(self, ch):
        ch = str(ch).lower()
        
        mods_int = pygame.key.get_mods()
        
        shift = mods_int & pygame.KMOD_SHIFT
        
        if shift: ch = self.text_field.convert_key(ch)
        
        if ch == "*": ch = 'x'
        if ch == 'c': self.text_field.stored_string = ''
        if ch == '=': 
            self.evaluate_expression()
            return
        if ch == 'x**2': 
            self.text_field.on_key_down(')', pygame.key.get_mods())
            self.text_field.on_key_down('*', pygame.key.get_mods())
            self.text_field.on_key_down('*', pygame.key.get_mods())
            self.text_field.on_key_down('2', pygame.key.get_mods())
            self.text_field.on_key_down(')', pygame.key.get_mods())
            self.text_field.stored_string = '((' + self.text_field.stored_string
            self.text_field.cursor_position += 4
            return
            
        if ch == 'x**(1/2)': 
            self.text_field.on_key_down(')', pygame.key.get_mods())
            self.text_field.on_key_down('*', pygame.key.get_mods())
            self.text_field.on_key_down('*', pygame.key.get_mods())
            self.text_field.on_key_down('0', pygame.key.get_mods())
            self.text_field.on_key_down('.', pygame.key.get_mods())
            self.text_field.on_key_down('5', pygame.key.get_mods())
            self.text_field.on_key_down(')', pygame.key.get_mods())
            self.text_field.stored_string = '((' + self.text_field.stored_string
            self.text_field.cursor_position += 4
            return
        
        self.text_field.on_key_down(ch, pygame.key.get_mods())
    
    def make_executable_expression(self):
        value = self.text_field.get_value()
        
        value = value.replace('x', '*')
        
        return value
        
    def evaluate_expression(self):# to provide final result.
    
        expression = self.make_executable_expression()
        
        try:
            self.result =  str(eval(expression))
            
            self.text_box.post(self.text_field.get_value() + ' = '+ str(self.result))
            
            self.result = self.result.replace('*', 'x')
            
            self.text_field.stored_string = self.result
            
        except SyntaxError:
            self.text_box.post(self.text_field.get_value()+": Expression Syntax Error.")
            
        except NameError:
            self.text_box.post(self.text_field.get_value()+": Unknown Variable Error.")
            
    def init_calculator(self):
        pass
    
    def load(self, loadobj):
        pass
           
    def handle_event(self, events):
        pass
        
    def update(self):
        pass
    
    def draw(self, surface):
        self.push_button_group.draw(surface)
        self.text_box.draw(surface)
        self.field_group.draw(surface)
