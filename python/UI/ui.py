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
        
        from applist import pyapplist, tcapplist
                             
        app_list_ = [key for key in pyapplist["Apps"]]
        tcapp_list_ = [key for key in pyapplist["Apps"]]
        
        # For callbacks.
        pre_text = "gnome-terminal -e "
        c_text_dict = dict()
        for key in pyapplist: 
            print key
            for keyy in pyapplist[key]:
                c_text_dict[keyy] = pre_text + "./scripts/" + keyy + ".sh"
        for key in tcapplist: 
            print key
            for keyy in tcapplist[key]:
                c_text_dict[keyy] = pre_text + "./scripts/" + keyy + ".sh"
        
        name_dict = dict()
        for key in pyapplist: 
            print key
            for keyy in pyapplist[key]:
                name_dict[keyy] = pyapplist[key][keyy]
        for key in tcapplist: 
            print key
            for keyy in tcapplist[key]:
                name_dict[keyy] = tcapplist[key][keyy]
        
        
        icons = dict()
        for name in app_list_: icons[name] = img_load(idir_+name+".png")
        
        self.button_group = ButtonGroup()
        
        s_size = int(60*SCALE_RATIO), int(60*SCALE_RATIO)
#        surf_size = int(80*SCALE_RATIO), int(70*SCALE_RATIO)
#        c = surf_size[0]/2, surf_size[1]/2

        surf = pygame.Surface(s_size).convert_alpha()
        surf.fill((200, 200,200, 70), None, pygame.BLEND_RGBA_MIN)
        
        i = 0
        j = 1
        d_size = pygame.display.get_surface().get_size()
        
        self.text_list = text_list = []
        print c_text_dict
        for key in icons:
            i += 1
            button = Button()
            img = img_scale(icons[key], s_size)
            
            if i > 2: i, j  = 1, j + 1
            
            hover = surf.copy()
            hover.blit(img, (0, 0))
            
            button.rect.center = i*d_size[0]/5, j*d_size[1]/5
            button.theme = create_button_theme(img.copy(), hover)
            button.released(self.open_app, (c_text_dict[key],))
            self.button_group.add(button)
            
            text = TextLine()
            text.text_color = (0, 0, 0)
            text.font_size = int(16*SCALE_RATIO)
            text.text = name_dict[key]
            text.rect.center = i*d_size[0]/5, j*d_size[1]/5 + s_size[0]/1.5
            text_list.append(text)
        
        game_list_ = [key for key in pyapplist["Games"]]
        icons = dict()
        
        for name in game_list_: icons[name] = img_load(idir_+name+".png")
        i, j = 0, 1
        
        for key in icons:
            i += 1
            button = Button()
            img = img_scale(icons[key], s_size)
            
            if i > 2: i, j  = 1, j + 1
            
            hover = surf.copy()
            hover.blit(img, (0, 0))
            
            button.rect.center = (i+2)*d_size[0]/5, j*d_size[1]/5
            button.theme = create_button_theme(img.copy(), hover)
            button.released(self.open_app, (c_text_dict[key],))
            self.button_group.add(button)
            
            text = TextLine()
            text.text_color = (0, 0, 0)
            text.font_size = int(16*SCALE_RATIO)
            text.text = name_dict[key]
            text.rect.center = (i+2)*d_size[0]/5, j*d_size[1]/5 + s_size[0]/1.5
            text_list.append(text)
        
        s_size = int(50*SCALE_RATIO), int(50*SCALE_RATIO)
        surf = pygame.Surface(s_size).convert_alpha()
        surf.fill((200, 200,200, 70), None, pygame.BLEND_RGBA_MIN)
        
        game_list_ = [key for key in tcapplist["Games"]]
        icons = dict()
        
        for name in game_list_: icons[name] = img_load(idir_+name+".png")
        i, j = 0, 4
        
        for key in icons:
            i += 1
            button = Button()
            img = img_scale(icons[key], s_size)
            
            if i > 3: i, j  = 1, j + 1
            
            hover = surf.copy()
            hover.blit(img, (0, 0))
            
            button.rect.center = (i+3)*d_size[0]/7, j*d_size[1]/5
            button.theme = create_button_theme(img.copy(), hover)
            button.released(self.open_app, (c_text_dict[key],))
            self.button_group.add(button)
            
            text = TextLine()
            text.text_color = (0, 0, 0)
            text.font_size = int(16*SCALE_RATIO)
            text.text = name_dict[key]
            text.rect.center = (i+3)*d_size[0]/7, j*d_size[1]/5 + s_size[0]/1.5
            text_list.append(text)
        
        app_list_ = [key for key in tcapplist["Apps"]]
        icons = dict()
        
        for name in app_list_: icons[name] = img_load(idir_+name+".png")
        i, j = 0, 4
        
        for key in icons:
            i += 1
            button = Button()
            img = img_scale(icons[key], s_size)
            
            if i > 3: i, j  = 1, j + 1
            
            hover = surf.copy()
            hover.blit(img, (0, 0))
            
            button.rect.center = (i)*d_size[0]/7, j*d_size[1]/5
            button.theme = create_button_theme(img.copy(), hover)
            button.released(self.open_app, (c_text_dict[key],))
            self.button_group.add(button)
            
            text = TextLine()
            text.text_color = (0, 0, 0)
            text.font_size = int(16*SCALE_RATIO)
            text.text = name_dict[key]
            text.rect.center = (i)*d_size[0]/7, j*d_size[1]/5 + s_size[0]/1.5
            text_list.append(text)
        
        self.button_group.add(button)
        
        
        
        text = TextLine(text="Apps")
        text.rect.center = (3.75*d_size[0]/12, d_size[1]/10)
        text_list.append(text)
        
        text = TextLine(text="Games")
        text.rect.center = (9*d_size[0]/12, d_size[1]/10)
        text_list.append(text)
        
        
        from widgets.Clock import Clock
        self.clock = Clock()
        self.clock.center = (d_size[0]/2, d_size[1]/2)
#        self.clock.fill = True
        self.clock.lable_radius = (98/2, 94/2, 90/2, 82/2, 73/2  )
        self.clock.radius = 50
        self.clock.radius_tuple = (20, 35, 40)
        
        
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
        
        from widgets.Paint import PaintSurface
        
        
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
        self.clock.update()
        
    def draw(self, surface):
        
        self.slideshow.draw(surface)        
        self.clock.draw(surface)
        
#        self.paint.draw(surface)
        self.button_group.draw(surface)
        for text in self.text_list: 
            text.draw(surface)
        
