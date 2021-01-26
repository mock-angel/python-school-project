def init():
    pass
from sVars import *
from boardinit import emptyarray, Board_default, Location_default
#from color import inv_color
import os
os.system("rm sVars.pyc boardinit.pyc color.pyc script.pyc")
os.system("rm ")
# TODO change everything to arrays
class Board():
  ''' init '''
  def __init__(self):
  # boardinit -------------------------------------
#    ##############################################
#    def emptyarray(selection=None):
#      # TODO: Is there a way to reduce this?
#      # Two conditions can be put to chk selection values
#      # Relace 1.(selection == WHITE) & 2.(selection == BLACK)
#      # with 1.((selection == WHITE) or (selection == None))
#      # and 2.((selection == BLACK) or (selection == None))  
#      # respectively and remove (selection == None) area
#      #
#      # This code basically assigns default board values
#      # regarding unit placement as R, N, B, Q, K, p
#      #
#      #
#      Matr = [[' ' for y in range(8)]for x in range (8)] 
#      if (selection == None):
#        for i in range(8):          # Both colors
#          Matr[1][i] = Matr[6][i] = 'p'
#        Matr[0][1] = Matr[0][6] = 'N'
#        Matr[7][1] = Matr[7][6] = 'N'
#        Matr[0][2] = Matr[0][5] = 'B'
#        Matr[7][2] = Matr[7][5] = 'B'
#        Matr[0][0] = Matr[0][7] = 'R'
#        Matr[7][0] = Matr[7][7] = 'R'
#        Matr[0][3] = Matr[7][3] = 'Q'
#        Matr[0][4] = Matr[7][4] = 'K'
#      if (selection == WHITE):      # The White selection
#        for i in range(8):
#          Matr[6][i] = 'p'
#        Matr[7][1] = Matr[7][6] = 'N'
#        Matr[7][2] = Matr[7][5] = 'B'
#        Matr[7][0] = Matr[7][7] = 'R'
#        Matr[7][3] = 'Q'
#        Matr[7][4] = 'K'
#      if (selection == BLACK):      # The Black selection
#        for i in range(8):
#          Matr[1][i] = 'p'
#        Matr[0][1] = Matr[0][6] = 'N'
#        Matr[0][2] = Matr[0][5] = 'B'
#        Matr[0][0] = Matr[0][7] = 'R'
#        Matr[0][3] = 'Q'
#        Matr[0][4] = 'K'
#      return Matr
#    ##############################################

#    #################################################
#    def Board_default(selection=None, Team=None):
#      # TODO: Apparently complete
#      #
#      # Defines which part of the board is black
#      # and which is white.
#      # 
#      #
#      Matr = [[' ' for y in range(8)]for x in range (8)]
#      if Team == TEAMS:
#        for i in range(8):
#            if selection == BLACK or selection == None:
#              Matr[0][i] = Matr[1][i] = SBLACK
#            if selection == WHITE or selection == None:
#              Matr[7][i] = Matr[6][i] = SWHITE
#      else:
#        return emptyarray(selection)

#      return Matr
#    #################################################
      
