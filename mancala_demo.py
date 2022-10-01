"""Mancala, built on Norvig's Game class
adapted to Python 3 in September 2016

"""

from utils import *
# from Tkinter import *
import random, re, time


count = 0
testing = 0
BigInitialValue = 1000000


def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    global count
    global testing
    global BigInitialValue
    
    player = game.to_move(state)
    count = 0
    starttime = time.time()
    

    def max_value(state, alpha, beta, depth):
        global count, testing
        if testing:
            print("  "* depth, "Max  alpha: ", alpha, " beta: ", beta, " depth: ", depth)
        if cutoff_test(state, depth):
            if testing:
                print("  "* depth, "Max cutoff returning ", eval_fn(state))
            return eval_fn(state)
        v = -BigInitialValue
        succ = game.successors(state)
        count = count + len(succ)
        if testing:
            print("  "*depth, "maxDepth: ", depth, "Total:", count, "Successors: ", len(game.successors(state)))
        for (a, s) in succ:
            # Decide whether to call max_value or min_value, depending on whose move it is next.
            # Some games, such as Mancala, sometimes allow the same player to make multiple moves.
            if state.to_move == s.to_move:
                v = max(v, max_value(s, alpha, beta, depth+1))
            else:
                v = max(v, min_value(s, alpha, beta, depth+1))
            if testing:
                print("  "* depth, "max best value:", v)
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        global count
        if testing:
            print("  "*depth, "Min  alpha: ", alpha, " beta: ", beta, " depth: ", depth)
        if cutoff_test(state, depth):
            if testing:
                print("  "*depth, "Min cutoff returning ", eval_fn(state))
            return eval_fn(state)
        v = BigInitialValue
        succ = game.successors(state)
        count = count + len(succ)
        if testing:
            print("  "*depth, "minDepth: ", depth, "Total:", count, "Successors: ", len(game.successors(state)))
        for (a, s) in succ:
            # Decide whether to call max_value or min_value, depending on whose move it is next.
            # Some games, such as Mancala, sometimes allow the same player to make multiple moves.
            if state.to_move == s.to_move:
                v = min(v, min_value(s, alpha, beta, depth+1))
            else:
                v = min(v, max_value(s, alpha, beta, depth+1))
            if testing:
                print("  "*depth, "min best value:", v)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def right_value(s, alpha, beta, depth):
        if s.to_move == state.to_move:
            return max_value(s, -BigInitialValue, BigInitialValue, 0)
        else:
            return min_value(s, -BigInitialValue, BigInitialValue, 0)

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, game.current_player))
    action, state = argmax(game.successors(state),
                           # lambda ((a, s)): right_value(s, -BigInitialValue, BigInitialValue, 0))
                            lambda a_s: right_value(a_s[1], -BigInitialValue, BigInitialValue, 0))
    stoptime = time.time()
    elapsed = stoptime - starttime
    print("Final count: ", count, "Time: ", end=",")
    print(" %.5f seconds" % elapsed)
    return action

#______________________________________________________________________________
# Players for Games

##def query_player(game, state):
##    "Make a move by querying standard input."
##    game.display(state)
##    return num_or_str(raw_input('Your move? '))
##
##def random_player(game, state):
##    "A player that chooses a legal move at random."
##    # Added state argument to legal_moves AJG 8/9/04
##    return random.choice(game.legal_moves(state))
##
##def alphabeta_player(game, state):
##    return alphabeta_search(state, game)
##
##def alphabeta_full_player(game, state):
##    return alphabeta_full_search(state, game)
##
##def alphabeta_depth1_player(game, state):
##    return alphabeta_search(state, game, 1)

class mancala_player:
    def __init__(self, name):
        self.name = name
        
    def calculate_utility(self, boardstate):
        return boardstate.default_utility()

    def alphabeta_parameters(self, boardstate, remainingTime):
        # This should return a tuple of (cutoffDepth, cutoffTest, evalFn)
        # where any (or all) of the values can be None, in which case the
        # default values are used:
        #        cutoffDepth default is 4
        #        cutoffTest default is None, which just uses cutoffDepth to
        #            determine whether to cutoff search
        #        evalFn default is None, which uses your boardstate_utility_fn
        #            to evaluate the utility of board states.
       return (4, None, None)        

class mancala_player2:
    def __init__(self, name):
        self.name = name
        
    def calculate_utility(self, boardstate):
        return boardstate.default_utility2()

    def alphabeta_parameters(self, boardstate, remainingTime):
        # This should return a tuple of (cutoffDepth, cutoffTest, evalFn)
        # where any (or all) of the values can be None, in which case the
        # default values are used:
        #        cutoffDepth default is 4
        #        cutoffTest default is None, which just uses cutoffDepth to
        #            determine whether to cutoff search
        #        evalFn default is None, which uses your boardstate_utility_fn
        #            to evaluate the utility of board states.
       return (6, None, None)        

