#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# MineShuffle.py

'''
                    2017-10-03  MODULING
'''

import random

class MinesShuffle:
    def __init__(self):

        pass
        
    def check_mine_duplicate(self, MineCords):
        """check_mine_duplicate() - returns True if there is any mine over another mine."""
        
        # Equivalant to chk_similarity in v1.0
        # Checks whether there are 2 mines on the same loc.
        
        return not bool(len(set(MineCords)) == len(MineCords))
        
        # All mines are unique.
        
        # Disclaimer: Only returns True if there is another mine on 
        # the same location.
    
    def check_start_overlap(self, mine_cords, startxy):
        """check_start_overlap() - returns True if any mine is in the 
        reserved zone around the starting tile.
        
        Check whether any mine is in the safe location."""
        
        start = [tuple(startxy)]
        r, c = startxy
        
        start += [
            (r - 1, c - 1),
            (r - 1, c),
            (r - 1, c + 1),
            (r, c - 1),
            (r, c + 1),
            (r + 1, c - 1),
            (r + 1, c),
            (r + 1, c + 1)            
        ]
        
        # If both sets intersect, then there is a mine in the safe location.
        
        return bool(set(start) & set(mine_cords))

        # Disclaimer: Only returns 1 if there is a mine on 
        # the start location.
        
    def allocate_mines_randomly(self, Tuple, NumberOfMines, startxy):
        
        # Equivalant to randomize_mine_placement in v1.0
        # rand_mines needs to be written.
        
        self.NumberOfMines = NumberOfMines
        self.startxy = startxy
        
        tile_count = Tuple[0] * Tuple[1]
        li_ = range(tile_count)
        sample_list = random.sample(li_, NumberOfMines)
        
        
        rand_mines = []
        for sample in sample_list:
            rand_mines += [(sample/Tuple[1], sample % Tuple[1])]
        
        
        while True:
            
            sample_list = random.sample(li_, NumberOfMines)
        
            rand_mines = []
            for sample in sample_list:
                rand_mines += [(sample/Tuple[1], (sample % Tuple[1]))]
            
            if (self.check_mine_duplicate(rand_mines)
                    or self.check_start_overlap(rand_mines, startxy) ):
                continue
            else: 
                return rand_mines


