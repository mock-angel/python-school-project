from ChessBoard import *
import ChessRules

Game = ChessBoard()
Game.AssignChessOrder(3)
GameRules = ChessRules.ChessRules()
print list(GameRules.getListOfLegalMoves(Game.getBoard, Game.getTeamColor, (0, 1)))

print "hello"





