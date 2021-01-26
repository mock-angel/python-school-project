# Mine.py
"""
    VERSION: v5 (Mad Hunter!)
    Authors: Anantha Krishna R.
"""

"""
Create sprites for game screen, selection screen and custom screen
# TODO: HighScore screen.


Mine
    * g - UpdateEngine -> EngineGraphics
    * screen_info - Current screen const.
    * timer - Tiner()  - Timer object to perform stopwatch operations.
    
    - init_game_screen()
    - init_selection_screen()
    - init_custom_screen()
    
    - switch_screen(SCREEN_CONST)
    
    - load(loadingobj)
    - handle_event(events)
    - update()
    - draw(surface)
"""
import time
import pygame
from pygame.locals import *

from widgets import Timer, Button
from tile import Tile, TileGroup
from TileEssentials import *
from widgets.Text  import TextLine
from widgets import ButtonGroup

from widgets import Panel
from widgets.TextField import TextFieldSingleLine, TextField

from constants import *

class Mine():
    def __init__(self, engineObj):
        
        self.g = engineObj
        
        self.timer = Timer()
        
        self.init_game_screen()
        self.init_selection_screen()
        self.init_custom_screen()
        
        self.screen_info = SELECTION_SCREEN
        self.switch_screen(SELECTION_SCREEN)
        
    #init_game_screen
    ######################################################################
    def init_game_screen(self):
        """ init_game_screen() - Loads actual game screen objects.
        
        USES:
            TileGroup()
            TileGroup.load()
            
            ButtonGroup()
            self.load_option_buttons()
        """
    
        panel = self.game_screen_panel = Panel()
        
        # Load the TileGroup that contains every thing required to run the game.
        
        self.TileGroup = TileGroup(self.game_screen_panel, self.timer)
        self.TileGroup.load()
        
        self.load_option_buttons()
        self.load_other_buttons() # loads flag and timer.
    def load_option_buttons(self):#game_screen
        """ load_option_buttons<() - Loads option buttons for game screen.
        
        They are then attatched to the TileGroup.
        
        USES: 
            self.option_buttons_list
            TileGroup.attatch_option_buttons(self.option_buttons_list)
        """
        
        # Load images and make themes.
        
        # Start over button.
        default =  pygame.image.load("button/start_over/default.png")
        hover = pygame.image.load("button/start_over/hover.png")
        disabled = pygame.image.load("button/start_over/disabled.png")
        pressed = pygame.image.load("button/start_over/held.png")
        bt_startover = create_button_theme(default, hover, pressed, disabled)
        
        # Resume Button.
        default =  pygame.image.load("button/resume/default.png")
        hover = pygame.image.load("button/resume/hover.png")
        pressed =  pygame.image.load("button/resume/held.png")
        self.bt_resume = create_button_theme(default, hover, pressed)
        
        # Pause Button.
        default =  pygame.image.load("button/pause/default.png")
        hover = pygame.image.load("button/pause/hover.png")
        disabled = pygame.image.load("button/pause/disabled.png")
        pressed =  pygame.image.load("button/pause/held.png")
        self.bt_pause = create_button_theme(default, hover, pressed, disabled)
        
        # Change difficulty button.
        default =  pygame.image.load("button/change_difficulty/default.png")
        hover = pygame.image.load("button/change_difficulty/hover.png")
        pressed = pygame.image.load("button/change_difficulty/held.png")
        bt_change_difficulty = create_button_theme(default, hover, pressed)
        
        # Generate buttons using themes and add to Group.
        
        self.option_buttons_list = ButtonGroup()
        
        # Start over button.
        start_over = Button(self.game_screen_panel)
        start_over.label = "start_over"
        start_over.theme = bt_startover
        start_over.rect.x, start_over.rect.y = 297, 193
        start_over.disable()
        start_over.released(self.TileGroup.start_over, ())
        self.option_buttons_list.add(start_over)
        
        # Change difficulty button.
        change_difficulty = Button(self.game_screen_panel)
        change_difficulty.label = "change_difficulty"
        change_difficulty.theme = bt_change_difficulty
        change_difficulty.rect.x = 297
        change_difficulty.rect.y = 193 + 62
        change_difficulty.released(self.switch_to_change_difficulty_screen, ())
        self.option_buttons_list.add(change_difficulty)
        
        # Pause Button.
        pause = Button(self.game_screen_panel)
        pause.label = "pause"
        pause.theme = self.bt_pause
