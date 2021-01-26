# tile.py
from widgets.Button import Button, ButtonGroup
from TileEssentials import *
from nonGraphics.MineField import MinesField
from widgets.Text  import TextLine
from constants import *

#Tile
#    * mine_board
#    * tile_res
#    * pos
#    * vis
#    * con
#    
#    * tile_template
#    * flag_template
#    
#    set_number
#    
#    flag - flag state
#    
#    __init__
#    - adjust_rect()
#    # callback
#    - touched
#    # mutators
#    - refresh_theme()
#    - set_flag
#    - uncover_tile
#    - pop_tile
#    
#    set_pos

class Tile(Button):
    def __init__(self, panel, pos, tile_res, mine_board):
        
        Button.__init__(self, panel)
        
        self.mine_board = mine_board
        self.tile_res = tile_res
        self.pos = pos
        
        
        self.vis = "covered" #uncovered/covered.
        self.con = "norm"
        
        self.flag = NO_FLAG
        
        self.tile_template = dict()
        self.flag_template = dict()
        
        self.set_number("0")
        
        self.released(self.touched, ())
        self.right_clicked(self.set_flag, ())
        
        self.flag_template = self.tile_res.get_flag_template()
        self.adjust_rect()
        
    # Mutator.
    ##############################################################
    def adjust_rect(self):
        r, c = self.pos
        
        offset_x, offset_y = OFFSET_XY
        self.rect.x = (c * self.rect.width) + offset_x
        self.rect.y = (r * self.rect.height) + offset_y
        
    def refresh_theme(self):
        """refresh_theme() - Refreshes the theme if there is not flag."""
        if not self.flag:
            
            self.theme = self.tile_template[self.con][self.vis]
            
    def set_flag(self):
        """set_flag() - Switches between flags and adjusts rect.
        
        touched() will call this upon (on_)right_clicked()."""
        
        theme = None # Dot let this remain None.
        
        if self.vis == "uncovered" or self.con == "lost":
            return
        
        if self.flag == NO_FLAG:
            self.flag = RED_FLAG
            self.mine_board.flag_added()
            theme = self.flag_template["flag"][self.con]
            
        elif self.flag == RED_FLAG:
            self.flag = BLUE_FLAG
            self.mine_board.flag_removed()
            theme = self.flag_template["maybe"][self.con]
            
        elif self.flag == BLUE_FLAG:
            self.flag = NO_FLAG
            
            theme = self.tile_template[self.con][self.vis]

        self.theme = theme
        
        self.adjust_rect()
        
    
    def uncover_tile(self):
        """uncover_tile() - Uncovers the tile and reveals its contents.
        
        Also calling this will remove all set flags."""
        
        if self.flag == RED_FLAG:
            return
        
        # TODO: Merge these two - self.color_number in ("13", "12")
        if self.color_number == "13":
#            self.con = "lost"
            return
            
        elif self.color_number == "12":
            return
            
        self.vis = "uncovered"
        self.flag = NO_FLAG
        
        self.refresh_theme()
        
    def pop_tile(self):#after lost.
        
        self.con = "lost"
        
        if self.flag == RED_FLAG and (self.color_number == "13"):
            self.theme = self.flag_template["flag"][self.con]
            return
            
        elif self.flag == RED_FLAG and not (self.color_number == "13"):
            self.theme = self.flag_template["incorrect"][self.con]
            return
        
        elif self.flag == BLUE_FLAG and not (self.color_number == "13"):
            self.theme = self.flag_template["maybe"][self.con]
            return
            
        elif self.flag == BLUE_FLAG and (self.color_number == "13"):
            self.flag = NO_FLAG
            
        if self.color_number in ("13", "12"):

            self.vis = "uncovered"
    
    # Callbacks.
    ##############################################################
    def touched(self):
        """Processing done after user presses a tile."""
        
        if self.mine_board.is_paused(): return
        
        # Red flags do nothing.
        
        if self.flag == RED_FLAG:
            return
        
        if self.vis == "uncovered" or self.con == "lost":
            return
        if not(self.color_number == MINES):
            self.mine_board.tile_touched(self)
            
            self.uncover_tile()
        else:
            print "Stepped on a mine at : ", self.pos
            self.mine_board.tile_blown(self)
    
    # Setters.
    ##############################################################
    # Used by TileGroup() class.
    
    def set_number(self, number):
        """The number is set here."""
        
        self.color_number = number
        self.tile_template = self.tile_res.get_number_template(number)
        
        self.refresh_theme()
        
    def set_pos(self, pos):
        self.pos = pos
        self.adjust_rect()