#    ##############################################
#    def Location_default(selection=None, ):
#      # TODO: Apparently complete
#      #
#      # Gives locations of all places containing 
#      # units
#      # 
#      # When [selection = None](i,e nt specified in 
#      # definition calling), both team's unit locs
#      # are 
#      Matr = []
#        
#      if selection == BLACK or selection == None:
#        for i in range(8):
#          Matr += [[0, i]]
#        for i in range(8):
#          Matr += [[1, i]]
#      if selection == WHITE or selection == None:
#        for i in range(8):
#          Matr += [[6, i]]
#        for i in range(8):
#          Matr += [[7, i]]
#      return Matr
#    ##############################################
        
    class __get_Info():
      def __init__(self, val=ALL, perem=ALL):
            self.start_Info(val, perem)
      def start_Info(self, val, perem):
        if perem == ALL:
         if val == ALL:
          '''
          # Too confusing to set up.
          # Code neutralised.
          #
          self.teams_All = Board_default()
          self.teams_Black = Board_default(BLACK)
          self.teams_White = Board_default(WHITE)
          self.All = Location_default()
          self.Blacks = Location_default(BLACK)
          self.Whites = Location_default(WHITE)
          '''
         if val == LOC:
          self.Both = Location_default()
          self.Blacks = Location_default(BLACK)
          self.Whites = Location_default(WHITE)
         if val == BOARD:
          # WH and BL
          self.team_Blacks = Board_default(BLACK, TEAMS)
          self.team_Whites = Board_default(WHITE, TEAMS)
          self.team = Board_default(Team=TEAMS) #both teams
          # p,R,N,B,Q,K
          self.Blacks = Board_default(BLACK)
          self.Whites = Board_default(WHITE)
          self.Both = Board_default()
          
    self.units = emptyarray()
    self.getDefaultAll = __get_Info()       #class
    self.getDefaultLoc = __get_Info(LOC)    #class
    self.getDefaultBoard = __get_Info(BOARD)#class
    self.getAll = __get_Info()         #class
    self.getLoc = __get_Info(LOC)    #class
    self.getBoard = __get_Info(BOARD)#class
  ''' /init '''
  
  ###############################################       MOVE
  def move(self, fromPOS, toPOS):
    # TODO: Need to update all other varables -DONE
    # Use getBoard.Both and then later          
    # write script to update every other
    # variable.
    # ***********************************
    # TODO: I neeed to remove enemy unit when moved
    # and not make the move if its friendly(provided 
    # error perhaps).
    # I also might want to check whether units path
    # is obstructed.                          -DONE
    # Possible errors could be
    # UnitPathObstructed, PositionFriendly,
    # UnauthorisedAccesstoUnit, PositionInvalid
    # LocationEmpty(=UnauthorisedAccesstoUnit)
    # ***********************************
    #
    # 
    # Break after for loops.
    #
    #getBoard
    chk_y = y = toPOS[0]
    chk_x = x = toPOS[1]
    passPermit = 1
    print str(fromPOS) + " " + str(toPOS)
    if (self.getBoard.team[fromPOS[0]][fromPOS[1]] == self.getBoard.team[toPOS[0]][toPOS[1]]
        and self.getBoard.team[fromPOS[0]][fromPOS[1]] != ' '):
      print self.getBoard.team[toPOS[0]][toPOS[1]]
      print "first     ------ error"
      suitOne(FriendlyFire).currentException(FriendlyFire)
      passPermit = 0
    print self.get_available_move(fromPOS) 
    if [toPOS] in self.get_available_move(fromPOS):
      print self.getBoard.team[toPOS[0]][toPOS[1]]
      print "second     ------ error"
      suitOne(MoveUnavailable).currentException(MoveUnavailable)
      passPermit = 0
    if passPermit:
      self.getBoard.Both[toPOS[0]][toPOS[1]] = (
        self.getBoard.Both[fromPOS[0]][fromPOS[1]])
      self.getBoard.Whites[toPOS[0]][toPOS[1]] = (
        self.getBoard.Whites[fromPOS[0]][fromPOS[1]])
      self.getBoard.Blacks[toPOS[0]][toPOS[1]] = (
        self.getBoard.Blacks[fromPOS[0]][fromPOS[1]])
        
      self.getBoard.team[toPOS[0]][toPOS[1]] = (
        self.getBoard.team[fromPOS[0]][fromPOS[1]])
      self.getBoard.team_Whites[toPOS[0]][toPOS[1]] = (
        self.getBoard.team_Whites[fromPOS[0]][fromPOS[1]])
      self.getBoard.team_Blacks[toPOS[0]][toPOS[1]] = (
        self.getBoard.team_Blacks[fromPOS[0]][fromPOS[1]])

      self.getBoard.Both[fromPOS[0]][fromPOS[1]] = ' '
      self.getBoard.Blacks[fromPOS[0]][fromPOS[1]] = ' '
      self.getBoard.Whites[fromPOS[0]][fromPOS[1]] = ' '
    
      self.getBoard.team[fromPOS[0]][fromPOS[1]] = ' '
      self.getBoard.team_Blacks[fromPOS[0]][fromPOS[1]] = ' '
      self.getBoard.team_Whites[fromPOS[0]][fromPOS[1]] = ' '
    
    
    # TODO: Enter break to come out of unnecessary 
    # evaluation.  Merge 3 loops to 1 loop with 2 if
    # confitions nested inside to decrease execution 
    # time.         --HALT
    # But avoid it as far as possible
    # TODO: Why not evaluate for Black and White and then
    # merge two lists?
    #               --HALT
    #
    #getLoc
      l = 0
      for i in self.getLoc.Blacks:
        if i == [fromPOS[0], fromPOS[1]]:
          self.getLoc.Blacks[l] = (
              [[toPOS[0], toPOS[1]]]
              )
        l += 1
      m = 0
      for i in self.getLoc.Whites:
        if i == [fromPOS[0], fromPOS[1]]:
          self.getLoc.Whites[m] = (
              [[toPOS[0], toPOS[1]]]
              )
        m += 1
      n = 0
      for i in self.getLoc.Both:
        if i == [fromPOS[0], fromPOS[1]]:
          self.getLoc.Both[n] = (
              [[toPOS[0], toPOS[1]]]
              )
        n += 1

    pass

  ###############################################

  ###############################################
  def get_available_move(self, POS):
    # TODO: Make it check for teams and -- DONE
    #   don't include location if friendly.
    # TODO: Do we seperate into independant 
    #   modules?
    # TODO: Is there a better way to simplyfy this?
    # Method would be easier and code would be more 
    # legible and effecient. 
    #
    # First check all moves of piece on an empty board. 
    # Then check team and remove coinciding 
    # friendly locations.
    # 
    #
    ####################################
    def reculcate_moves(crntLoc, chkLoc, 
                        getBoard):
      # Function meant for simplification, not changing 
      # parts of existing array
      print "\n  Doing reculcate_moves"
      x = crntLoc[0]
      y = crntLoc[1]
      chk_x = chkLoc[0]
      chk_y = chkLoc[1]
      print "crntLoc = " + str(crntLoc)
      print "chkLoc = " + str(chkLoc)
      if (chk_x >= 0 
          and chk_x <= 7 
          and chk_y >= 0 
          and chk_y <= 7):
        # Makes sure it checks places only
        # inside border.
          
        if (str(getBoard.Both[chk_y][chk_x]) != str(' ') ):
          # If unit is present
          # in provided location.
          
          # -----------------------------
          # Checks for friendly units.
          # FIXME: Bug here !!!!!!  --MAYBE CORRECTED
          # 
          print "lll"
          if (
            getBoard.team[y][x] == 
            getBoard.team[chk_y][chk_x]
            and getBoard.team[y][x] != ' '
                ):
            print getBoard.team[chk_y][chk_x]
            print "ss"
            return []
          # -----------------------------
          
            print getBoard.team[2][1]
          return [[[chk_x, chk_y]], 1]
        else:
          # If NO unit is present
          # in provided location.
          
          return [[[chk_x, chk_y]], 0]
          pass