#        pause.rect.x = 297
#        pause.rect.y = 193 + 62*2
        pause.disable()
        self.option_buttons_list.add(pause)
        
        resume = Button(self.game_screen_panel)
        resume.label = "resume"
        resume.theme = self.bt_resume
        resume.rect = pause.rect
#        pause.rect.x = 297
#        pause.rect.y = 193 + 62*2
        resume.disable()
        self.option_buttons_list.add(resume)
        
        self.flag_static_sprite = fsp = Button()
        fsp.label = "flag"
        img = pygame.image.load("data/themes/bgcolors/Tile/flag.png").convert_alpha()
        img = pygame.transform.scale(img, (32, 32))
        fsp.theme = create_button_theme(img)
        fsp.disable()
        self.option_buttons_list.add(fsp)
        
        self.clock_static_sprite = csp = Button()
        csp.label = "clock"
        img = pygame.image.load("data/themes/bgcolors/Tile/flag.png").convert_alpha()
        csp.theme = create_button_theme(img)
        csp.disable()
        self.option_buttons_list.add(fsp)
        
        # Now attatch it to TileGroup.
        
        self.TileGroup.attatch_option_buttons(self.option_buttons_list)
    
    def load_other_buttons(self):
        # Pause Button.
        pass
    #init_selection_screen
    ######################################################################
    def init_selection_screen(self):
        panel = self.selection_screen_panel = Panel()
        
        # Load basic oversized images.
        
        default_surf = default_surf = pygame.image.load("button/selection/default.png")
        hover_surf = hover_surf = pygame.image.load("button/selection/hover.png")
        held_surf = held_surf = pygame.image.load("button/selection/held.png")
        disabled_surf = disabled_surf = pygame.image.load("button/selection/disabled.png")
        
        THEME = create_button_theme(default_surf, hover_surf, held_surf, disabled_surf)
        
        size = default_surf.get_size()
        
        scale_size = (186, 186) 
        
        def draw_text(mine_size_str, mine_count_str, post_text_str,  alpha_surf):
            """
            
            Consider surfaces x and y with surfaces (-x-) and (-y-) respectively
            lying on a parent surface marked as --- ---.
            ---(-x-)(-y-)--- in orer to place (-x-)(-y-) in the center, the x's center
            is set to [(parent_surface.width/2)] - [width of (-y-)/2]
            """
            text_surf = alpha_surf.copy().convert_alpha()
            
            rect = text_surf.get_rect()
            size = text_surf.get_size()
            
            # "Mines" text.
            text_mines = TextLine(font = "Sans",text = post_text_str)
            text_mines.bold = False
            text_mines.font_size = 14
            text_mines.text_color = (60, 60, 60)
            
            # Draw 8x8 at the center of the image.
            text = TextLine(font = "Sans")
            text.text_color = (60, 60, 60)
            text.text = mine_size_str
            text.font_size = 16
            text.bold = True
            text.rect.center = size[0]/2, size[1]/2 - text.rect.height/2
            text.draw(text_surf)
            print "sizetest", text.rect.center
            # Mine count.
            text.text = mine_count_str
            text.size = 16
            text.bold = True
            x = size[0]/2 - (text_mines.rect.width)/2
            y = size[1]/2 + text.rect.height/2
            text.rect.center = x, y
            text.draw(text_surf)
            
            # "Mines" is drawn.
            x = size[0]/2 + text.rect.width/2 
            text_mines.rect.center = x, y
            text_mines.draw(text_surf)
            
            return text_surf
        
        # All surfaces are now generated with the corrected size.
        
        alpha_surf = pygame.Surface(scale_size).convert_alpha()
        alpha_surf.fill((0, 0, 0, 0), None, pygame.BLEND_RGBA_MULT)
        
        # Draw text in desired format on the alpha_surf.
        
        text_8x8_surf = draw_text("8 x 8", "10", " mines", alpha_surf)
        text_16x16_surf = draw_text("16 x 16", "40", " mines", alpha_surf)
        text_30x16_surf = draw_text("30 x 16", "99", " mines", alpha_surf)
        text_custom_surf = draw_text("?", "", "Custom", alpha_surf)
        
        # Generate the theme using the surface having text.
        
        def make_selection_theme(text_surface, scale_size, default_theme):
            """make_selection_theme() - returns theme.
            
            Uses default theme and blits textsurface over it"""
            theme = default_theme
            
            default = scale(theme["default"].copy(), scale_size)
            default.blit(text_surface, (0, 0))
        
            hover = scale(theme["hover"].copy(), scale_size)
            hover.blit(text_surface, (0, 0))
            
            held = scale(theme["pressed"].copy(), scale_size)
            held.blit(text_surface, (0, 0))
            
            disabled = scale(theme["disabled"].copy(), scale_size)
            disabled.blit(text_surface, (0, 0))
            
            return create_button_theme(default, hover, held, disabled)
        
        # THEMES:
        _8x8_selection_theme = make_selection_theme(text_8x8_surf, scale_size, THEME)
        _16x16_selection_theme = make_selection_theme(text_16x16_surf, scale_size, THEME)
        _30x16_selection_theme = make_selection_theme(text_30x16_surf, scale_size, THEME)
        _custom_selection_theme = make_selection_theme(text_custom_surf, scale_size, THEME)
        
        #######
        # TODO: Rework this code and make it small.
        #
        # Offsetxy from center - ox, oy
        # cx, cy = Calculated center co-ords of buttons.
        
        # FIXME: START TRASH.
        
        def make_selection_button(cell_xy, theme, callback, params):
            """ make_selection_button() - returns a created selection button.
            
            Create buttons and assign themes and center coords 
            by calculating its center from display center."""
            
            cell_x, cell_y = cell_xy
            
            # Get display size and display center.
            display_size = pygame.display.get_surface().get_size()
            display_center_pos = display_size[0]/2, display_size[1]/2
            
            cx = display_center_pos[0] + cell_x * (scale_size[0]/2 + 9)
            cy = display_center_pos[1] + cell_y * (scale_size[1]/2 + 9)
            print cx, cy
            selection_button = Button(panel)
            selection_button.theme = theme
            selection_button.rect.center = cx, cy
            
            selection_button.released(callback, params)
            
            return selection_button
        
        self.selection_button_list = ButtonGroup()
        
        # BUTTONS(THEMES):
        cell_xy = -1, -1
        callback, params = self.start_game, ((8, 8), 10)
        _8x8_selection_button = make_selection_button(cell_xy, _8x8_selection_theme, callback, params)
        self.selection_button_list.add(_8x8_selection_button)
        
        cell_xy =  1, -1
        callback, params = self.start_game, ((16, 16), 40)
        _16x16_selection_button = make_selection_button(cell_xy, _16x16_selection_theme, callback, params)
        self.selection_button_list.add(_16x16_selection_button)
        
        cell_xy = -1, 1
        callback, params = self.start_game, ((16, 30), 99)
        _30x16_selection_button = make_selection_button(cell_xy, _30x16_selection_theme, callback, params)
        self.selection_button_list.add(_30x16_selection_button)
        
        cell_xy = 1, 1
        callback, params = self.switch_screen, (CUSTOM_SCREEN, )
        _custom_selection_button = make_selection_button(cell_xy, _custom_selection_theme, callback, params)
        self.selection_button_list.add(_custom_selection_button)
        
        # FIXME: END TRASH.
        
    #init_custom_screen
    ######################################################################
    def init_custom_screen(self):
    
        panel = self.custom_screen_panel = Panel()
        
        dheight, dwidth = pygame.display.get_surface().get_size()
        
        cx, cy = dheight/2, dwidth/2
        
        self.custom_screen_sprite_list = TextField()
        
        digits = [str(i) for i in range(0, 10) ]
        
        size = pygame.display.get_surface().get_size()
        
        # Row inputfield.
        row = TextFieldSingleLine(panel, "16")
        row.set_name("row")
        row.set_max_char_length(4)
        row.rect.center = cx, cy - 50
        row.set_allowed_chars(digits)
        row.rect.centerx = size[0]/2 + row.rect.width/2 
        self.custom_screen_sprite_list.add(row)
        
        # Row text.
        row_text = TextLine(font = "Serif", text="Row :  ")
        row_text.text_color= 75, 75, 75
        row_text.rect.center = size[0]/2 - (row_text.rect.width)/2, size[1]/2 - 50
        
        # Col text.
        col_text = TextLine(font = "Serif", text="Col :  ")
        col_text.text_color= 75, 75, 75
        col_text.rect.center = size[0]/2 - (col_text.rect.width)/2, size[1]/2 - 20
        
        # Col inputfield.
        col = TextFieldSingleLine(panel, "16")
        col.rect.y += 30*1
        col.set_name("col")
        col.set_max_char_length(4)
        col.rect.center = cx, cy - 20
        col.set_allowed_chars(digits)
        self.custom_screen_sprite_list.add(col)
        col.rect.centerx = size[0]/2 + col.rect.width/2
        
        coverage_text = TextLine(font = "Serif", text="Mine % : ")
        coverage_text.text_color= 75, 75, 75
        coverage_text.rect.center =size[0]/2-(coverage_text.rect.width)/2, size[1]/2 +15
        
        # MIne count inputfield.
        coverage = TextFieldSingleLine(panel, "16")
        coverage.rect.y += 30*2
        coverage.set_name("coverage")
        coverage.set_max_char_length(4)
        coverage.rect.center = cx, cy + 15
        coverage.set_allowed_values([str(i) for i in range(1, 100)])
        self.custom_screen_sprite_list.add(coverage)
        coverage.rect.centerx = size[0]/2 + coverage.rect.width/2 
        
        self.custom_screen_sprite_list.returned(self.parase_value_to_start_game,\
                                                (self.custom_screen_sprite_list,))
            
        self.text_list = row_text, col_text, coverage_text
        
    def parase_value_to_start_game(self, obj):
        
        values = obj.get_values()
        
        coverage = int(values["coverage"])
        row, col = int(values["row"]), int(values["col"])
        
        mine_count = (coverage * row * col)/100
        print mine_count
        self.start_game((row, col), mine_count)
        
    ######################################################################
    # Used as callbacks.
    def switch_to_change_difficulty_screen(self):
        self.switch_screen(SELECTION_SCREEN)
        
    def start_game(self, mine_size, mine_count):
        
        # TODO: Change generate_tiles to start_game.
        
        self.TileGroup.generate_tiles(mine_size, mine_count)
        self.switch_screen(GAME_SCREEN)
        
        print "Game Started"
        
    ######################################################################
    #Setter and mutator.
    def switch_screen(self, new_screen_info):
        """switch_screen() - 
        
        will set screen size during start of the game. 
        Will reset screen size to upon endgame. 
        Disable the previous panel and enabled the new one."""
    
        #Don't change if is the same screen.
        if self.screen_info == new_screen_info:
            return
        
        # Disable old screen panel.
        
        if self.screen_info == GAME_SCREEN:
            self.game_screen_panel.disable()
            
            # Restting of screen to original size is required upon endgame.
            # Reset to default screen size if display size don't match.
            
            if pygame.display.get_surface().get_size() == SCREEN_SIZE:
                pass
            else:
                self.g.graphics_engine.set_screen_size(SCREEN_SIZE)
            
        elif self.screen_info == SELECTION_SCREEN:
            self.selection_screen_panel.disable()
            
        elif self.screen_info == CUSTOM_SCREEN:
            self.custom_screen_sprite_list.disable()
            
        # Enable all new screen panel.
        
        if new_screen_info == GAME_SCREEN:
            self.game_screen_panel.enable()
            
            # If desired size is same as current screen size, do not change.
            
            size = self.TileGroup.get_screen_size_requirement()
            
            if not (pygame.display.get_surface().get_size() == size):
                self.g.graphics_engine.set_screen_size(size)
            
        elif new_screen_info == SELECTION_SCREEN:
            self.selection_screen_panel.enable()
            
        elif new_screen_info == CUSTOM_SCREEN:
            self.custom_screen_panel.enable()
        
        self.screen_info = new_screen_info
        
    ######################################################################
    # Automatic methods. -DONE
    def load(self, loadobj):
        pass
        
    def handle_event(self, events):
        """Passes events to the selected screen panels.
        
        USES:
            Panel.update(events)
        """
        
        screen_info = self.screen_info 
        
        if screen_info == GAME_SCREEN:
            self.game_screen_panel.update(events)
            return
        
        if screen_info == SELECTION_SCREEN:
            self.selection_screen_panel.update(events)
            return
        
        if screen_info == CUSTOM_SCREEN:
            self.custom_screen_panel.update(events)
            return
    
    def update(self):
        """Does nothing currently because this is an event driven program."""
        pass
        
    def draw(self, surface):
        """draw() - Draws the selected screen group
        
            sprite.Group()          -   screen
        TileGroup                   - GAME_SCREEN
        selection_button_list       - SELECTION_SCREEN
        custom_screen_sprite_list   - CUSTOM_SCREEN
        
        USES:
            TileGroup.draw(surface)
            
            selection_button_list.draw(surface)
            custom_screen_sprite_list.draw(surface)
        """
        
        screen_info = self.screen_info 
        
        if screen_info == GAME_SCREEN:
            
            self.TileGroup.draw(surface)
            return
        
        if screen_info == SELECTION_SCREEN:
            
            self.selection_button_list.draw(surface)
            return
        
        if screen_info == CUSTOM_SCREEN:
            
            self.custom_screen_sprite_list.draw(surface)
            
            for text in self.text_list:
                text.draw(surface)
            return
