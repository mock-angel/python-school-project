# Aberration.py
"""
    4B3RR4710N.
"""
import pygame
from TitleBar import TitleBar
import widgets
from widgets import TextLine
from widgets.Button import Button, ButtonGroup, create_button_theme
import system

SELECTION_SCREEN = 1
GAME_SCREEN = 0
END_GAMESCREEN = 2

class Aberration():
    def __init__(self, engine_obj):
        self.title = TitleBar(engine_obj)
        
        self.init_selection_screen()
        size = pygame.display.get_surface().get_size()
        self.end_screen_panel = widgets.Panel()
        self.end_game_text = TextLine(text="Hack Failed!", size=30)
        self.end_game_text.rect.center = size[0]/2, size[1]/2
        self.screen_info = SELECTION_SCREEN
    def init_selection_screen(self):
        panel = self.selection_screen_panel = widgets.Panel()
        
        # Design selection screen here.
        self.selection_screen = widgets.ButtonGroup()
        
        def start_callback():
            self.switch_screen(GAME_SCREEN)
            
        text = widgets.TextLine(text="Start Game")
        text.text_color = (222, 222, 222)
        text.rect.center = 50, 10

        start_surf = pygame.Surface((100, 20)).convert_alpha()
        start_surf.fill((77, 0, 0, 55), None, pygame.BLEND_RGBA_MIN)
        text.draw(start_surf)
        
        disp = pygame.display.get_surface().get_size()
        start_button = widgets.Button()
        start_button.theme = create_button_theme(start_surf)
        start_button.rect.center = disp[0]/2, disp[1]/2
        start_button.clicked(start_callback, ())
        self.sel_button_group = widgets.ButtonGroup()
        self.sel_button_group.add(start_button)
        
    def switch_screen(self, screen):
        if screen == GAME_SCREEN: 
            self.System = system.System()
            self.Virus = system.virus.Virus()
            self.Virus.infect(self.System)
            
            self.System.set_abberation(self)
        self.screen_info = screen

    def load(self, loading_obj):
        pass
        
    def handle_event(self, events):
        if self.screen_info == GAME_SCREEN: return
        
        elif self.screen_info == SELECTION_SCREEN:
            self.selection_screen_panel.update(events)
        
        elif self.screen_info == END_GAMESCREEN:
            self.end_screen_panel.update(events)
            
    def update(self):
        if self.screen_info == GAME_SCREEN:
            self.System.update()
            self.Virus.update()
        
        elif self.screen_info == SELECTION_SCREEN:
            self.selection_screen.update()
        
    def draw(self, surface):
        self.title.draw(surface)
            
        if self.screen_info == GAME_SCREEN:
            self.System.draw(surface)
            if self.Virus.ready: self.Virus.draw(surface)
            
        elif self.screen_info == SELECTION_SCREEN:
            self.selection_screen.draw(surface)
            self.sel_button_group.draw(surface)
            
        elif self.screen_info == END_GAMESCREEN:
            self.end_game_text.draw(surface)
            