#          else: 
#           pass
#          if (str(getBoard.Both[chk_y][chk_x]) == str(' ') ):
##            print repr(getBoard.Both[chk_y][chk_x] + 'p')
#             return [[chk_x,chk_y]]
      return []
    ####################################
     
    ###############################################
    def freelinemove(xy):
       xx = self.xy.xx
       yy = self.xy.yy
       
       x = self.xy.x
       y = self.xy.y
       n = 1
       LOCATIONS  = []
       print " reached freelinemove --"
       while(1):
        
        store = reculcate_moves(
                            (x, y), (x + xx, y + yy),
                            self.getBoard)
        if store == []:
            print '  opting for exit --'
            break
        print "\n  unique   --  "+ str(n)
        print "    " + str(LOCATIONS) + (str(len(LOCATIONS)))
        print "    " + 'store[1] = ' + str(store[1])
        print "    " + 'store = ' + str(store)
        print "    " + repr(self.getBoard.Both[y + yy][x + xx])
        if store[1] == 0:
          LOCATIONS += store[0]
        else:
          LOCATIONS += store[0]
          break
        x += xx
        y += yy
        
        # --------------------------------------
        # TODO: Is this necessary?
        # May need to conduct tests and remove if
        # code has negative or no effect on output
        #
        if len(LOCATIONS) != (n):
          store = reculcate_moves(
                            (x, y), (x + 1, yy + 1),
                            self.getBoard)
                    
          break
        # --------------------------------------
        
        
        n += 1
       self.xy.LOCATIONS  += LOCATIONS
       print "Final === " + str(self.xy.LOCATIONS)
       self.xy.LOCATIONS = []
    ###############################################
    
    self.getBoard.Both[POS[0]][POS[1]] 
    self.xy.x = x = POS[1]
    self.xy.y = y = POS[0]
    exception = [None]
    LOCATIONS = []
#    storeClass = ''
    # For 'p'
    
    
    if self.getBoard.Both[POS[0]][POS[1]] == 'p':

      # ****************************************************
      def pawns(location_holders):
          xx = location_holders[0]
          yy = location_holders[1]
          UNIT_MODE = location_holders[2]
          LOCATE = reculcate_moves(
                                (x, y), (xx, yy),
                                self.getBoard)
          if LOCATE != []:
            if (LOCATE[1] == 1) and UNIT_MODE == ATTACK:
              return LOCATE
            print LOCATE[1]
            if (LOCATE[1] == 0) and UNIT_MODE == NO_ATTACK:
              return LOCATE