class TileGroup(ButtonGroup):
    def __init__(self, panel, timer):
        super(TileGroup, self).__init__()
        
        self.panel = panel
        self.Field = MinesField()
        self.timer = timer
        
        self.buffer_group = ButtonGroup()
        self.request_sprite_lock = False 
        self.sprite_lock = False
        
        self.tile_res = MineImages()
        
        self.set_size((8, 8))
        self.flag_count = 0
        self.set_mines(10)
        
        self.uncovered_list = pygame.sprite.Group()
        
        self.pause_screen = pygame.Surface((1, 1))
        self.pause_screen_rect = self.pause_screen.get_rect()
        
        self.touched_count = 0
        self.load()
        
        self.ghost_tile = Tile(panel, (-1, -1), self.tile_res, self)
        self.ghost_tile.kill()
        
    def load(self):
        from widgets import Timer
        
        self.tile_res.load_surfaces()
        
        self.flag_count_text = TextLine()
        self.flag_count_text.lable = "flag_count"
        self.flag_count_text.font_size = 22
        self.flag_count_text.text_color = (75, 75, 75)
        self.flag_count_text.text = "10"
        
        self.timer = Timer()
        
    def set_size(self, size):
        self.size = size
    
    def set_mines(self, mine_count):
        self.mine_count = mine_count
        
    def generate_tiles(self, size, mine_count):
        """generate_tiles() - Generates tiles."""
        
        self.set_size(size)
        self.set_mines(mine_count)
        self.reset()
        s_r, s_c = size
        
        print "Generating graphic tiles ", s_r, '*', s_c, '-', mine_count
        
        while self.request_sprite_lock:
            self.sprite_lock = False
            
        self.sprite_lock = True
        
        for r in range(s_r):
          for c in range(s_c):
            tile = Tile(self.panel, (r, c), self.tile_res, self)
            self.buffer_group.add(tile)
            
        self.adjust_option_button_placement()
        self.add(self.buffer_group)
        self.buffer_group.empty()
        self.sprite_lock = False
        
        # Adjust pause screen.
        ghost_tile = self.ghost_tile
        ghost_tile.set_pos((0, 0))
        x, y = ghost_tile.rect.x, ghost_tile.rect.y
        
        ghost_tile.set_pos((self.size[0] - 1, self.size[1] - 1))
        mwidth = ghost_tile.rect.x + ghost_tile.rect.width - x
        mheight = ghost_tile.rect.y + ghost_tile.rect.height - y
        self.pause.ready = True
        self.pause_screen = pygame.Surface((mwidth, mheight))
        self.pause_screen_rect = pygame.Rect((x, y, mwidth, mheight))
        self.pause_screen_rect.x = x
        self.pause_screen_rect.y = y
        self.pause_screen_rect.width = mwidth
        self.pause_screen_rect.height = mheight
        print "DONE"
        
    def get_screen_size_requirement(self):
        tile =  self.ghost_tile
        tile.set_pos((self.size[0] - 1, self.size[1] - 1))
        
        ex, ey = tile.rect.x + tile.rect.width, tile.rect.y + tile.rect.height #end cord
        
        offset_x, offset_y = OFFSET_XY
        ex += 194
        ey += 84
        
        if ex < 470: ex = 470
        if ey < 470: yx = 470
        size = ex, ey
        
        return size
        
    def assign_colored_numbers(self, mine_field):
        """Uses a mine_field array to assign colored numbers to tiles."""
        
        print "Assigning color to tiles."
        
        sprites = self.sprites()
        
        for tile in sprites:
            r, c = tile.pos
            tile.set_number(str(mine_field[r][c]))
        
    def get_tile_by_pos(self, tile_pos):
        sprites = self.sprites()
        
        for spr in sprites:
            if spr.pos == tile_pos:
                return spr
        
    def tile_touched(self, tile):
        """The player selected this tile."""
        #exit(1)
        touched_posxy = tile.pos
        
        print "Tile ", touched_posxy, "touched."
        
        # Generate matrix if for the first time.
        if not self.touched_count:
            
            # Generating matrix.
            self.Field.set_field((self.size[0], self.size[1]))
            self.Field.lay_mines(self.mine_count, touched_posxy)
            
            self.Field.debug_display()
            
            print self.Field.get_field()
            self.assign_colored_numbers(self.Field.get_field())
            print "All enabled"
            self.pause.enable()
            self.pause.ready = True
            self.start_over_b.enable()
            
            self.timer.start()
            
        # Now touch the tile.
        uncover_list = self.Field.touch_field(tile.pos)
        
        print "Uncovering the folowing tiles: ", uncover_list
        
        for tile_pos in uncover_list:
            temp_tile = self.get_tile_by_pos(tile_pos)
            temp_tile.uncover_tile()
            self.uncovered_list.add(temp_tile)
            
        self.touched_count += 1
        
        # Check whether player won.
        if self.mine_count == (self.size[0] * self.size[1]) - len(self.uncovered_list):

            self.victory_sequence()
        
    def tile_blown(self, tile):
        touched_posxy = tile.pos
        sprites = self.sprites()
        tile.set_number("12")
        print "Tile ", touched_posxy, "blown."
        
        mines_list = self.Field.get_all_mines()
        
        # Reveal all mines.
        for mine_pos in mines_list:
            mine_tile = self.get_tile_by_pos(mine_pos)
            mine_tile.pop_tile()
        
        grey_out = self.Field.get_all_unused()
        print "grey" , grey_out
        for tile_pos in grey_out:
            searched_tile = self.get_tile_by_pos(tile_pos)
            searched_tile.set_number(0)
            
            self.get_tile_by_pos(tile_pos).pop_tile()
            
        for tile in sprites:
            tile.refresh_theme()
        
    def start_over(self):
        print "start_over"
        
        
        self.request_sprite_lock = True
        
        while self.sprite_lock == False:
        
            self.sprite_lock = True
        self.request_sprite_lock = False
        
        self.reset()
        self.generate_tiles(self.size, self.mine_count)
        self.sprite_lock = False
        
    def reset(self):
        sprites = self.sprites()
        self.start_over_b.disable()
        self.pause.disable()
        self.flag_count = 0
        self.touched_count = 0
        self.timer.reset()
        self.resume.ready = False
        self.resume.disable()
        self.Field.reset_minefield()
