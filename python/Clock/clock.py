# clock.py
"""
    VERSION: v1.0 (The Emotion Core)
    Authors: Anantha Krishna R.
"""

"""
    Completion Date 5 Nov, 10:45PM.
"""
from widgets.Clock import Clock, Leaf
import pygame
from widgets.Text import TextLine
from widgets.Button import Button, ButtonGroup, create_button_theme

class clock():
    def __init__(self, engineobj):
        self.g = engineobj
        
        self.init_clock()
        self.clock = Clock()
        
        d_size = pygame.display.get_surface().get_size()
        
        self.clock.set_center((d_size[0]/2, d_size[1]/2))
        self.clock.radius = 100
        self.init_leaves()
        self.init_switch_buttons()
        
    def init_leaves(self):
        d_size = pygame.display.get_surface().get_size()
        
        self.leaf_list = []
        self.text_list = []
        
        hour_list = list(str(i) for i in range(1, 13))
        self.hour_clock_leaf = Leaf(20, hour_list)
        self.hour_clock_leaf.rect.center = d_size[0]/2 - 30, d_size[1]/2 - 30
        self.leaf_list.append(self.hour_clock_leaf)
        
        minute_list = list(str(i) for i in range(1, 61))
        self.minute_clock_leaf = Leaf(20, minute_list)
        self.minute_clock_leaf.rect.center = d_size[0]/2, d_size[1]/2 - 30
        self.leaf_list.append(self.minute_clock_leaf)
        
        second_list = list(str(i) for i in range(1, 61))
        self.second_clock_leaf = Leaf(20, second_list)
        self.second_clock_leaf.rect.center = d_size[0]/2 + 30, d_size[1]/2 - 30
        self.leaf_list.append(self.second_clock_leaf)
        
        date_list = list(str(i) for i in range(1, 32))
        self.date_clock_leaf = Leaf(20, date_list)
        self.date_clock_leaf.rect.center = d_size[0]/2 + 70, d_size[1]/2 
        self.leaf_list.append(self.date_clock_leaf)
        
        text_color = (44, 44, 44)
        
        text_h = TextLine(text='h')
        text_h.text_color = text_color
        text_h.rect.center = d_size[0]/2 - 30, d_size[1]/2 - 58
        self.text_list.append(text_h)
        
        text_m = TextLine(text='m')
        text_m.text_color = text_color
        text_m.rect.center = d_size[0]/2, d_size[1]/2 - 58
        self.text_list.append(text_m)
        
        text_s = TextLine(text='s')
        text_s.text_color = text_color
        text_s.rect.center = d_size[0]/2 + 30, d_size[1]/2 - 58
        self.text_list.append(text_s)
        
        text_D = TextLine(text='D')
        text_D.text_color = text_color
        text_D.rect.center = d_size[0]/2 + 70, d_size[1]/2 - 28
        self.text_list.append(text_D)
        
        text = TextLine(text='Watch Clock')
        text.text_color = text_color
        text.font_size = 30
        text.rect.center = d_size[0]/2, d_size[1]/5
        self.text_list.append(text)
        
    def init_switch_buttons(self):
        d_size = pygame.display.get_surface().get_size()
        
        text = TextLine(text = "Toggle needles motion")
        rect = pygame.Rect((0, 0, 150, 20))
        text.rect.center = rect.width/2, rect.height/2
        surf = pygame.Surface((150, 20))
        surf.fill((111, 111, 111))
        text.draw(surf)
        toggle_button_1 = Button()
        toggle_button_1.theme = create_button_theme(surf)
        toggle_button_1.rect.center = 3*d_size[0]/4 + 20, 3*d_size[1]/4
        toggle_button_1.clicked(self.toogle_smooth_rough, ())
        
        text.text = "Toggle lables"
        text.rect.center = rect.width/2, rect.height/2
        surf = pygame.Surface((150, 20))
        surf.fill((100, 100, 100))
        text.draw(surf)
        toggle_button_2 = Button()
        toggle_button_2.theme = create_button_theme(surf)
        toggle_button_2.rect.center = 3*d_size[0]/4 + 20, 3*d_size[1]/4 - 30
        toggle_button_2.clicked(self.toogle_lables, ())
        
        self.toggle_button = ButtonGroup()
        self.toggle_button.add([toggle_button_1, toggle_button_2])
        
    def init_clock(self):
        pass
        
    def toogle_lables(self):
        """toogle_lables() - Switch between different types of numbering."""
        lable_no, max_count = self.clock.lable_no, self.clock.max_lable_count
        self.clock.lable_no = 0 if lable_no + 1 > max_count else lable_no + 1
            
    def toogle_smooth_rough(self):
        """toogle_smooth_rough() - toogle the needle and leaf smoothness."""
        self.clock.smooth_needle = not self.clock.smooth_needle
    
    def load(self, loadobj):
        pass
        
    def handle_event(self, events):
        pass
        
    def update(self):
        self.clock.update()
        hh, mm, ss = self.clock.get_hms()
        DD, MM, YY = self.clock.get_DMY()
        
        self.hour_clock_leaf.readjust_crop(hh*100)
        self.minute_clock_leaf.readjust_crop(mm*100)
        self.second_clock_leaf.readjust_crop(ss*100)
        
        self.date_clock_leaf.readjust_crop((DD/31.) * 100)
        pass
    
    def draw(self, surface):
        # Handle leaf drawing.
        for leaf in self.leaf_list:
            leaf.draw(surface)
        
        for text in self.text_list:
            text.draw(surface)
        
        # Draw Toggle Button.
        self.toggle_button.draw(surface)
        self.clock.draw(surface)