#          elif(Friendly_Allow == True and  )
          return []
      # ****************************************************
      
      location_holders = [ [x, y + 1, NO_ATTACK],
                           [x + 1, y + 1, ATTACK],
                           [x - 1, y + 1, ATTACK] 
      ]
      
      for i in location_holders:
        LOCATIONS += pawns(i)
       
      j = self.getBoard
    # For 'K'
    if self.getBoard.Both[POS[0]][POS[1]] == 'K':
    # TODO: Need to look for check 
    #   Is in (--BookMark 1)
      x = self.xy.x
      y = self.xy.y
      LOCATIONS += reculcate_moves(
                            (x, y), (x - 1, y - 1),
                            self.getBoard)
      LOCATIONS += reculcate_moves(
                            (x, y), (x - 1, y),
                            self.getBoard)
      LOCATIONS += reculcate_moves(
                            (x, y), (x - 1, y + 1),
                            self.getBoard)
      LOCATIONS += reculcate_moves(
                            (x, y), (x, y - 1),
                            self.getBoard)
      LOCATIONS += reculcate_moves(
                            (x, y), (x, y + 1),
                            self.getBoard)
      LOCATIONS += reculcate_moves(
                            (x, y), (x + 1, y - 1),
                            self.getBoard)
      LOCATIONS += reculcate_moves(
                            (x, y), (x + 1, y),
                            self.getBoard)
      LOCATIONS += reculcate_moves(
                            (x, y), (x + 1, y + 1),
                            self.getBoard)
                            
      def kings(location_holders):
        xx = location_holders[0]
        yy = location_holders[1]
        UNIT_MODE = location_holders[2]
        return reculcate_moves(
                                (x, y), (x + 1, y + 1),
                                self.getBoard)
#      location_holders = [ [x - 1, y - 1, BOTH], [x, y - 1, BOTH], [x + 1, y - 1, BOTH],
#                           [x - 1, y, BOTH],                       [x + 1, y, BOTH],
#                           [x - 1, y + 1, BOTH], x, y + 1, BOTH],  [x + 1, y + 1, BOTH]
#      ]
      location_holders = [ [- 1, - 1,], [0, - 1], [+ 1, - 1],
                           [- 1, 0],              [+ 1, y],
                           [- 1, + 1], [0, + 1], [+ 1, + 1]
      ]
      # (--BookMark 1)
      # TODO: must check all other enemy placement and check whether
      #     any of them have king's location as target to call it check
      #     after that calculate all available moves for king and check which 
      #     isn't included in being checkmate
      # It would suit best to include 2 arrays that traces all
      # available moves of pieces.
      for i in location_holders:
        i[0] = x
        i[1] = y
        i += [BOTH]
        LOCATIONS += kings(i)
        
    
    # For 'R' 
    if self.getBoard.Both[POS[0]][POS[1]] == 'R':

      castleMoves = [        [0, -1],
                    [1, 0],          [-1, 0],
                             [0, 1]
      ]
      for i in castleMoves:
        self.xy.xy(i[0], i[1])
        freelinemove(self.xy)
    # For 'Q' 
    if self.getBoard.Both[POS[0]][POS[1]] == 'Q':
      
      queenMoves = [[-1, -1], [0, -1], [1, -1],
                    [1, 0],            [-1, 0],
                    [-1, 1],  [0, 1],  [1, 1]
      ]
      for i in queenMoves:
        self.xy.xy(i[0], i[1])
        freelinemove(self.xy)
    # For 'B' 
    if self.getBoard.Both[POS[0]][POS[1]] == 'B':
     
      bishopMoves = [[-1, -1],        [1, -1],
                              
                    [-1, 1],          [1, 1]
      ]
      for i in bishopMoves:
        print "\n\n+++++++++++++++++++++++++++++++++++++++++++++++"
        print str(i) + ' in bishopMoves' 
        self.xy.xy(i[0], i[1])
        freelinemove(self.xy) 
    return LOCATIONS
  ###############################################
 
  ###############################################
  class __xyz():#location holder
    def __init__(self):
        self.x = self.y = 0
        self.xx = self.yy = 0
        self.LOCATIONS = []
    def refreshxyz():
        pass
    def xy(self, x, y):
        self.xx = x
        self.yy = y
  xy = __xyz()
  ###############################################   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

# Check whether enemy 
def is_It_Enemy(locF, locC, getBoard):
    if getBoard.teams[locF[0]][locF[1]] == SBLACK:
      if getBoard.teams[locC[0]][locC[1]] == SBLACK:
        return 0
      else:
        return 1
    if getBoard.teams[locF[0]][locF[1]] == SWHITE:
      if getBoard.teams[locC[0]][locC[1]] == SWHITE:
        return 0
      else:
        return 1
        
        
FriendlyFire = 0
MoveUnavailable = 1
errorNames = [  "FriendlyFire", 
                "MoveUnavailable"
]      
# Exceptions
class ExceptionsCase:
  def __init__(self, ErrorType):
    self.ErrorType = ErrorType
    pass
  def currentException(self, ErrorType):
      print "Exception occured:"
      print errorNames[ErrorType] + " -  " +str(ErrorType) + ": Cannot move pieces"
suitOne = ExceptionsCase







# Invert team colors
def inv_color(COLOR):
    if COLOR == BLACK:
        return WHITE
    if COLOR == WHITE:
        return BLACK
    if COLOR == SBLACK:
        return SWHITE
    if COLOR == SWHITE:
        return SBLACK



