#        self.empty()
        
        for spr in sprites:
            spr.kill()
            del spr
        
#    def on_screen_change(self, callback):
#        self.screen_change_callback = callback
        
    def disable(self):
        ButtonGroup.disable(self)
        self.empty()
        self.option_buttons_list.disable()
        
    def attatch_option_buttons(self, option_buttons_list):
        self.option_buttons_list = option_buttons_list
        
        self.change_difficulty_b = self.find_option_button_by_label("change_difficulty")
        self.pause = self.find_option_button_by_label("pause")
        self.resume = self.find_option_button_by_label("resume")
        self.start_over_b = self.find_option_button_by_label("start_over")
        
        self.flag_sprite = self.find_option_button_by_label("flag")
        self.clock_sprite = self.find_option_button_by_label("clock")
        
        self.resume.ready = False
        self.pause.clicked(self.pause_timer, ())
        self.resume.clicked(self.resume_timer, ())
    def pause_timer(self):
        self.resume.enable()
        self.pause.disable()
        self.pause.ready = False
        self.resume.ready = True
        self.timer.pause()
        self.timer.pause()
        
    def resume_timer(self):
        self.pause.enable()
        self.resume.disable()
        self.pause.ready = True
        self.resume.ready = False
        self.timer.resume()
        
    def adjust_option_button_placement(self):
        tile =  self.ghost_tile
        tile.set_pos((self.size[0] - 1, self.size[1] - 1))
        
        
        x, y = tile.rect.x + tile.rect.width, tile.rect.y + tile.rect.height #end cord
        x += 21
        y -= (7 + self.pause.rect.height)
        self.pause.rect.x, self.pause.rect.y = x, y
        
        y -=  self.pause.rect.height
        self.change_difficulty_b.rect.x, self.change_difficulty_b.rect.y = x, y
        
        y -=  self.pause.rect.height
        self.start_over_b.rect.x, self.start_over_b.rect.y = x, y
        
#        self.resume.rect = self.pause.rect
        
        tile.set_pos((0, 0))
        cx = x + self.start_over_b.rect.width/2
        y =  tile.rect.y
        self.flag_sprite.rect.centerx = cx 
        self.flag_sprite.rect.y = y
        
        self.flag_modfied()
        self.timer_modified()
        
    def find_option_button_by_label(self, label):
        for button in self.option_buttons_list:
            if button.label == label:
                return button
    def victory_sequence(self):
        self.start_over()
    
    def timer_modified(self):
        pass
    
    
    def flag_added(self):
        self.flag_count += 1
        self.flag_modfied()
        
    def flag_removed(self):
        self.flag_count -= 1
        self.flag_modfied()
        
    def flag_modfied(self):
        self.flag_count_text.text = str(self.flag_count) + "/" + str(self.mine_count)
        
        
        y = self.flag_sprite.rect.y + self.flag_sprite.rect.height + 4
        centerx = self.flag_sprite.rect.x + self.flag_sprite.rect.width/2 - 2
        
        self.flag_count_text.rect.y, self.flag_count_text.rect.centerx = y, centerx
        
    def is_paused(self):
        return False if (not self.timer.is_paused()) or not self.touched_count else True
        
    def draw(self, surface):
        
        self.option_buttons_list.draw(surface)
        
        # If not paused or not touched.
        if not self.is_paused():
            ButtonGroup.draw(self, surface)
        
        else: surface.blit(self.pause_screen, self.pause_screen_rect)
        self.flag_count_text.draw(surface)
            
