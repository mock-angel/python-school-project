

from boardinit import *
from sVars import *


##############################################
def emptyarray(selection=None):
  # TODO: Is there a way to reduce this?
  # Two conditions can be put to chk selection values
  # Relace 1.(selection == WHITE) & 2.(selection == BLACK)
  # with 1.((selection == WHITE) or (selection == None))
  # and 2.((selection == BLACK) or (selection == None))  
  # respectively and remove (selection == None) area
  #
  # This code basically assigns default board values
  # regarding unit placement as R, N, B, Q, K, p
  #
  #
  Matr = [[' ' for y in range(8)]for x in range (8)] 
  if (selection == None):
    for i in range(8):          # Both colors
      Matr[1][i] = Matr[6][i] = 'p'
    Matr[0][1] = Matr[0][6] = 'N'
    Matr[7][1] = Matr[7][6] = 'N'
    Matr[0][2] = Matr[0][5] = 'B'
    Matr[7][2] = Matr[7][5] = 'B'
    Matr[0][0] = Matr[0][7] = 'R'
    Matr[7][0] = Matr[7][7] = 'R'
    Matr[0][3] = Matr[7][3] = 'Q'
    Matr[0][4] = Matr[7][4] = 'K'
  if (selection == WHITE):      # The White selection
    for i in range(8):
      Matr[6][i] = 'p'
    Matr[7][1] = Matr[7][6] = 'N'
    Matr[7][2] = Matr[7][5] = 'B'
    Matr[7][0] = Matr[7][7] = 'R'
    Matr[7][3] = 'Q'
    Matr[7][4] = 'K'
  if (selection == BLACK):      # The Black selection
    for i in range(8):
      Matr[1][i] = 'p'
    Matr[0][1] = Matr[0][6] = 'N'
    Matr[0][2] = Matr[0][5] = 'B'
    Matr[0][0] = Matr[0][7] = 'R'
    Matr[0][3] = 'Q'
    Matr[0][4] = 'K'
  return Matr
##############################################

#################################################
def Board_default(selection=None, Team=None):
  # TODO: Apparently complete
  #
  # Defines which part of the board is black
  # and which is white.
  # 
  #
  Matr = [[' ' for y in range(8)]for x in range (8)]
  if Team == TEAMS:
    for i in range(8):
        if selection == BLACK or selection == None:
          Matr[0][i] = Matr[1][i] = SBLACK
        if selection == WHITE or selection == None:
          Matr[7][i] = Matr[6][i] = SWHITE
  else:
    return emptyarray(selection)

  return Matr
#################################################

##############################################
def Location_default(selection=None, ):
  # TODO: Apparently complete
  #
  # Gives locations of all places containing 
  # units
  # 
  # When [selection = None](i,e nt specified in 
  # definition calling), both team's unit locs
  # are 
  Matr = []
    
  if selection == BLACK or selection == None:
    for i in range(8):
      Matr += [[0, i]]
    for i in range(8):
      Matr += [[1, i]]
  if selection == WHITE or selection == None:
    for i in range(8):
      Matr += [[6, i]]
    for i in range(8):
      Matr += [[7, i]]
  return Matr
##############################################

