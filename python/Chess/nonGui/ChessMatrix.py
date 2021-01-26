# ChessMatrix.py
from ChessRules import ChessRules

DEFAULT_BOARD = [['e','e','e','e','e','e','e','e'],\
				['e','e','e','e','e','e','e','e'],\
				['e','e','e','e','e','e','e','e'],\
				['e','e','e','e','e','e','e','e'],\
				['e','e','e','e','e','e','e','e'],\
				['e','e','e','e','e','e','e','e'],\
				['e','e','e','e','e','e','e','e'],\
				['e','e','e','e','e','e','e','e']]

DEFAULT_BOARD[0] = ['dR','dN','dB','dQ','dK','dB','dN','dR']
DEFAULT_BOARD[1] = ['dp','dp','dp','dp','dp','dp','dp','dp']
DEFAULT_BOARD[2] = ['e','e','e','e','e','e','e','e']
DEFAULT_BOARD[3] = ['e','e','e','e','e','e','e','e']
DEFAULT_BOARD[4] = ['e','e','e','e','e','e','e','e']
DEFAULT_BOARD[5] = ['e','e','e','e','e','e','e','e']
DEFAULT_BOARD[6] = ['lp','lp','lp','lp','lp','lp','lp','lp']
DEFAULT_BOARD[7] = ['lR','lN','lB','lQ','lK','lB','lN','lR']

class ChessMatrix():
    # Maintain only one instance.
    chess_rules = ChessRules()
    def __init__(self, setup = 0, pre_matrix = None):
        self.squares = [['e','e','e','e','e','e','e','e'],\
						['e','e','e','e','e','e','e','e'],\
						['e','e','e','e','e','e','e','e'],\
						['e','e','e','e','e','e','e','e'],\
						['e','e','e','e','e','e','e','e'],\
						['e','e','e','e','e','e','e','e'],\
						['e','e','e','e','e','e','e','e'],\
						['e','e','e','e','e','e','e','e']]
        
        if pre_matrix: 
            self.squares = pre_matrix
            return
            
        if setup == 0: self.squares = [[c for c in r] for r in DEFAULT_BOARD]
    
    def get_available_moves(self, fromTuple):
        
        return self.chess_rules.getLegalMoves(self.squares, fromTuple)
        
    def get_squares(self):
        
        return self.squares
    
    def force_move(self, from_square, to_square):
        """Use if you are allready previously checking authentic moves."""
        
        from_r, from_c = from_square
        to_r, to_c = to_square
        self.squares[to_r][to_c] = self.squares[from_r][from_c]
        self.squares[from_r][from_c] = 'e'
    
    def reset(self):
        self.squares = [[c for c in r] for r in DEFAULT_BOARD]
