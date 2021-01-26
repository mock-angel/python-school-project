'''
    VERSION: V1.0 (Mythical Mayhem)

    Authors: Anantha Krishna R.
'''

"""
    Completion Date 4 Nov, 10:30PM.
    
    TODO: Provide more options to user, i.e,  option to 
            - change color of board.
            - change positions for starting players.
            - change color of pieces.
            - set choose from boards, or create a board.
"""
import pygame

import widgets
from widgets.TextField import TextFieldSingleLine, TextField
from widgets.Button import Button, ButtonGroup, create_button_theme
from widgets.TextBox import AutoScrollingTextBox
from ChessBoard import ChessBoard

SELECTION_SCREEN = 1
GAME_SCREEN = 0

class chess():
    def __init__(self, engineobj):
        self.g = engineobj
        
        text_box_rect = pygame.Rect([525, 50, 300, 400])
        self.text_box = AutoScrollingTextBox(text_box_rect, font_name="Sans")
        
        engineobj.set_screen_color((0, 0, 0))
        
        self.init_selection_screen()
        self.init_game_screen()
        
        self.screen_info = SELECTION_SCREEN
        self.switch_screen(SELECTION_SCREEN)
        
        self.free_move = False
        
    def init_selection_screen(self):
        
        
        panel = self.selection_screen_panel = widgets.Panel()
        
        # Design selection screen here
        self.selection_screen_buttons = widgets.ButtonGroup()
        
        tb = self.text_box
        
        self.plyr_1_name_text = TextFieldSingleLine(panel, "Player1", (150, 20))
        self.plyr_1_name_text.set_name("Light")
        self.plyr_1_name_text.max_display_length = 20
        self.plyr_1_name_text.rect.center = tb.rect.x + tb.rect.width/2, tb.rect.y
        
        self.plyr_2_name_text = TextFieldSingleLine(panel, "Player2", (150, 20))
        self.plyr_2_name_text.set_name("Dark")
        self.plyr_2_name_text.max_display_length = 20
        self.plyr_2_name_text.rect.center = tb.rect.x + tb.rect.width/2, tb.rect.y + 30
        
        self.max_turn_text = TextFieldSingleLine(panel, "0", (150, 20))
        self.max_turn_text.set_name("Turn")
        self.max_turn_text.max_display_length = 20
        self.max_turn_text.rect.center = tb.rect.x + tb.rect.width/2, tb.rect.y + 80
        
        allowed_chars = [str(i) for i in range(0, 10)]
        self.max_turn_text.set_allowed_chars(allowed_chars)
        
        surf = pygame.Surface((90, 18))
        surf.fill((33, 33, 33))
        
        b_surf = surf.copy()
        b_rect = b_surf.get_rect()
        
        # Text Surface. SEE? I AM VERY LAZY!!
        text = widgets.TextLine(text="Start Game")
        text.rect.center = center = b_rect.width/2, b_rect.height/2
        b_surf.blit(text.image, text.rect)
        b_start = Button(panel)
        b_start.theme = create_button_theme(b_surf)
        b_start.rect.center = tb.rect.x + tb.rect.width/2, tb.rect.y + 66 + 50
        
        b_surf_1 = surf.copy()
        text.text = "Free Move"
        text.rect.center = center
        b_surf_1.blit(text.image, text.rect)
        b_free_move = Button(panel)
        b_free_move.theme = create_button_theme(b_surf_1)
        b_free_move.rect.center = tb.rect.x + tb.rect.width/2, tb.rect.height+ 50
        
        self.start_b = b_start
        b_start.clicked(self.start_game, ())
        
        self.free_move_b = b_free_move
        b_free_move.clicked(self.free_move_activate, ())
        
        self.text_field = TextField()
        self.text_field.add(self.plyr_1_name_text)
        self.text_field.add(self.plyr_2_name_text)
        self.text_field.add(self.max_turn_text)
        self.text_field.returned(self.start_game, ())
        self.selection_screen_buttons.add([b_start, b_free_move])
        
    def init_game_screen(self):
        panel = self.game_screen_panel = widgets.Panel()
        
        surf = pygame.Surface((90, 18))
        surf.fill((33, 33, 33))
        
        b_surf = surf.copy()
        b_rect = b_surf.get_rect()
        
        text = widgets.TextLine(text="Reset Game")
        text.rect.center = b_rect.width/2, b_rect.height/2
        
        b_surf_2 = surf.copy()
        b_surf_2.blit(text.image, text.rect)
        
        b_reset = Button(panel)
        b_reset.theme = create_button_theme(b_surf_2)
        b_reset.clicked(self.reset, ())
        
        tb = self.text_box
        
        self.reset_b = b_reset
        b_reset.rect.center = tb.rect.x + tb.rect.width/2, tb.rect.y + tb.rect.height+20
        
        # Design game screen here.
        self.chess_board = ChessBoard(self)
    
    def free_move_activate(self):
        self.free_move_b.disable()
        
        self.free_move = True
        
    def start_game(self):
        self.chess_board.player["name"]['l'] = self.plyr_1_name_text.get_value()
        self.chess_board.player["name"]['d'] = self.plyr_2_name_text.get_value()
        self.chess_board.max_turns = int(self.max_turn_text.get_value())
        self.chess_board.reset_text_box()
        
        self.free_move = False
        
        self.switch_screen(GAME_SCREEN)
        self.chess_board.started = True
        
    def reset(self):
        self.chess_board.reset()
        self.free_move_b.enable()
        self.free_move = False
        self.switch_screen(SELECTION_SCREEN)
        
    def switch_screen(self, screen):
        self.screen_info = screen
    
    def load(self, loadobj):
        pass
    
    def handle_event(self, events):# DONE.
        
        if self.screen_info == GAME_SCREEN:
            self.game_screen_panel.update(events)
            
        elif self.screen_info == SELECTION_SCREEN:
            self.selection_screen_panel.update(events)
            
    def update(self):# DONE.
        pass
        
    def draw(self, surface):# DONE.
        
        if self.screen_info == GAME_SCREEN:
            self.chess_board.draw(surface)
            self.text_box.draw(surface)
            self.reset_b.draw(surface)
            
        elif self.screen_info == SELECTION_SCREEN:
            self.chess_board.draw(surface)
            
            self.text_field.draw(surface)
            
            self.selection_screen_buttons.draw(surface)
