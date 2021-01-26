import pygame

import widgets
import config
from widgets.Button import create_button_theme
from widgets.Text import TextLine
from ChessEssentials import ChessEssentials
from nonGui.ChessMatrix import ChessMatrix
from nonGui.ChessRules import ChessRules
from constants import *

def get_color(color):
    return "White" if color == 'l' else "Black"
    
def get_piece_name(piece):
    if piece == 'p': return "Pawn"
    if piece == 'K': return "King"
    if piece == 'Q': return "Queen"
    if piece == 'B': return "Bishop"
    if piece == 'N': return "Knight"
    if piece == 'R': return "Rook"

class ChessTile(widgets.Button):
    def __init__(self, board, starting_piece, r, c, res, panel=None):
        widgets.Button.__init__(self, panel)
        
        self.board = board
        self.resource = res
        
        self.tile_color = config.color1 if (r + c)%2 else config.color2 
        
        self.chess_square_tuple = r, c
        self.state = IDLE
        
        # Declare rect.
        self.rect = pygame.Rect((0, 0, 0, 0))
        self.rect.center = self.convert_to_screen_coords((r, c))
        
        self.piece_img = None
        self.piece = starting_piece
        
        # Now get image from resource.
        self.refresh_theme()
        
    def refresh_theme(self): 
    
        self.theme = self.resource.get_tile_theme(self.chess_square_tuple, self.state)
        self.rect.center = self.convert_to_screen_coords(self.chess_square_tuple)
        
        self.piece_img = self.resource.get_piece(self.piece)
        
    def set_piece(self, piece): 
        self.piece = piece
        
        self.refresh_theme()
        
    def set_state(self, state): 
        if state == POINT:
            self.state = POINT_FREE if self.piece == 'e' else POINT_CAPTURE
            
        self.state = state if state!=POINT else \
                                    (POINT_FREE if self.piece=='e' else POINT_CAPTURE)
        self.refresh_theme()
        
    @staticmethod
    def convert_to_screen_coords(chess_square_tuple): 
		row, col = chess_square_tuple
		screen_x = config.board_start_x + col*config.square_size + config.square_size/2
		screen_y = config.board_start_y + row*config.square_size + config.square_size/2
		return screen_x, screen_y
        
    def on_clicked(self): 
        widgets.Button.on_clicked(self)
        
        self.board.touched(self)
        
    def draw(self, surface): 
        widgets.Button.draw(self, surface)
        
        # Now draw the piece.
        surface.blit(self.piece_img, (self.rect.x, self.rect.y))
        
