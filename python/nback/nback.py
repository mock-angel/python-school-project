# nback.py
"""
    VERSION: v0.2
    
    Authors: Anantha Krishna R.
"""
import pygame
from Jack import Jack
import widgets
from widgets.Button import create_button_theme
SELECTION_SCREEN = 1
GAME_SCREEN = 0
END_GAMESCREEN = 2

class nback:
    def __init__(self, engineobj):
        self.g = engineobj
        
        engineobj.set_screen_color((255, 255, 255))
        
        self.clock = pygame.time.Clock()
        self.speed_inv = 1
        
        self.init_selection_screen()
        self.init_game_screen()
        self.init_end_game_screen()
        
        self.switch_screen(SELECTION_SCREEN)
        
    def init_selection_screen(self):
        panel = self.selection_screen_panel = widgets.Panel()
        
        # Design selection screen here.
        self.selection_screen = widgets.ButtonGroup()
        
        def start_callback():
            self.switch_screen(GAME_SCREEN)
            
        text = widgets.TextLine(text="Start Game")
        text.text_color = (0, 0, 0)
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
        
    def init_game_screen(self):
        self.jack = Jack(self)
        
        def image_match_callback():
            self.jack.register('a')
        
        def audio_match_callback():
            self.jack.register('l')
        
        # Design game screen here.
        def init_buttons():
            """Initialised button sprites for ingame interactions.."""
            self.button_panel = widgets.Panel()
            
            d_size = pygame.display.get_surface().get_size()
            
            left_b = widgets.Button(self.button_panel)
            left_b.theme = create_button_theme(pygame.image.load("data/PositionMatch.png").convert_alpha())
            left_b.rect.center = d_size[0]/4, d_size[0]/14 * 13
            left_b.clicked(image_match_callback, ())
            
            right_b = widgets.Button(self.button_panel)
            right_b.theme = create_button_theme(pygame.image.load("data/AudioMatch.png").convert_alpha())
            right_b.rect.center = 3*d_size[0]/4, d_size[0]/14 * 13
            right_b.clicked(audio_match_callback, ())
            
            self.button_group = widgets.ButtonGroup()
            self.button_group.add(left_b, right_b)
        
        init_buttons()
    
    def init_end_game_screen(self):
        
        panel = self.end_screen_panel = widgets.Panel()
        start_button = widgets.Button(panel)
        
        size = pygame.display.get_surface().get_size()
        start_button.rect.center = size[0]/2, size[1]/2
        
        self.end_screen_buttons = widgets.ButtonGroup()
        self.end_screen_buttons.add(start_button)
        
        nu = self.numerical_score = widgets.TextLine()
        nu.text_color = (65, 65, 65)
        nuf = self.numerical_failed = widgets.TextLine()
        nuf.text_color = (65, 65, 65)
        al = self.alphabet_score = widgets.TextLine()
        al.text_color = (65, 65, 65)
        alf = self.alphabet_failed = widgets.TextLine()
        alf.text_color = (65, 65, 65)
        ta = self.total_answered = widgets.TextLine()
        ta.text_color = (65, 65, 65)
        tf = self.total_failed = widgets.TextLine()
        tf.text_color = (65, 65, 65)
        of  =self.out_of = widgets.TextLine()
        of.text_color = (65, 65, 65)
#        esc = widgets.TextLine()
        
        self.game_screen_text_list = [nu, al, nuf, alf, ta, tf, of]
        
    def switch_screen(self, screen):
        
        self.screen_info = screen
    
    def set_speed(self, speed):
        
        self.speed_inv /= speed
    
    def end_screen(self, back_obj):
        """"""
        
        size = pygame.display.get_surface().get_size()
        
        self.numerical_score.text = "Pattern Scored : " + str(back_obj.pattern_answered_count)
        self.numerical_score.rect.center = 2*size[0]/5, size[1]/2 - 10
        
        self.alphabet_score.text = "Alphabet Scored : " + str(back_obj.audio_answered_count)
        self.alphabet_score.rect.center = 2*size[0]/5, size[1]/2 + 10
        
        
        self.numerical_failed.text = "Pattern Failed : " + str(back_obj.pattern_answered_count)
        self.numerical_failed.rect.center = 3*size[0]/5, size[1]/2 - 10
        
        self.alphabet_failed.text = "Alphabet Failed : " + str(back_obj.pattern_answered_count)
        self.alphabet_failed.rect.center = 3*size[0]/5, size[1]/2 + 10
        
        self.total_answered.text = "Total Scored : " + str(back_obj.answered_count)
        self.total_answered.rect.center = 2*size[0]/5, size[1]/2 + 35
        
        self.total_failed.text = "Total Failed : " + str(back_obj.failed_count)
        self.total_failed.rect.center = 3*size[0]/5, size[1]/2 + 35
        
        self.out_of.text = "Out of : " + str(back_obj.answer_count)
        self.out_of.rect.center = size[0]/2, size[1]/2 + 65
        
        self.switch_screen(END_GAMESCREEN)
    
    def load(self, loadobj):
        pass
    
    def handle_event(self, events):# DONE.
        
        if self.screen_info == GAME_SCREEN:
            for event in events:
                if event.type == pygame.KEYDOWN and len(pygame.key.name(event.key)) == 1:
                     self.jack.register(pygame.key.name(event.key))
            self.button_panel.update(events)
            
        elif self.screen_info == SELECTION_SCREEN:
            self.selection_screen_panel.update(events)
        
        elif self.screen_info == END_GAMESCREEN:
            self.end_screen_panel.update(events)
        
    def update(self):# DONE.
    
        if self.screen_info == GAME_SCREEN:
            self.jack.update()
        
        elif self.screen_info == SELECTION_SCREEN:
            self.selection_screen.update()
    
    def draw(self, surface):# DONE
        
        if self.screen_info == GAME_SCREEN:
            self.jack.draw(surface)
            self.button_group.draw(surface)
            
        elif self.screen_info == SELECTION_SCREEN:
            self.selection_screen.draw(surface)
            self.sel_button_group.draw(surface)
            
        elif self.screen_info == END_GAMESCREEN:
            self.end_screen_buttons.draw(surface)
            
            for text in self.game_screen_text_list:
                text.draw(surface)
