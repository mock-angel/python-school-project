#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
 *
 * Authors: Anantha Krishna R
 *
"""

'''
                    2017-12-26
'''


class ChessRules():
    def __init__(self):
        pass
    def getListOfLegalMoves(self, getBoard, getTeamColor, fromTuple, toTuple):
        for row in range(8):
            for col in range(8):
                toTuple = row, col
                yield self.IsItLegal(getBoard, getTeamColor, fromTuple, toTuple)
        
    def IsItLegal(self, BoardMatr, ColorMatr, fromTuple, toTuple):
        """Checks wheter a move is legal."""
        
        from_r = fromTuple[0]
        from_c = fromTuple[1]
        to_r = toTuple[0]
        to_c = toTuple[1]
        
        
        fromColor = self.CheckColorFromPosition(ColorMatr, fromTuple)
        toColor = self.CheckColorFromPosition(ColorMatr, toTuple)
        
        if fromColor == toColor:
            pass
        else:
            # Check starts from here(for p, then K, Q, R, B, N)
            
            if "p" in BoardMatr[from_r][from_c]:
                if (from_r - to_r == 1)  and (from_c - to_c == 0) and (toColor == None) :
                  return True
                if (from_r - to_r == 1) and (from_c - to_c == -1 or from_c - to_c == 1) and (not (toColor == None) ):
                  return True
                 
                  
            if 'K' in BoardMatr[from_r][from_c]:
                if (from_r - to_r == 1)  and (from_c - to_c == 0):
                    return True
                if (from_r - to_r == 1)  and (from_c - to_c == -1):
                    return True
                if (from_r - to_r == 1)  and (from_c - to_c == 1):
                    return True
                if (from_r - to_r == 0)  and (from_c - to_c == -1):
                    return True
                if (from_r - to_r == 0)  and (from_c - to_c == 1):
                    return True
                if (from_r - to_r == -1)  and (from_c - to_c == 0):
                    return True
                if (from_r - to_r == -1)  and (from_c - to_c == -1):
                    return True
                if (from_r - to_r == -1)  and (from_c - to_c == -1):
                    return True
                    
            if 'Q' in BoardMatr[from_r][from_c]:
                if self.IsItLegalInPlusLine( ColorMatr, fromTuple, toTuple):
                    return True
                if self.IsItLegalInCrossLine( ColorMatr, fromTuple, toTuple):
                    return True
                else:
                    return False
                    
            if 'R' in BoardMatr[from_r][from_c]:
                if self.IsItLegalInPlusLine( ColorMatr, fromTuple, toTuple):
                    return True
                else:
                    return False
                    
            if 'B' in BoardMatr[from_r][from_c]:
                if self.IsItLegalInCrossLine( ColorMatr, fromTuple, toTuple):
                    return True
                else:
                    return False
                    
            if 'N' in BoardMatr[from_r][from_c]:
                if (from_r + 2 == to_r and ( (from_c + 1 == to_c) or (from_c - 1 == to_c) ) ):
                    return True
                if (from_r - 2 == to_r and ( (from_c + 1 == to_c) or (from_c - 1 == to_c) ) ):
                    return True
                if (from_c + 2 == to_c and ( (from_r + 1 == to_r) or (from_c - 1 == to_r) ) ):
                    return True
                if (from_c + 2 == to_c and ( (from_r + 1 == to_r) or (from_c - 1 == to_r) ) ):
                    return True
        return False
        
        
    def checkColorFromPosition(self, ColorMatr, Tuple):
#        print Tuple
#        for i in ColorMatr:
#            print i
        r, c = Tuple[0], Tuple[1]
        if ColorMatr[r][c] == "e":
            return None # 
        if ColorMatr[r][c] == "W":
            return "white"
        if ColorMatr[r][c] == "B":
            return "black"

            
    def isItLegalInPlusLine(self, ColorMatr, fromTuple, toTuple):
        """IsItLegalInPlusLine() returns True or False.
        
        Checks whether a move is possible witout interception along 
        the vertical and horizontal lines of a chessboard.
        
        Applicable for Q and R units."""
        
        from_r = fromTuple[0]
        from_c = fromTuple[1]
        to_r = toTuple[0]
        to_c = toTuple[1]
        r = from_r
        c = from_c
        ColorTuple = (r, c)
        fromColor = self.CheckColorFromPosition(ColorMatr, fromTuple)
        toColor = self.CheckColorFromPosition(ColorMatr, toTuple)
        CurrentColor = self.CheckColorFromPosition(ColorMatr, ColorTuple)
        
        TupleArray = []
        
        # Check whether move belongs to the same row as that of the
        # selected piece.
        if from_r == to_r:
          # TODO: Simplify lines of code into method().
            # Checks whether it needs to look up or down in the color Board.
            operation = 0
            
            if from_c < to_c:
                operation = (+1)
            if from_c > to_c:
                operation = (-1)
                
            while (c >= 0 and c <= 7):
                c = c + operation
                if not (c >= 0 and c <= 7):
                    break
                ColorTuple = (r, c)
                CurrentColor = self.CheckColorFromPosition(ColorMatr, ColorTuple)
                if CurrentColor == None:
                    TupleArray += [[r, c]]
                elif CurrentColor == fromColor:
                    break
                elif not(CurrentColor == fromColor):# Switch to else
                    TupleArray += [[r, c]]
                    break
                    
        # If its nt part of the same row, then is it part of the 
        # same column?.
        elif from_c == to_c:
          # TODO: Simplify lines of code into method().
            # Checks whether it needs to look left or right in the color Board.
            operation = 0
            if from_r < to_r:
                operation = (+1)
            if from_r > to_r:
                operation = (-1)
            
            while not(r == to_r):
            
                r = r + operation
                ColorTuple = (r, c)
                CurrentColor = self.CheckColorFromPosition(ColorMatr, ColorTuple)
                if CurrentColor == None:
                    TupleArray += [(r, c)]
                elif CurrentColor == fromColor:
                    break
                elif not(CurrentColor == fromColor):# Switch to else
                    TupleArray += [(r, c)]
                    break
                    
        # If it neither belongs to the same column nor the same row
        # then method ends its turn.
        else:
            return False
                    
        if toTuple in TupleArray:
            return True
        
        return False
                
                
                
    def isItLegalInCrossLine(self, ColorMatr, fromTuple, toTuple):
        """IsItLegalInPlusLine() returns True or False.
        
        Applicable for Q and N."""
        
        from_r = fromTuple[0]
        from_c = fromTuple[1]
        to_r = toTuple[0]
        to_c = toTuple[1]
        r = from_r
        c = from_c
        ColorTuple = (r, c)
        fromColor = self.CheckColorFromPosition(ColorMatr, fromTuple)
        toColor = self.CheckColorFromPosition(ColorMatr, toTuple)
        CurrentColor = self.CheckColorFromPosition(ColorMatr, ColorTuple)
        
        diff_r = from_r - to_r
        diff_c = from_c - to_c
        TupleArray = []
        
        # Check whether move belongs to the same row or column as that of the
        # selected piece.
        
        if from_r == to_r or from_c == to_c:
            return False
            
        # If It reaches till here, then check whether they comes in the same line
        # diagonally.
        
        elif not (diff_r == diff_c):
            return False
        
        # If it neither belongs to the same column nor the same row
        # then method executes its main order.
        
        else:
          # TODO: Simplify lines of code into method().
            # Variables for conducting increment/decrement operations on row/column
            
            operationr = operationc = 0
            
            
            # Checks which direction on rows it needs to look in the color Board.
            
            if from_r < to_r:
                operationr = (+1)
            elif from_r > to_r:
                operationr = (-1)
            else:
                return False

            if from_c < to_c:
                operationc = (+1)
            elif from_c > to_c:
                operationc = (-1)
            else:
                return False
                
                
            # This loop Writes an array that contains Legal-diagonal-moves
            # by searching towards the desired move.
            
            while (c >= 0 and c <= 7):
            
                # Conduct operations.
                c = c + operationc
                r = r + operationr
                
                if not (c >= 0 and c <= 7):
                    break
                
                # Form tuple and get team color.
                
                ColorTuple = (r, c)
                CurrentColor = self.CheckColorFromPosition(ColorMatr, ColorTuple)
                
                # Test Color of selected element. Add to array if there is no unit,
                # break if the team is same or add and break if it finds an enemy.
                
                if CurrentColor == None:
                    TupleArray += [(r, c)]
                elif CurrentColor == fromColor:
                    break
                elif not(CurrentColor == fromColor):# else:
                    TupleArray += [(r, c)]
                    break

        # If move is available in generated array,
        # then method is successful.
        
        if toTuple in TupleArray:
            return True
        
        # Natural else.
        
        return False
    
    def getLegalMoves(self):
        """getLegalMoves() returns a list of board xy_coords that the player can move.
        
        """
        
        # TODO: Need to write this. 
        
        # TODO: Either check for all cells legality of try to simply define
        # and create a list.        
        
        
        
        
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
