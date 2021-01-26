import time
import pygame
from widgets import App
from widgets.Text import TextLine
from constants import *

class SplashScreen(App):
    def __init__(self, eobj):
        App.__init__(self, eobj)
        
        self.img = pygame.transform.scale(pygame.image.load("../libs/SplashScreen/hunger-for-light.jpg"), SCREEN_SIZE)
        self.rect = self.img.get_rect()
        self.rect.center = SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2
        self.size = SCREEN_SIZE
        self.screen_color = SCREEN_COLOR
        self.exit = False
        
        self.app_name = ""
        
        text = TextLine(text="SIGI", size=40, font="fonts/Acme-Regular.ttf")
        text.text_color = (0, 150, 210)
        text.text_color = (0, 107, 161)
        text.text_color = (209, 11, 123)
        text.bold = True
        text.rect.centery = 30 +20
        text.rect.x = 10
        self.text_list = []
        self.text_list.append(text)
        
        text = TextLine(text="UI Demonstration for Simplified Graphics Implementation", size=10, font="../libs/SplashScreen/fonts/Acme-Regular.ttf")
        text.text_color = (209, 11, 123)
        text.bold = True
        text.rect.centery = 53 +20
        text.rect.x = 10
        self.text_list.append(text)
        
        text = TextLine(text="Copyright [2018] [Anantha Krishna R. & Tejal Shetty]", size=7, font="../libs/SplashScreen/fonts/Acme-Regular.ttf")
        text.text_color = (209, 11, 123)
        text.bold = True
        text.rect.center = SCREEN_SIZE[0]/2, 53 +20 + 200
        self.text_list.append(text)
        
        self.anchor_time = 0
        
        self.widgets_loaded = self.engine_loaded = self.app_loading = False
        
    def widgets_imported(self):
        
        self.widgets = text = TextLine(text="Imported Widgets - libs/widgets", size=10, font="../libs/SplashScreen/fonts/Acme-Regular.ttf")
        text.text_color = (209, 11, 123)
        text.rect.centery = 240
        text.rect.x = 250
        self.text_list.append(text)
        self.widgets_loaded = True
        
    def engine_loaded_C(self):
        self.engine = text = TextLine(text="Loaded Engine - libs/widgets", size=10, font="../libs/SplashScreen/fonts/Acme-Regular.ttf")
        text.text_color = (209, 11, 123)
        text.rect.centery = 250
        text.rect.x = 250
        self.text_list.append(text)
        self.engine_loaded = True
    
    def loading_app(self, appname):
        self.engine = text = TextLine(text="Loading " + appname + " App on Engine", size=10, font="../libs/SplashScreen/fonts/Acme-Regular.ttf")
        text.text_color = (209, 11, 123)
        text.rect.centery = 260
        text.rect.x = 250
        self.text_list.append(text)
        self.app_loading = True
        
    def update(self):
        t = time.time()
        
        if not self.anchor_time: self.anchor_time = time.time()
        
        if t - self.anchor_time > 2 and not self.widgets_loaded: 
            self.widgets_imported()
        
        if t - self.anchor_time > 2.5 and not self.engine_loaded: 
            self.engine_loaded_C()
            
        if t - self.anchor_time > 5 and not self.app_loading: 
            self.loading_app(self.app_name)
            
        if t - self.anchor_time > 8.9: 
            self.exit = True
            
    def draw(self, surface):
        
        surface.blit(self.img, self.rect)
        
        for text in self.text_list:
            text.draw(surface)
        