def play_mancala(game=None,initialTime=600,
                 player1=mancala_player("p1"),player2=mancala_player2("p2")):
    "Play an 2-person, move-alternating Mancala game."
    # This is play_game with stuff added to keep track of time.
    game = game or Mancala()
    state = game.initial
    players = (player1, player2)
    # initialize the amount of time for each player.  Units are seconds.
    # 600 seconds is 10 minutes
    clocks = {player1: initialTime, player2: initialTime}
    previousPass = 0
    while True:
        player = players[state.to_move]
        game.current_player = player
        params = player.alphabeta_parameters(state, clocks[player])
        startTime = time.time()
        move = alphabeta_search(state, game, params[0], params[1], params[2])
        endTime = time.time()
        moveTime = endTime - startTime
        if moveTime > clocks[player]:
             print("Player", player.name, "took too much time and loses.")
             # Should really just return some utility that reflects player losing.
             return "Game Over!!!"
        else:
            clocks[player] -= moveTime
        state = game.make_move(move, state)
        print("Time remaining player 1:", clocks[player1], "player 2:", clocks[player2])
        print("Player: ", player.name, "took move ", move, "resulting in state:")
        game.display(state)
        if game.terminal_test(state):
            P0Count = state.PlayerPieceCount(P0)
            P1Count = state.PlayerPieceCount(P1)
            print("Player: ", players[P0].name, "piece count: ", P0Count)
            print("Player: ", players[P1].name, "piece count: ", P1Count)
            if P0Count > P1Count:
                print("Player ", players[P0].name, " WINS!!!")
            elif P1Count > P0Count:
                print("Player ", players[P1].name, " WINS!!!")
            else:
                print("Game is a tie.")
            return "Game Over!!"

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement
    legal_moves, make_move, utility, and terminal_test. You may
    override display and successors or you can inherit their default
    methods. You will also need to set the .initial attribute to the
    initial state; this can be done in the constructor."""

    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."
        abstract()

    def make_move(self, move, state):
        "Return the state that results from making a move from a state."
        abstract()
            
    def utility(self, state, player):
        "Return the value of this final state to player."
        abstract()

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.legal_moves(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print(state)

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        m = [(move, self.make_move(move, state))
                for move in self.legal_moves(state)]
        return m

#        return [(move, self.make_move(move, state))
#                for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


#______________________________________________________________________________
# Beginning of Mancala classes

# Mancala board representation:
#      x1 x2 x3 x4 x5 x6
#  x0                     y0
#      y1 y2 y3 y4 y5 y6
#
# Assume the named positions shown above, where y0 and x0 are the Mancala's for
# player's y and x respective, and the remaining positions are the bins.
# The board is stored as a list with the elements in the following order:
#  [y1, y2, y3, y4, y5, y6, y0,
#   x6, x5, x4, x3, x2, x1, x0]
#
# Notice that this ordering means we can just step through the list to find
# continguous bins.

# give names to where particular positions appear in the internal list
P0Mancala = 6
P1Mancala = 13
P0Start = 0
P1Start = 7

# other constants
InitialPieceCount = 6
P0 = 0
P1 = 1

def opponent(player):
    if player == 1:
        return 0
    elif player == 0:
        return 1
    else:
        print("Oooooooooooooooops")

class BoardState:
    """Holds one state of the Mancala board."""
    def __init__(self, to_move=None, utility=None, board=None, moves=None):
        if ((to_move == 0) or (to_move == 1)):   # assume if to_move is not None, then neither are the rest
            self.to_move = to_move
            self._utility = utility
            self._board = board
            self._moves = moves
        else:
            self.create_initial_boardstate()

    def getPlayer(self):
        return self.to_move

    def create_initial_boardstate(self):
        """Create an initial boardstate with the default start state."""
        # this magic bit of code creates a list with 14 elements in it,
        # each of which is InitialPieceCount
        b = [InitialPieceCount] * 14
        # Now reset the 2 Mancala bins to be 0, instead of InitialPieceCount
        b[P0Mancala] = 0
        b[P1Mancala] = 0
        self._board = b

        self.to_move = P0   # P0 has the first move
        self._moves = self.calculate_legal_moves()
        self._utility = self.default_utility()

    def legal_p(self, move):
        "A legal move must involve a position with pieces."
        if self._board[move] > 0:
            return True
        else:
            return None

    def legal_moves(self):
        "Return a list of legal moves for player."
        return self._moves

    def calculate_legal_moves(self):
        """Calculate the legal moves in the current BoardState."""
        moves = []
        if self.to_move == P0:
            # the range of bins that P0 is allowed to choose from
            for poss in range(P0Start,P0Mancala):
                if self.legal_p(poss):
                    moves.append(poss)
        else:
            # the range of bins that P1 is allowed to choose from
            for poss in range(P1Start,P1Mancala):
                if self.legal_p(poss):
                    moves.append(poss)
        return moves
        

    def make_move(self, move):
        "Return a new BoardState reflecting move made from given board state."
        newboard = BoardState(opponent(self.to_move), None, self._board[:], None)
        # Note where the opponent's mancala is located
        if self.to_move == P1:
            oppMancala = P0Mancala
        else:
            oppMancala = P1Mancala
        if move != None:
            # the number of pieces to be distributed around the board
            pieceCount = newboard._board[move]
            # set the move position's piece count to 0
            newboard._board[move] = 0

            # figure out the first bin that gets a piece distributed to it
            position = (move + 1) % 14
            # keep distributing pieces until you run out
            while pieceCount > 0:
                # don't distribute a piece to the opponent's mancala
                if position != oppMancala:
                    newboard._board[position] += 1
                    pieceCount -= 1
                position = (position + 1) % 14

            # if last move is into a previously empty bin owned by mover, then capture
            # the opponent's pieces from the opposite bin
            lastMove = (position - 1) % 14
            inRange = False
            if self.to_move == P0:
                if lastMove in range(P0Start, P0Mancala):
                    inRange = True
            else:
                if lastMove in range(P1Start, P1Mancala):
                    inRange = True
            if (newboard._board[lastMove] == 1) and inRange:
                # Magically, in our representation the "opposite" bin is always in the
                # array position 12 - Bin.
                oppBin = 12 - lastMove
                oppCount = newboard._board[oppBin]
                newboard._board[oppBin] = 0
                # print "!!! captured ", oppCount, " pieces from bin: ", oppBin
                if self.to_move == P0:
                    newboard._board[P0Mancala] += oppCount
                else:
                    newboard._board[P1Mancala] += oppCount

            # if last move is into the player's own Mancala, then they get another turn
            #  Note that this is kind of weird from a Minimax search perspective.
            if (self.to_move == P0) and (lastMove == P0Mancala):
                newboard.to_move = self.to_move
            elif (self.to_move == P1) and (lastMove == P1Mancala):
                newboard.to_move = self.to_move
            
        newboard._moves = newboard.calculate_legal_moves()
        return newboard

    def PlayerPieceCount(self, player):
        "Return a count of player's pieces where player is P0 or P1."
        total = 0
        if player == P0:
            for pos in range(P0Start,P0Mancala+1):
                total += self._board[pos]
        else:
            for pos in range(P1Start,P1Mancala+1):
                total += self._board[pos]
        return total

    def default_utility(self):
        "Return count of player's pieces minus opponent's pieces."
        p0total = self.PlayerPieceCount(P0)
        p1total = self.PlayerPieceCount(P1)
        if self.to_move == P0:
            return p0total - p1total
        else:
            return p1total - p0total

    def default_utility2(self):
        "Return player's Mancala count minus opponent's Mancala count."
        if self.to_move == P0:
            return self._board[P0Mancala] - self._board[P1Mancala]
        else:
            return self._board[P1Mancala] - self._board[P0Mancala]

class Mancala(Game):
    """Play Mancala on a board with 6 bins plus a Mancala for each player."""

    def __init__(self):
        self.current_state = BoardState()
        self.initial = self.current_state

    def display(self, boardstate):
        "Print out the board in a readable way."
        print('   ', end="")
        for top in range(12,7,-1):
            print('%2d' % boardstate._board[top],end=",")
        print('%2d' % boardstate._board[7],end="\n")
        # print(' ', end='\n')
        print(boardstate._board[P1Mancala],end="")
        for place in range(12,6,-1):
            print('   ',end="")
        print(' ', boardstate._board[P0Mancala])

        print('   ',end="")
        for bottom in range(P0Start,P0Mancala-1):
            print('%2d' % boardstate._board[bottom],end=",")
        print('%2d' % boardstate._board[P0Mancala-1],end="\n")
        # print()
        
    def legal_moves(self, boardstate):
        return boardstate.legal_moves()
    
    def make_move(self, move, boardstate):
        "Return a new BoardState reflecting move made from given board state."
        newBoard = boardstate.make_move(move)
        return newBoard

    def calculate_utility(self, boardstate):
        return boardstate.default_utility()

    def utility(self, boardstate, player):
        "This is where your utility function gets called."
        return player.calculate_utility(boardstate)

