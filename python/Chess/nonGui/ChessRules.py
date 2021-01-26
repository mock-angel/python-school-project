#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# ChessRules.py
"""
    Authors: Anantha Krishna R
"""

'''
                    2017-12-26
'''

# TODO: Make all methods static.
class ChessRules():
    def __init__(self):
        pass
    
    @staticmethod
    def getListOfLegalMoves(ChessRules, getBoard, getTeamColor, fromTuple, toTuple):
        for row in range(8):
            for col in range(8):
                toTuple = row, col
                yield ChessRules.isItLegal(getBoard, getTeamColor, fromTuple, toTuple)
    
    @staticmethod
    def isItLegal(BoardMatr, ColorMatr, fromTuple, toTuple):
        """Checks wheter a move is legal."""
        
        from_r, from_c = fromTuple[0], fromTuple[1]
        to_r, to_c = toTuple[0], toTuple[1]
        r, c = from_r, from_c
        
        fromColor = ChessRules.getColorFromPosition(ColorMatr, fromTuple)
        toColor = ChessRules.getColorFromPosition(ColorMatr, toTuple)
        
        if fromColor == toColor: return False
        
        # Check starts from here(for p, then K, Q, R, B, N)
        
        if "p" in BoardMatr[from_r][from_c]: # Optimised.
            if fromColor == 'dark': 
                r_diff_match = -1
                double_move_row = 1
                
            if fromColor == 'light': 
                r_diff_match = 1
                double_move_row = 6
                
            r_diff = (from_r - to_r)
            c_diff_abs = abs(from_c - to_c)
            
            # Normal check.
            if (r_diff == r_diff_match)  and (c_diff_abs == 0) and (toColor == None) :
              return True
              
            if (r_diff == r_diff_match) and (c_diff_abs == 1) and not (toColor == None):
              return True
              
            # Check if its 2 moves at starting pos.
            if ((r_diff == r_diff_match*2) and (double_move_row == from_r) 
                and (c_diff_abs == 0) and (toColor == None) 
                and ChessRules.isItLegalInPlusLine(ColorMatr, fromTuple, toTuple)):
              return True
              
        if 'K' in BoardMatr[from_r][from_c]: # Optimised.
            r_diff_abs = abs(from_r - to_r)
            c_diff_abs = abs(from_c - to_c)
            if (r_diff_abs == 1)  and (c_diff_abs == 0):
                return True
            if (r_diff_abs == 1)  and (c_diff_abs == 1):
                return True
            if (r_diff_abs == 0)  and (c_diff_abs == 1):
                return True
                
        if 'Q' in BoardMatr[from_r][from_c]: # Optimised.
            if ChessRules.isItLegalInPlusLine( ColorMatr, fromTuple, toTuple):
                return True
            if ChessRules.isItLegalInCrossLine( ColorMatr, fromTuple, toTuple):
                return True
                
        if 'R' in BoardMatr[from_r][from_c]: # Optimised.
            if ChessRules.isItLegalInPlusLine( ColorMatr, fromTuple, toTuple):
                return True
                
        if 'B' in BoardMatr[from_r][from_c]: # Optimised.
            if ChessRules.isItLegalInCrossLine( ColorMatr, fromTuple, toTuple):
                return True
                
        if 'N' in BoardMatr[from_r][from_c]: # Optimised.
            r_diff_abs = abs(from_r - to_r)
            c_diff_abs = abs(from_c - to_c)
            
            if r_diff_abs == 2 and c_diff_abs == 1:
                return True
            if c_diff_abs == 2 and r_diff_abs == 1:
                return True
        return False
        
    @staticmethod
    def getColorFromPosition(ColorMatr, Tuple):
    
        r, c = Tuple[0], Tuple[1]
        if ColorMatr[r][c] == None:
            return None
        if ColorMatr[r][c] == "l":
            return "light"
        if ColorMatr[r][c] == "d":
            return "dark"

    @staticmethod
    def isItLegalInPlusLine(ColorMatr, fromTuple, toTuple):
        """isItLegalInPlusLine() returns True or False.
        
        Checks whether a move is possible witout interception along 
        the vertical and horizontal lines of a chessboard.
        
        Applicable for Q and R units."""
        
        from_r, from_c = fromTuple[0], fromTuple[1]
        to_r, to_c = toTuple[0], toTuple[1]
        r, c = from_r, from_c
        
        ColorTuple = (r, c)
        fromColor = ChessRules.getColorFromPosition(ColorMatr, fromTuple)
        toColor = ChessRules.getColorFromPosition(ColorMatr, toTuple)
        CurrentColor = ChessRules.getColorFromPosition(ColorMatr, ColorTuple)
        
        TupleArray = []
        
        # Check whether move belongs to the same col as that of the
        # selected piece.
        if from_r == to_r:
          # TODO: Simplify lines of code into method().
            # Checks whether it needs to look up or down in the color Board.
            
            operationc = 1 if from_c < to_c else -1
            col = c
            
            while True:
                col = col + operationc
                if not (col >= 0 and col <= 7): break
                
                ColorTuple = (r, col)
                CurrentColor = ChessRules.getColorFromPosition(ColorMatr, ColorTuple)
                
                if CurrentColor == None: 
                    TupleArray.append(ColorTuple)
                
                elif CurrentColor == fromColor: 
                    break
                
                elif not(CurrentColor == fromColor):# Switch to else.
                    TupleArray.append(ColorTuple)
                    break
                    
        # If its nt part of the same row, then is it part of the 
        # same column?.
        elif from_c == to_c:
          # TODO: Simplify lines of code into method().
            # Checks whether it needs to look left or right in the color Board.
            
            operationr = 1 if from_r < to_r else -1
            
            row = r
            
            while True:
            
                row = row + operationr
                if not (row >= 0 and row <= 7): break
                
                ColorTuple = (row, c)
                CurrentColor = ChessRules.getColorFromPosition(ColorMatr, ColorTuple)
                
                if CurrentColor == None:
                    TupleArray.append(ColorTuple)
                    
                elif CurrentColor == fromColor:
                    break
                    
                else: # Switch to else.
                    TupleArray.append(ColorTuple)
                    break
                    
        # If it neither belongs to the same column nor the same row
        # then method ends its turn.
        else: return False
                    
        if toTuple in TupleArray: return True
            
        return False
        
    @staticmethod
    def isItLegalInCrossLine(ColorMatr, fromTuple, toTuple):
        """isItLegalInPlusLine() returns True or False.
        
        Applicable for Q and N."""
        
        from_r, from_c = fromTuple[0], fromTuple[1]
        to_r, to_c = toTuple[0], toTuple[1]
        r, c = from_r, from_c
        
        ColorTuple = (r, c)
        fromColor = ChessRules.getColorFromPosition(ColorMatr, fromTuple)
        toColor = ChessRules.getColorFromPosition(ColorMatr, toTuple)
        CurrentColor = ChessRules.getColorFromPosition(ColorMatr, ColorTuple)
        
        diff_r = from_r - to_r
        diff_c = from_c - to_c
        r_diff_abs = abs(from_r - to_r)
        c_diff_abs = abs(from_c - to_c)
        TupleArray = []
        
        # Check whether move belongs to the same row or column as that of the
        # selected piece.
        
        if from_r == to_r or from_c == to_c:
            return False
            
        # If It reaches here, then check whether they comes in the same line
        # diagonally.
        
        if not (r_diff_abs == c_diff_abs):
            return False
        
        
        
        # If it neither belongs to the same column nor the same row and not in diagonal,
        # then method executes its main order.
        
        else:
            # Variables for conducting increment/decrement operations on row/column
            
            operationr = operationc = 0
            
            # Checks which direction on rows it needs to look in the color Board.
            
            operationr = 1 if from_r < to_r else -1
            operationc = 1 if from_c < to_c else -1
            
            # This loop Writes an array that contains Legal-diagonal-moves
            # by searching towards the desired move.
            
            col = c
            row = r
            
            while True:
            
                # Conduct operations.
                col = col + operationc
                row = row + operationr
                
                if not (col >= 0 and col <= 7) or not (row >= 0 and row <= 7): break
                
                # Form tuple and get team color.
                
                ColorTuple = (row, col)
                CurrentColor = ChessRules.getColorFromPosition(ColorMatr, ColorTuple)
                
                # Test Color of selected element. Add to array if there is no unit,
                # break if the team is same or add and break if it finds an enemy.
                
                if CurrentColor == None:
                    TupleArray.append(ColorTuple)
                    
                elif CurrentColor == fromColor:
                    break
                    
                elif not(CurrentColor == fromColor):# else:
                    TupleArray.append(ColorTuple)
                    break

        # If move is available in generated array,
        # then method is successful.
        
        if toTuple in TupleArray: return True
        
        # Natural else.
        
        return False
    
    @staticmethod
    def seperateBoard(Board):
        
        cMatr = []
        bMatr = []
        
        # Generate 2 matrices.
        for row in Board:
            li_color = []
            li_board = []
            
            for element in row:
                li_color.append(None if element=='e' else element[0])
                li_board.append(element if element=='e' else element[1])
                
            cMatr.append(li_color)
            bMatr.append(li_board)
        return bMatr, cMatr
    
    @staticmethod
    def getKingPos(BoardMatr, ColorMatr, color):
        # Get king pos first. Returns error if its not able to find the king.
        for r, row in enumerate(BoardMatr):
            for c, e in enumerate(row):
                
                if 'K' == e and color == ColorMatr[r][c]: 
                    return (r, c)
                    
    @staticmethod
    def isCheck(BoardMatr, ColorMatr, color):
        
        kingTuple = ChessRules.getKingPos(BoardMatr, ColorMatr, color)
                    
        enemyColor = 'l' if color == 'd' else 'd'
        
        for r, row in enumerate(BoardMatr):
            for c, e in enumerate(row):
                toTuple = r, c
                
                if enemyColor == ColorMatr[r][c]:
                
                    if ChessRules.isItLegal(BoardMatr, ColorMatr, toTuple, kingTuple):
						return True
        return False
        
    @staticmethod
    def testCheck(board, color):
        boardMatr, colorMatr = ChessRules.seperateBoard(board)
        return ChessRules.isCheck(boardMatr, colorMatr, color)
    @staticmethod
    def predictCheck(board, fromTuple, toTuple):
        
        copiedBoard = [[element for element in r] for r in board]
        
        (from_r, from_c), (to_r, to_c) = fromTuple, toTuple
        
        copiedBoard[to_r][to_c] = copiedBoard[from_r][from_c]
        copiedBoard[from_r][from_c] = 'e'
        
        BoardMatr, ColorMatr = ChessRules.seperateBoard(copiedBoard)
        
        return ChessRules.isCheck(BoardMatr, ColorMatr, ColorMatr[to_r][to_c])
    
    @staticmethod
    def isCheckMate(board, color):
        
        BoardMatr, ColorMatr = ChessRules.seperateBoard(board)
        
        kingTuple = ChessRules.getKingPos(BoardMatr, ColorMatr, color)
        
        totalLegalSquares = []
        
        for r, row in enumerate(BoardMatr):
            for c, e in enumerate(row):
                fromTuple = r, c
                
                if color == ColorMatr[r][c]:
                    totalLegalSquares += ChessRules.getLegalSquares(board, BoardMatr, 
                                                                ColorMatr, fromTuple)
        return False if len(totalLegalSquares) else True
    @staticmethod
    def getLegalSquares(board, boardMatr, colorMatr, fromTuple):
        from_r, from_c = fromTuple
        
        legalSquares = []
        for row, r_content in enumerate(boardMatr):
            for col, c_content in enumerate(r_content):
                toTuple = (row, col)
                
                if ChessRules.isItLegal(boardMatr, colorMatr, fromTuple, toTuple):
                
                    # Check whether it puts player in check.
                    if not ChessRules.predictCheck(board, fromTuple, toTuple):
                        legalSquares.append(toTuple)
        return legalSquares
    
    @staticmethod
    def getLegalMoves(Board, fromTuple):
        """getLegalMoves() returns a list of board xy_coords that the player can move.
        
        """
        
        boardMatr, colorMatr = ChessRules.seperateBoard(Board)
        
        legalSquares = ChessRules.getLegalSquares(Board, boardMatr, colorMatr,fromTuple)
        return legalSquares
        
        # NOTE: Either check for all cells legality OR try to simply define
        # and create a list of legal moves.        