class ChessBoard(widgets.ButtonGroup):
    def __init__(self, chess_obj, panel =None, setup=0, pre_matrix=None,turn_count=0):
        widgets.ButtonGroup.__init__(self)
        
        self.panel = panel
        
        self.resource = ChessEssentials()
        self.chess_matrix = ChessMatrix(setup, pre_matrix)
        
        self.chess_obj = chess_obj
        
        self.text_box = chess_obj.text_box
        self.text_box.post("")
        
        self.init_board()
        self.init_chess_tiles()
        self.init_chess_letters()
        
        self.selected_chess_tile = None
        self.pointed_chess_squares = []
        self.pointed_chess_tiles = []
        
        self.turn = 'l'
        self.turn_count = turn_count
        
        self.started = False
        
        self.player = {
            "name":{
                'l' : "Player1",
                'd' : "Player2"
            },
            "color":{
                'l' : "White",
                'd' : "Black"
            }
        }
        
        self.max_turns = 0 # 0 means infinity
        self.max_turns = 1
        self.text_box.post(self.get_turn_msg())
        
        
    def init_board(self): 
        pass
        
    def init_chess_letters(self):
        """init letters that appear around the chess board."""
        
        convert_to_screen_coords = ChessTile.convert_to_screen_coords
        
        ua = TextLine(text = "a")
        ua.rect.center = convert_to_screen_coords((-1, 0))
        ub = TextLine(text = "b")
        ub.rect.center = convert_to_screen_coords((-1, 1))
        uc = TextLine(text = "c")
        uc.rect.center = convert_to_screen_coords((-1, 2))
        ud = TextLine(text = "d")
        ud.rect.center = convert_to_screen_coords((-1, 3))
        ue = TextLine(text = "e")
        ue.rect.center = convert_to_screen_coords((-1, 4))
        uf = TextLine(text = "f")
        uf.rect.center = convert_to_screen_coords((-1, 5))
        ug = TextLine(text = "g")
        ug.rect.center = convert_to_screen_coords((-1, 6))
        uh = TextLine(text = "h")
        uh.rect.center = convert_to_screen_coords((-1, 7))
        
        da = TextLine(text = "a")
        da.rect.center = convert_to_screen_coords((8, 0))
        db = TextLine(text = "b")
        db.rect.center = convert_to_screen_coords((8, 1))
        dc = TextLine(text = "c")
        dc.rect.center = convert_to_screen_coords((8, 2))
        dd = TextLine(text = "d")
        dd.rect.center = convert_to_screen_coords((8, 3))
        de = TextLine(text = "e")
        de.rect.center = convert_to_screen_coords((8, 4))
        df = TextLine(text = "f")
        df.rect.center = convert_to_screen_coords((8, 5))
        dg = TextLine(text = "g")
        dg.rect.center = convert_to_screen_coords((8, 6))
        dh = TextLine(text = "h")
        dh.rect.center = convert_to_screen_coords((8, 7))
        
        l_num_1 = TextLine(text = "1")
        l_num_1.rect.center = convert_to_screen_coords((0, -1))
        l_num_2 = TextLine(text = "2")
        l_num_2.rect.center = convert_to_screen_coords((1, -1))
        l_num_3 = TextLine(text = "3")
        l_num_3.rect.center = convert_to_screen_coords((2, -1))
        l_num_4 = TextLine(text = "4")
        l_num_4.rect.center = convert_to_screen_coords((3, -1))
        l_num_5 = TextLine(text = "5")
        l_num_5.rect.center = convert_to_screen_coords((4, -1))
        l_num_6 = TextLine(text = "6")
        l_num_6.rect.center = convert_to_screen_coords((5, -1))
        l_num_7 = TextLine(text = "7")
        l_num_7.rect.center = convert_to_screen_coords((6, -1))
        l_num_8 = TextLine(text = "8")
        l_num_8.rect.center = convert_to_screen_coords((7, -1))
        
        r_num_1 = TextLine(text = "1")
        r_num_1.rect.center = convert_to_screen_coords((0, 8))
        r_num_2 = TextLine(text = "2")
        r_num_2.rect.center = convert_to_screen_coords((1, 8))
        r_num_3 = TextLine(text = "3")
        r_num_3.rect.center = convert_to_screen_coords((2, 8))
        r_num_4 = TextLine(text = "4")
        r_num_4.rect.center = convert_to_screen_coords((3, 8))
        r_num_5 = TextLine(text = "5")
        r_num_5.rect.center = convert_to_screen_coords((4, 8))
        r_num_6 = TextLine(text = "6")
        r_num_6.rect.center = convert_to_screen_coords((5, 8))
        r_num_7 = TextLine(text = "7")
        r_num_7.rect.center = convert_to_screen_coords((6, 8))
        r_num_8 = TextLine(text = "8")
        r_num_8.rect.center = convert_to_screen_coords((7, 8))
        
        self.text_list = []
        self.text_list += [ua, ub, uc, ud, ue, uf, ug, uh, da, db, dc, dd, de, df,dg,dh]
        self.text_list += [l_num_1, l_num_2, l_num_3, l_num_4, \
                            l_num_5, l_num_6, l_num_7, l_num_8,\
                            r_num_1, r_num_2, r_num_3, r_num_4, \
                            r_num_5, r_num_6, r_num_7, r_num_8]
        
    def init_chess_tiles(self):
        ress = self.resource
        
        piece = "e"
        
        squares = self.chess_matrix.get_squares()
        
        for r in range(8):
            for c in range(8): 
                self.add(ChessTile(self, piece, r, c, ress, self.panel))
        
        self.apply_changes_to_chess_tiles()
        
    def get_turn_msg(self):
        plyr_name = self.player["name"][self.turn]
        plyr_color = self.player["color"][self.turn]
        
        msg = "TURN {} - {} ({})" .format(str(self.turn_count), plyr_name, plyr_color)
        return "-----%s-----" % msg
        
    def apply_changes_to_chess_tiles(self):
        
        sprites = self.sprites()
        squares = self.chess_matrix.get_squares()
        
        for spr in sprites:
            x, y = spr.chess_square_tuple
            spr.set_state(IDLE)# TROUBLE HERE.
            spr.set_piece(squares[x][y])
    
    def search_chess_tile(self, square):
        
        sprites = self.sprites()
        for spr in sprites:
            if spr.chess_square_tuple == square: return spr
    
    def set_changed_to_idle(self):
        # Chenge every selected and pointed tiles to idle tile.
        
        pointed_squares = self.pointed_chess_squares[:]
        
        tile  = self.selected_chess_tile
        
        self.selected_chess_tile = None
        self.pointed_chess_squares = []
        
        tile.set_state(IDLE)
        for pointed_square in pointed_squares:
            self.search_chess_tile(pointed_square).set_state(IDLE)
        
    def select_tile(self, tile):
        moves = self.chess_matrix.get_available_moves(tile.chess_square_tuple)
        
        tile.set_state(SELECTED)
        
        [self.search_chess_tile(square).set_state(POINT) for square in moves]
        
        self.selected_chess_tile = tile
        
        self.pointed_chess_squares = moves
        tile.set_state(SELECTED)
    
    def force_move(self, from_tile, to_tile):
        
        if self.max_turns and self.max_turns < self.turn_count:
            return
        
        f_color, f_piece = get_color(from_tile.piece[0]), get_piece_name(from_tile.piece[1])
        f_pos, t_pos = from_tile.chess_square_tuple, to_tile.chess_square_tuple
        
        capture_text = ""
        if not (to_tile.piece == 'e'):
            capture_text = " and captures {}".format(to_tile.piece)
        
        T_ =  "{} {} moves from {} to {} {}"
        moveReport = T_.format(f_color, f_piece, f_pos, t_pos, capture_text)
        
        to_tile.set_piece(from_tile.piece)
        from_tile.set_piece("e")
        
        self.chess_matrix.force_move(from_tile.chess_square_tuple, to_tile.chess_square_tuple)
        self.turn = 'd' if self.turn == 'l' else 'l'
        
        plyr_name = self.player["name"][self.turn]
        plyr_color = self.player["color"][self.turn]
        
        self.turn_count += 1
        
        self.text_box.post(moveReport)
        
        self.text_box.post((" "))
        msg = "TURN {} - {} ({})" .format(str(self.turn_count), plyr_name, plyr_color)
        self.text_box.post(("-----%s-----" % msg))
        
        
        name = self.player['name'][self.turn]
        color = self.player['color'][self.turn]
        board = self.chess_matrix.squares
        
        if ChessRules.isCheckMate(board, 'l') or ChessRules.isCheckMate(board, 'd'):
            checkmate_msg = "Checkmate : Player {}({}) lost!.".format(name, color)
            self.text_box.post(checkmate_msg)
            
        
        elif ChessRules.testCheck(board, 'l') or ChessRules.testCheck(board, 'd'):
            check_msg = "Warning -- {}({}) is in check!".format(name, color)
            self.text_box.post(check_msg)
            
        elif self.max_turns and self.max_turns < self.turn_count:
            draw_msg = "Draw ! PLease Click Reset Game to continue.".format(name, color)
            self.text_box.post(draw_msg)
        
    def free_touched(self, tile):
    
        sel_tile, pointed_sqr = self.selected_chess_tile, self.pointed_chess_squares
        
        if self.selected_chess_tile:
            self.set_changed_to_idle()
            self.force_move(sel_tile, tile)
        
        elif tile.piece == 'e': return
        
        else:
            self.selected_chess_tile = tile
            self.select_tile(tile)
            
    def touched(self, tile):
        
        print "Selected :", tile.chess_square_tuple
        
        if self.max_turns and self.max_turns < self.turn_count:
            return
        
        # NOTE: New Feature!
        if self.chess_obj.free_move:   
            self.free_touched(tile)
            return
            
        if not self.started: 
            self.started = True
            
            self.reset_text_box()
            
            self.chess_obj.switch_screen(GAME_SCREEN)
            self.chess_obj.start_game()
            
        sel_tile, pointed_sqr = self.selected_chess_tile, self.pointed_chess_squares
        
        # If current pressed tile is one of the previous selected tile's moves.
        if tile.chess_square_tuple in self.pointed_chess_squares:
            self.set_changed_to_idle()
            self.force_move(sel_tile, tile)
            
            return
            
        elif not (tile.piece) == 'e' and not (tile.piece[0] == self.turn) : return
        
        # If any chess square was previously selected on board, and
        # if there requires no piece movement.
        if self.selected_chess_tile:
            
            self.set_changed_to_idle()
            
            # Check if current clicked tile coincides with selected tile.
            if tile == sel_tile: pass
            
            else:  self.select_tile(tile)
                
        else:  self.select_tile(tile)
        
    def reset(self):
        self.chess_matrix.reset()
        
        if self.selected_chess_tile: self.set_changed_to_idle()
        
        self.apply_changes_to_chess_tiles()
        
        self.started = False
        self.turn = 'l'
        self.reset_text_box()
        
    def reset_text_box(self):
        self.turn_count = 0
        self.text_box.clear()
        self.text_box.post(self.get_turn_msg())
        
    # Used by displayengine(GraphicsEngine).
    def draw(self, surface):
        sprites = self.sprites()
        
        for spr in sprites:
            spr.draw(surface)
        
        text_list = self.text_list
        
        for txt in text_list:
            txt.draw(surface)
        
