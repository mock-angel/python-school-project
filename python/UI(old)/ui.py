"""
    UI version 0.1
    Completion Date 7 Nov
    Spent 35 cumulative mins on the project.
    
    Authors: Anantha Krishna R.
"""
import os
from math import *
from threading import Thread

import pygame

from widgets.Text import TextLine
#from widgets.TextBox import AutoScrollingTextBox
from widgets.Button import Button, ButtonGroup, create_button_theme
from widgets.SlideShow import SlideShow

from constants import *
class ui():
    def __init__(self, engineobj):
        self.g = engineobj
        
        self.threads = []
        
        self.init_buttons()
        
    def init_buttons(self):
        
        d_size = pygame.display.get_surface().get_size()
        
        self.push_button_group = ButtonGroup()
        
        img_load = pygame.image.load 
        img_scale = pygame.transform.scale
        
        idir_ = "data/icons/"
        
        text_dict ={ "pycalculator": "Calculator", 
                "pychess": "Viking chess",
                 "pyclock" : "Watch Clock",
                  "pyminesweeper": "MineSweeper",
                   "pydualnback" : "Dual n-back",
                    "pycodeclash": "Code Clash",
                     "pydraw" : "PyDraw",
                      "pypdtb" : "PyPeriodic Table",
                       "pyaberration" : "Abberration",
                        "tccalculator" : "Calculator",
                         "tcdiscsh" : "Disk Shooter",
                          "tcclock" : "Clock",
                           "tcvirpet" : "Virtual Pet",
                            "tcpiano" : "Piano",
                             "tcsnake" : "Snake"}
                             
        list_ = [key for key in text_dict]
        
        # For callbacks.
        pre_text = "gnome-terminal -e "
        c_text_dict ={ "pycalculator": pre_text + "./scripts/pycalculator.sh", 
                "pychess": pre_text + "./scripts/pychess.sh", 
                 "pyclock" : pre_text + "./scripts/pyclock.sh", 
                  "pyminesweeper": pre_text + "./scripts/pyminesweeper.sh", 
                   "pydualnback" :pre_text +  "./scripts/pydualnback.sh", 
                    "pycodeclash": pre_text + "./scripts/pycodeclash.sh", 
                     "pydraw" : pre_text + "./scripts/pydraw.sh", 
                      "pypdtb" : pre_text + "./scripts/pypdtb.sh", 
                       "pyaberration" : pre_text + "./scripts/pyaberration.sh",
                        "tccalculator" : pre_text + "./scripts/tccalculator.sh", 
                         "tcdiscsh" : pre_text + "./scripts/tcdiscsh.sh", 
                          "tcclock" : pre_text + "./scripts/tcclock.sh", 
                           "tcvirpet" : pre_text + "./scripts/tcvirpet.sh", 
                            "tcpiano" : pre_text + "./scripts/tcpiano.sh", 
                             "tcsnake" : pre_text + "./scripts/tcsnake.sh", }
        
        icons = dict()
        for name in list_: 
            icons[name] = img_load(idir_+name+".png")
        
        self.button_group = ButtonGroup()
        
        s_size = int(60*SCALE_RATIO), int(60*SCALE_RATIO)
        surf_size = int(80*SCALE_RATIO), int(80*SCALE_RATIO)
        c = surf_size[0]/2, surf_size[1]/2
        
        surf = pygame.Surface(s_size).convert_alpha()
        surf.fill((200, 200,200, 70), None, pygame.BLEND_RGBA_MIN)
        
        i = 0
        j = 1
        d_size = pygame.display.get_surface().get_size()
        
        self.text_list = text_list = []
        
        for key in icons:
            i += 1
            button = Button()
            img = img_scale(icons[key], s_size)
            
            if i > 4: i, j  = 1, j + 1
            
            hover = surf.copy()
            hover.blit(img, (0, 0))
            
            button.rect.center = i*d_size[0]/5, j*d_size[1]/5
            button.theme = create_button_theme(img.copy(), hover)
            button.released(self.open_app, (c_text_dict[key],))
            self.button_group.add(button)
            
            text = TextLine()
            text.text_color = (0, 0, 0)
            text.font_size = int(16*SCALE_RATIO)
            text.text = text_dict[key]
            text.rect.center = i*d_size[0]/5, j*d_size[1]/5 + s_size[0]/1.5
            text_list.append(text)
            
        self.button_group.add(button)
        
        self.slideshow = SlideShow()
        dir__ = "Wallpapers/"
        
        # Note: Simply adding an image file into Wallpapers folder is enough to add
        # it to slideshow.
        from os import listdir
        from os.path import isfile, join
        onlyfiles = [f for f in listdir(dir__) if isfile(join(dir__, f))]
        
        slideslist = []
        for path in onlyfiles:
            slideslist.append((img_load(dir__+path)).convert_alpha())
            
        for img in slideslist:
            self.slideshow.add_slide(img)
            
    def __del__(self):
        for thread in self.threads:
            thread.join()
            
    def open_app(self, exe_text):
        t1 = Thread(target=os.system, args=(exe_text,) )
        t1.start()
        self.threads.append(t1)
    
    def load(self, obj):
        """No loading script."""
        
    def handle_event(self, events):
        pass 
    
    def update(self):
        self.slideshow.update()
        self.button_group.update()
    
    def draw(self, surface):
        
        self.slideshow.draw(surface)        
        
        self.button_group.draw(surface)
        for text in self.text_list: 
            text.draw(surface)
