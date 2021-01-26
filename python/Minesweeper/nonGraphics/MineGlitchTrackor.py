#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# MineGlitchTrackor.py

"""
    Note: All matrix errors should be tested here. 
"""

'''
                    2017-10-03
'''

class MineGlitchTrackor:
    def __init__(self):
        pass
        
    def check_squeeze(self, rc):
        top, bottom = 0, 0
        left, right = 0, 0
        r, c = rc
        #print  self.matrix
        # Check when tile is only having 0.
        if self.matrix[r][c]:
            return False
        
        left = 1 if c!=1 and self.matrix[r][c - 1] != 0 else left
        
        right = 1 if c!=8 and self.matrix[r][c + 1] != 0 else right

        top = 1 if r!=1 and self.matrix[r - 1][c] != 0 else top
        
        bottom = 1 if r!=8 and self.matrix[r + 1][c] != 0 else bottom
        
        if top and right:
            if not self.matrix[r - 1][c + 1]: # topright.
                return True
        if right and bottom:
            if not self.matrix[r + 1][c + 1]: # rightbottom.
                return True
        if bottom and left:
            if not self.matrix[r + 1][c - 1]: # botomleft.
                return True
        if left and top:
            if not self.matrix[r - 1][c - 1]: # lefttop.
                return True
        
        return False
        
    def check_bug_1(self, ):
        
        matrix = []
        self.matrix = self.mine_matrix
        
        for (r, row) in enumerate(self.matrix):
            for (c, col) in enumerate(row):
                if r in (0, 1) or c in (0, 1) or r in (len(self.matrix) - 1, \
                            len(self.matrix) - 2) or c in (len(row) - 1, len(row) - 2):
                            
                    continue
                if self.check_squeeze((r, c)):
                    return True
                    
    def track_all(self, mine_matrix):

        self.mine_matrix = mine_matrix

        if self.check_bug_1():
            return True

