# MinesField.py
from nonGraphics.Helper import append_nonduplicates, list2d
from nonGraphics.MineShuffle import MinesShuffle
from nonGraphics.MineGlitchTrackor import MineGlitchTrackor

#MinesField
#    __init__
#    set_field
#    lay_mines
#    reset
#    reset_minefield
#    
#    increment_value_around_tile
#    __place_all_mines_and_colored_numbers_to_field
#    
#    adjust_field
#    touch_field
#    
#    get_neighbouring_blank_tiles
#    get_all_neighbouring_tiles
#    
#    get_tiles_to_reveals
#    get_all_unused
#    get_field
#    get_all_mines
#    
#    debug_display

class MinesField:
    def __init__(self):
        self.reset()
        
    ##################################################################
    # Setters.
    def set_field(self, size):
        """"""
        # Make it usable by the class.
        self.size = size
        
        # Create a 2d list.
        Tuple2, value = (size[0] + 2, size[1] + 2), 0
        self.mine_field_original = list2d(Tuple2, value)
        self.mine_field_original_cropped = list2d(size, value)
    
    
    def lay_mines(self, NumberOfMines, startposxy):
      n = NumberOfMines
      
      startx, starty = startposxy
      
      while True:
        # Randomly select the locations where mines are placed.
        self.mine_locs = list(MinesShuffle().allocate_mines_randomly(self.size, NumberOfMines, startposxy))
        
        print self.mine_locs, "mine cords"
        
        # Override generated mine locations here.
        #self.mine_locs = [[0, 2], [5, 7], [7, 1], [5, 4], [2, 3], [4, 2], [3, 1], [3, 6], [2, 6]]
        
        # *squeeze problem rectified.
        
        # Make a mine_field out of the given mine locations.
        self.__place_all_mines_and_colored_numbers_to_field(self.get_all_mines())
        
        #break
        # Chech whether there is a fault in the mine_field.
        if not MineGlitchTrackor().track_all(self.mine_field_original):
            self.adjust_field()
            break
        else:
            self.set_field(self.size)
    
    # Mutators
    ##################################################################
    def adjust_field(self):
    
        self.mine_field_original_cropped = [x[:] for x in self.mine_field_original]
        
        # Removes first and last rows.
        del self.mine_field_original_cropped[0]
        del self.mine_field_original_cropped[-1]
        
        row = 0
        
        # Removes first and last columns.
        for i in self.mine_field_original_cropped:
            del self.mine_field_original_cropped[row][0]
            del self.mine_field_original_cropped[row][-1]
            row += 1
    
    def reset(self):
        self.mine_field_original = list2d()
        self.mine_locs = []
        
        self.accessed = set()
        
        # Data to not alter.
#        self.size
        
    # Used by TileGroup()
    def reset_minefield(self):
        self.reset()
        
    ##################################################################
    def increment_value_around_tile(self, Tuple):
      """Calculate labels."""
#      print Tuple
      (r, c) = Tuple
      r += 1
      c += 1
      self.mine_field_original[r-1][c-1] += 1
    
      self.mine_field_original[r][c-1] += 1
      self.mine_field_original[r+1][c-1] += 1
      self.mine_field_original[r-1][c] += 1
      self.mine_field_original[r+1][c] += 1
    
      self.mine_field_original[r-1][c+1] += 1
      self.mine_field_original[r][c+1] += 1
      self.mine_field_original[r+1][c+1] += 1
      
    def __place_all_mines_and_colored_numbers_to_field(self, mines_pos):
        # __place_all_mines_and_colored_numbers
        
        # Adjust lable around all mines
        # and then place mines.
#        print self.mine_locs
        for Tuple in self.mine_locs:
            self.increment_value_around_tile(Tuple)
            self.debug_display()
        
        # Place mines
        for Tuple in self.mine_locs:
            self.mine_field_original[Tuple[0] + 1][Tuple[1] + 1] = 13
        
        self.debug_display()

    ##################################################################
    def touch_field(self, touched_posxy):
    
        ret = self.get_tiles_to_reveal(touched_posxy)
        self.accessed |= set(ret)
        
        return ret
    
    ##################################################################
    def get_neighbouring_blank_tiles(self, Tuple):
        # __search_emptys_around_block
        # TODO: Needs to be modified.
        
        field_matrix = self.get_field()
        
        (r, c) = Tuple
        blanks = []
        if r>0 and field_matrix[r - 1][c] == 0:# top.
            blanks.append( (r - 1, c) )
        if r<self.size[0]-1 and field_matrix[r + 1][c] == 0:# bottom.
            blanks.append((r + 1, c))
        if c>0 and field_matrix[r][c - 1] == 0:# left.
            blanks.append((r, c - 1))
        if c<self.size[1]-1 and field_matrix[r][c + 1] == 0:# right.
            blanks.append((r, c + 1))
        return blanks
    
    def get_all_neighbouring_tiles(self, Tuple):
        """Yields all the tile positions that are around a tile."""
        
        # Equivalant to __search_nomines_around_block in v1.0.
        
        (r, c) = Tuple
        if not (c == 0):
            yield (r, c - 1)
        if not (c == self.size[1]-1):
            yield (r, c + 1)
        if not (r == 0):
            yield (r-1, c)
        if not (r == self.size[0]-1):
            yield (r+1, c)
        if not (c == 0) and not (r == 0): # TOPLEFT.
            yield (r - 1, c - 1)
        if not (c == self.size[1]-1) and not (r == self.size[0]-1): # BOTTOMRIGHT.
            yield (r + 1, c + 1)
        if not (c == self.size[1]-1) and not (r == 0): # BOTTOMLEFT.
            yield (r - 1, c + 1)
        if not (c == 0) and not (r == self.size[0]-1): # TOPRIGHT.
            yield (r + 1, c - 1)
        return
    
    ################################################
    def get_tiles_to_reveal(self, Tuple):
        """Generates all tiles that needs to be revealed."""
        
        # Equivalant to __search_nonmines in v1.0.
        colored_numbers = set()
        (r, c) = Tuple
        
        field_matrix = self.get_field()
        
        if field_matrix[r][c]:
            return [Tuple]
            
        blank_tiles = [Tuple]
        
        # Gets colored numbers and blank tiles seperately.
        
        for b_tile in blank_tiles:
            blank_tiles += list(set(self.get_neighbouring_blank_tiles(b_tile)) - set(blank_tiles))
            
            colored_numbers |= set(self.get_all_neighbouring_tiles(b_tile))
        return list(colored_numbers | set(blank_tiles))
    
    def get_all_unused(self):
        list_ = []
        for r in range(self.size[0]):
            for c in range(self.size[1]):
                list_.append((r, c))
        return set(list_ ) - (self.accessed | set(self.get_all_mines()))
        
    ################################################
    def get_field(self):
        """Returns the entire field."""
        
        return self.mine_field_original_cropped
        
    def get_all_mines(self):
        """Returns all the mine locations"""
        
        return self.mine_locs
    
    def debug_display(self):
        display = ""

        for row in self.mine_field_original:
            for col in row: 
                display += "{:3}".format(str(col))
            display += "\n"
