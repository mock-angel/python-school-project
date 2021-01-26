import os
import script
from script import *
script.init()
os.system('reset')
###   print Boards.teams.All.Board_locations_Black
Chess = ChessBoard()
AssignChessOrder(0)
Chess.AssignChessOrder(1)
#Boards.move(c7,c5)
#Boards.move(c8,c2)

Boards.move(c1,e7)
Boards.move(e7,d8)

def main():
    print "\ngetLoc.Blacks"
    print Boards.getLoc.Blacks
    print "\ngetLoc.Whites"
    print Boards.getLoc.Whites
    print "\ngetBoard.team_Blacks"
    for i in range(8):
        print Boards.getBoard.team_Blacks[i]
    print "\ngetBoard.team_Whites"
    for i in range(8):
        print Boards.getBoard.team_Whites[i]
    print "\ngetBoard.team"
    for i in range(8):
        print Boards.getBoard.team[i]
    print "\ngetBoard.Blacks"
    for i in range(8):
        print Boards.getBoard.Blacks[i]
    print "\ngetBoard.Whites"
    for i in range(8):
        print Boards.getBoard.Whites[i]
    print "\ngetBoard.Both"
    for i in range(8):
        print Boards.getBoard.Both[i]
    print"\nBoards.move(a7,a6)" 

    print "getBoard.Both"
    for i in range(8):
        print Boards.getBoard.Both[i]
        
    pos = c7
    print "\nBoards.get_available_move(" + str(pos) +")"
    print Boards.get_available_move(pos)#


    
    
    

    
    
    
    
    
    
    
main()
    
if 1:
    pass
    
    '''
    Individual pieces:

    Pawn - 10 point

    Knight - 30 points

    Bishop - 30 points

    Rook - 50 points

    Queen - 90 points

    Piece combinations:

    Rook and Knight - 75 points

    Rook and Bishop - 80 points

    Pair of Rooks - 100 points

    Three minor pieces - 100 points

    Rook and two minor pieces - 110 points
    '''
    
    
    
    
