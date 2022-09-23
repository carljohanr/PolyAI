# This file has functions modified from the blokus implementation at
# https://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1305&context=cpesp

'''
Polyssimo Challenge AI
This code implements http://abrobecker.free.fr/jeux/index.htm#polyssimochallenge
It has been adapted from Blokus code, and contains some hacks that makes it illogical 
(e.g. referring to all points on the board as 'corners' in the piece placement code)

'''

import sys
import math
import random
import copy
import piece_poly as piece
from gui import *
import copy
import operator
import time
import numpy as np

# cutoff depth for alphabeta minimax search (default 2)
Depth = 1
# number of successor states returned (default 4)
MovesToConsider = 4
# change to adjust the number of games played (defualt 10)
Games = 1
TS = 0

# taken from mancala.py, used for alphabeta search
count = 0
testing = 0
BigInitialValue = 1000000

# number of total squares amongst all of a player's starting pieces
TotalStartingSize = 66
# number of pieces per player at the start of the game
TotalStartingPieces = 12

# used for analyzing AI performance
MoveTimes = []
Outcomes = []
Scores1 = []
Scores2 = []

Names = ['X','T','Z','W','U','F','P','I','L','N','Y','V']

MCounts = [0,0,0,0,0,0,0,0,0,0,0,0]

[piece.C0(),piece.C1(),piece.D0(),piece.Z0(),piece.W0(),piece.X0(),piece.F0(),piece.F1(),piece.F2(),piece.F3(),piece.F4(),piece.F5(),\
                      piece.I(),piece.L(),piece.V(),piece.W(),piece.F(),piece.X(),piece.N(),piece.Y(),piece.U(),piece.P(),piece.T(),piece.Z()];

ActualEstimatePairs = []
UselessInit = {
    'F0': 0,
    'F1': 0,
    'F2': 0,
    'F3': 0,
    'F4': 0,
    'F5': 0,
    'C0': 0,
    'C1': 0,
    'W0': 0,
    'Z0': 0,
    'X0': 0,
    'D0': 0
}
AIUseless = UselessInit
OpponentUseless = UselessInit

# Blokus Board
# DC-Claire
class Board:
    def __init__(self, nrow, ncol):
        self.nrow = nrow; # total rows
        self.ncol = ncol; # total columns

        self.state = [['_'] * ncol for i in range(nrow)];
        self.state2 = [[0] * ncol for i in range(nrow)];

    def update(self, player_id, placement):
        
        #print(self.state)
        #print(self.state2)
        maxval = max([max(s) for s in self.state2])
        for row in range(self.nrow):
            for col in range(self.ncol):
                if(col, row) in placement:
                    self.state[row][col] = player_id;
                    self.state2[row][col] = maxval+1

    # Check if the point (y, x) is within the board's bound
    def in_bounds(self, point):
        return 0<= point[0] < self.ncol and 0<= point[1] < self.nrow;

    # Check if a piece placement overlap another piece on the board
    def overlap(self, placement):
        return False in[(self.state[y][x] == '_') for x, y in placement]

    # Checks if a piece placement is adjacent to any square on
    # the board which are occupied by the player proposing the move.
    def adj(self, player_id, placement):
        adjacents = [];
        # Check left, right, up, down for adjacent square
        for x, y in placement:
            if self.in_bounds((x + 1, y)):
                adjacents += [self.state[y][x + 1] == player_id];
            if self.in_bounds((x -1, y)):
                adjacents += [self.state[y][x - 1] == player_id];
            if self.in_bounds((x, y -1)):
                adjacents += [self.state[y - 1][x] == player_id];
            if self.in_bounds((x, y + 1)):
                adjacents += [self.state[y + 1][x] == player_id];

        return True in adjacents;

    # Check if a piece placement is cornering
    # any pieces of the player proposing the move.
    def corner(self, player_id, placement):
        corners = [];
        # check the corner square from the placement
        for x, y in placement:
            if self.in_bounds((x + 1, y + 1)):
                corners += [self.state[y + 1][x + 1] == player_id];
            if self.in_bounds((x - 1, y -1)):
                corners += [self.state[y - 1][x - 1] == player_id];
            if self.in_bounds((x + 1, y - 1)):
                corners += [self.state[y - 1][x + 1] == player_id];
            if self.in_bounds((x - 1, y + 1)):
                corners += [self.state[y + 1][x - 1] == player_id];

        return True in corners;


# Player Class
# DC-Claire
class Player:
    def __init__(self, id, strategy):
        self.id = id # player's id
        self.pieces = [] # player's unused game piece, list of Pieces
        self.corners = set() # current valid corners on board
        self.strategy = strategy # player's strategy
        self.score = 0 # player's current score
        self.is_blocked = False

    # Add the player's initial pieces for a game
    def add_pieces(self, pieces):
        self.pieces = pieces;

    # Remove a player's Piece
    def remove_piece(self, piece):
        self.pieces = [p for p in self.pieces if p.id != piece.id];

    # Set the available starting corners for players
    def start_corner(self, p):
        self.corners = set([p])

    # Updates player information after placing a board Piece
    def update_player(self, piece, board):
        self.score += piece.size;
        for c in piece.corners:
            # Add the player's available corners
            if board.in_bounds(c) and not board.overlap([c]):
                self.corners.add(c);

    # Get a unique list of all possible placements
    def possible_moves(self, pieces, game):
        # Updates the corners of the player, in case the
        # corners have been covered by another player's pieces.
        locations = []
        t_counter = 0
        for i in range(12):
            for j in range(11):
                locations.append((i,j))
        
        self.corners = set([(x, y) for(x, y) in locations
                            if game.board.state[y][x] == '_']);
        # self.corners = set([(x, y) for(x, y) in self.corners
        #                     if game.board.state[y][x] == '_']);

        placements = [] # a list of possible placements
        visited = [] # a list placements (a set of points on board)

        # Check every available corner
        num = 0
        for cr in self.corners:
            # Check every available piece
            for sh in pieces:
                # Check every flip
                for flip in ["h", "v"]:
                    # Check every rotation
                    for rot in [0, 90, 180, 270]:
                        t_counter += 1
                        # Create a copy to prevent an overwrite on the original
                        candidate = copy.deepcopy(sh);
                        candidate.create(num, cr);
                        candidate.flip(flip);
                        candidate.rotate(rot);
                        # If the placement is valid and new
                        if game.valid_move(self, candidate.points):
                            if not set(candidate.points) in visited:
                                placements.append(candidate);
                                visited.append(set(candidate.points));
                                    
        # print(t_counter)
        return placements;

    def plausible_moves(self, pieces, game, cutoff, pid):
        placements = []
        for piece in pieces:
            possibles = self.possible_moves([piece], game)
            if possibles != []:
                for possible in possibles:
                    placements.append(possible)
                    if len(placements) == cutoff:
                        return placements
        return placements

    # Get the next move based off of the player's strategy
    def next_move(self, game):
        return self.strategy(self, game);


class Blokus:
    def __init__(self, players, board, all_pieces):
        self.players = players; 
        self.rounds = 0; 
        self.board = board; 
        self.all_pieces = all_pieces; 
        self.previous = 0;
        # counter for how many times the total available moves are the same by checking previous round
        self.repeat = 0; 
        self.win_player = 0; # winner

    # Check if a player's move is valid, including board bounds, pieces' overlap, adjacency, and corners.
    def valid_move(self, player, placement):
        if self.rounds < len(self.players):
            # Check for starting corner
            return not ((False in [self.board.in_bounds(pt) for pt in placement])
                        or self.board.overlap(placement)
                        or not (True in[(pt in player.corners) for pt in placement]));
        return not ((False in[self.board.in_bounds(pt) for pt in placement])
                    or self.board.overlap(placement));
                    # or self.board.adj(player.id, placement)
                    # or not self.board.corner(player.id, placement));

    # Play the game with the list of players sequentially until the
    # game ends (no more pieces can be placed for any player)
    def play(self):
        
        global Outcomes
        
        # t = time.time()
        
        # print(time.time()-t)
        # At the beginning of the game, it should
        # give the players their pieces and a corner to start.
        if self.rounds == 0: # set up starting corners and players' initial pieces
            max_x = self.board.ncol -1;
            max_y = self.board.nrow -1;
            starts = [(0, 0), (max_x, max_y), (0, max_y), (max_x, 0)];
            fl1 = random.sample(range(12),6)
            fl2 = random.sample(range(12),6)
            # fl2 = [0,1,4,5,8,10] # Fair draw
            # fl2 = [0,2,3,5,10,11] # Worst possible tiles for P1
            pl0=[]
            pl1=[]
            ap = list(self.all_pieces)
            for j in range(24):
                if j in fl1 or j-12 in fl2:
                    pl0.append(ap[j])
                else:
                    pl1.append(ap[j])
                    
            pl0 = random.sample(pl0[0:6],6)+random.sample(pl0[6:12],6)
            pl1 = random.sample(pl1[0:6],6)+random.sample(pl1[6:12],6)
                    
            # print(len(pl0),pl0)
            # print(len(pl1),pl1)
                    
            self.players[0].add_pieces(pl0)
            self.players[1].add_pieces(pl1)
        
        # print(time.time()-t)
        
        current = self.players[0]

        proposal = current.next_move(self); # get the next move based on
                                            # the player's strategy

        # print(time.time()-t)

        if proposal is not None: # if there a possible proposed move
            # check if the move is valid
            if self.valid_move(current, proposal.points):
                # update the board and the player status
                # print(time.time()-t)
                self.board.update(current.id, proposal.points);
                current.update_player(proposal, self.board);
                current.remove_piece(proposal); # remove used piece
                if self.players[0].id == 1:
                    render(self.board.state,self.board.state2,self.players[0].pieces,self.players[1].pieces)
                else:
                    render(self.board.state,self.board.state2,self.players[1].pieces,self.players[0].pieces)                            
                # print(time.time()-t)

            else: # end the game if an invalid move is proposed
                raise Exception("Invalid move by player "+ str(current.id));
        # put the current player to the back of the queue
        first = self.players.pop(0);
        self.players += [first];
        self.rounds += 1; # update game round

    def make_move(self, move, state):
        "Return a new BoardState reflecting move made from given board state."
        # make a copy of the given state to be updated
        newboard = copy.deepcopy(state)
        # get current player
        current = newboard.to_move;
        # update the board and the player status
        newboard._board.update(current.id, move.points);
        current.update_player(move, newboard._board);
        current.remove_piece(move); # remove used piece
        # put the current player to the back of the queue
        first = newboard.game.players.pop(0);
        newboard.game.players += [first];
        newboard.game.rounds += 1; # update game round
        # update newboard to_move
        newboard.to_move = newboard.game.players[0]
        return newboard

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        # find and return up to MovesToConsider possible moves as successors
        m = [(move, self.make_move(move, state))
                for move in state.to_move.plausible_moves(state.to_move.pieces, state.game, MovesToConsider, state.to_move.id)]
        return m

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        # if we have no moves left, it's effectively a final state
        return not state.to_move.plausible_moves(state.to_move.pieces, state.game, 1, state.to_move.id)

# This function will prompt the user for their piece
def piece_prompt(options):
    # Create an array with the valid piece names
    option_names = [str(x.id) for x in options];

    # Prompt the user for their choice
    print("\nIt's your turn! Select one of the following options:");
    choice = 0;
    
    # While they haven't chosen a valid piece...
    while (choice != 2):
        print("     1 - See available pieces.");
        print("     2 - Choose a piece.");

        # Get their choice. If they don't enter an integer, handle the exception
        try:
            choice = int(input("Choice: "));
        except:
            # Do nothing; choice = 0, so the user will be prompted again
            pass;

        # Once they've entered a choice, perform the desired actions
        print("");
        if (choice == 1): # Print the available pieces
            for x in option_names:
                print(x);
            print("\nSelect one of the following options:");

        elif (choice == 2): # Request the user's piece
            piece = input("Choose a piece: ");
            print("");
            if piece in option_names:  # If the piece name is valid, retrieve the piece object
                i = option_names.index(piece);
                piece = options[i];
            else:
                print("INVALID PIECE. Please try again:");
                choice = 0;

        else: # If the user doesn't request the list of pieces or choose a piece
            print("INVALID CHOICE. Please try again:");

    # Once they've chosen a piece...
    return piece;

# This function will prompt the user for their placement
def placement_prompt(possibles):
    choice = -1; # An invalid "choice" to start the following loop

    # While the user hasn't chosen a valid placment...
    while (choice < 1 or choice > len(possibles)):
        count = 1; # Used to index each placement; initialized to 1
        # Prompt the user for their placement
        print("Select one of the following placements:")
        for x in possibles:
            print("     " + str(count) + " - " + str(x.points));
            count += 1;

        # See if the user enters an integer; if they don't, handle the exception
        try:
            choice = int(input("Choose a placement: "));
        except:
            # Do nothing; if the user doesn't enter an integer, they will be prompted again
            pass;
        print("");

    # Once they've made a valid placement...
    placement = possibles[choice - 1];
    return placement;    

# Random Strategy: choose an available piece randomly
# DC
def Random_Player(player, game):
    options = [p for p in player.pieces];
    while len(options) > 0: # if there are still possible moves
        piece = random.choice(options);
        possibles = player.possible_moves([piece], game);
        if len(possibles) != 0: # if there is possible moves
            return random.choice(possibles);
        else: # no possible move for that piece
            options.remove(piece); # remove it from the options
    return None; # no possible move left

# Tyler - AI implementation, created a better opponent to test against
# Largest Strategy: play a random available move for the largest piece possible
def Largest_Player(player, game):
    # pieces are already in order from largest to smallest
    # iterate through and make the first possible move
    for p in player.pieces:
        possibles = player.possible_moves([p], game)
        # print('#Moves: ' + str(len(possibles)))
        if len(possibles) != 0: # if there is possible moves
            return random.choice(possibles);
    # if no possible moves are found, return None
    return None

def Greedy_Player_v2(player, game):
    # pieces are already in order from largest to smallest
    # iterate through and make the first possible move
    
    
    turn_number = (TotalStartingPieces - len(player.pieces) + 1)

    if turn_number ==3:
        print ('Game eval start: Turn ' + str(turn_number))
    if turn_number<3:
        move = Largest_Player(player,game)
        return move
    elif turn_number<5:
        move = Greedy_Player(player,game)
        return move        
    else:
    
        all_possibles = []
        moveeval= []
        best_index = 0
        best_value = -1000
        pcounter = -1
        
        maxlen = max(3,turn_number-2)
        
        game_copy = copy.deepcopy(game)
        state = BoardState(game_copy)
        
        if player.id == 1:    
            this_player = state.p1
            other_player = state.p2
        else:
            this_player = state.p2
            other_player = state.p1
        
        temp_possibles1 = player.possible_moves(this_player.pieces, game_copy)
        temp_possibles2 = player.possible_moves(other_player.pieces, game_copy)
        
        temp_set1 = [[t.id,set(t.points)] for t in temp_possibles1]
        temp_set2 = [[t.id,set(t.points)] for t in temp_possibles2]
        
        t_id1 = []
        t_id2 = []
        
        for t in temp_set1:
            if t[0] not in t_id1:
                t_id1.append(t[0])

        for t in temp_set2:
            if t[0] not in t_id2:
                t_id2.append(t[0])        
        
        for p in player.pieces[0:maxlen]:
            pcounter +=1
            possibles = player.possible_moves([p], game)
            all_possibles += possibles
            temp_counter = 0
            # print('#Moves: ' + str(len(possibles)))
            if len(possibles) != 0: # if there is possible moves
                
                for m in possibles:
                    temp_counter +=1
                    # if temp_counter == 1:
                    #     print(m.points)                    
                    # print(this_player.pieces)
                    # print(p)
                    # time.sleep(10)
                    # print(this_player.pieces, p)
                    # new_pieces = copy.deepcopy(this_player.pieces).pop(pcounter)
                    
                    p1set = set()
                    p2set = set()
                    
                    adj_value = 0
                    t_adj_value1 = 0
                    t_adj_value2 = 0
                    

                    
                    # Nice improvement where available moves are updated iteratively instead of re-generating with every move.
                    for t in temp_set1:
                        if t[0] != p.id and len(set(m.points).intersection(t[1]))==0:
                            p1set = p1set | t[1]

                    for t in temp_set2:
                        if len(set(m.points).intersection(t[1]))==0:
                            p2set = p2set | t[1]
                            
                    for t0 in t_id1:
                        tp1set = set()
                        t1set = set()
                        for t in temp_set1:
                            if t[0] != p.id and t[0] != t0 and len(set(m.points).intersection(t[1]))==0:
                                tp1set = tp1set | t[1]
                            if t[0] == t0 and t[0] != p.id and len(set(m.points).intersection(t[1]))==0:
                                t1set = t1set | t[1]
                                
                        t_adj_value_temp1 = len(t1set.difference(tp1set))
                        t_adj_value1 += max(0,t_adj_value_temp1-5)
                                
                    for t0 in t_id2:
                        tp2set = set()
                        t2set = set()
                        for t in temp_set2:
                            if t[0] != t0 and len(set(m.points).intersection(t[1]))==0:
                                tp2set = tp2set | t[1]
                            if t[0] == t0 and len(set(m.points).intersection(t[1]))==0:
                                t2set = t2set | t[1]

                        t_adj_value_temp2 = len(t2set.difference(tp2set))
                        t_adj_value2 += max(0,t_adj_value_temp2-5)                        

                    p1u = p1set.difference(p2set)
                    p2u = p2set.difference(p1set)
                            
                    # print(len(p1set),len(p2set), len(p1set.difference(p2set)),len(p2set.difference(p1set)))
                    
                    # print(t_adj_value1, t_adj_value2)
                    moveeval.append(len(p1u)-len(p2u)-t_adj_value1+t_adj_value2)
                    # print(len(temp_possibles1),len(temp_possibles2))
                    

        if len(all_possibles)>0:
                
            for i in range(len(all_possibles)):
                if moveeval[i]>=best_value:
                   best_index = i
                   best_value = moveeval[i]
                        
                    # print(best_index)
                        
            return all_possibles[best_index]
                # return random.choice(possibles);
        # if no possible moves are found, return None
        return None


def Greedy_Player(player, game):
    # pieces are already in order from largest to smallest
    # iterate through and make the first possible move
    
    
    turn_number = (TotalStartingPieces - len(player.pieces) + 1)

    if turn_number ==3:
        print ('Game eval start: Turn ' + str(turn_number))
    if turn_number<3:
        move = Largest_Player(player,game)
        return move
    else:
    
        all_possibles = []
        moveeval= []
        best_index = 0
        best_value = -1000
        pcounter = -1
        
        maxlen = max(3,turn_number-2)
        
        game_copy = copy.deepcopy(game)
        state = BoardState(game_copy)
        
        if player.id == 1:    
            this_player = state.p1
            other_player = state.p2
        else:
            this_player = state.p2
            other_player = state.p1
        
        temp_possibles1 = player.possible_moves(this_player.pieces, game_copy)
        temp_possibles2 = player.possible_moves(other_player.pieces, game_copy)
        
        temp_set1 = [[t.id,set(t.points)] for t in temp_possibles1]
        temp_set2 = [[t.id,set(t.points)] for t in temp_possibles2]
        
        
        for p in player.pieces[0:maxlen]:
            pcounter +=1
            possibles = player.possible_moves([p], game)
            all_possibles += possibles
            temp_counter = 0
            # print('#Moves: ' + str(len(possibles)))
            if len(possibles) != 0: # if there is possible moves
                
                for m in possibles:

                    p1set = set()
                    p2set = set()                 
                    
                    # Nice improvement where available moves are updated iteratively instead of re-generating
                    for t in temp_set1:
                        if t[0] != p.id and len(set(m.points).intersection(t[1]))==0:
                            p1set = p1set | t[1]

                    for t in temp_set2:
                        if len(set(m.points).intersection(t[1]))==0:
                            p2set = p2set | t[1]
                     
                    p1u = p1set.difference(p2set)
                    p2u = p2set.difference(p1set)
                            
                    # print(len(p1set),len(p2set), len(p1set.difference(p2set)),len(p2set.difference(p1set)))
                    
                    moveeval.append(len(p1u)-len(p2u))
                    # print(len(temp_possibles1),len(temp_possibles2))
                    

        if len(all_possibles)>0:
                
            for i in range(len(all_possibles)):
                if moveeval[i]>=best_value:
                   best_index = i
                   best_value = moveeval[i]
                        
                    # print(best_index)
                        
            return all_possibles[best_index]
                # return random.choice(possibles);
        # if no possible moves are found, return None
        return None

# Human Strategy: choose an available piece and placement based on user input
def Human_Player(player, game):
    options = [p for p in player.pieces];
    while len(options) > 0: # if there are still possible moves
        piece = piece_prompt(options);
        possibles = player.possible_moves([piece], game);
        if len(possibles) != 0: # if there is possible moves
            return placement_prompt(possibles);
        else: # no possible move for that piece
            options.remove(piece); # remove it from the options
    return None; # no possible move left


# Human Strategy: choose an available piece and placement based on user input
def Human_Player_Fast(player, game):
    turn_number = (TotalStartingPieces - len(player.pieces) + 1)
    if turn_number<6:
        move = Largest_Player(player,game)
        return move

    else:

        
        # Fix this so pieces that cannot be placed don't show up among the options
        options = [p for p in player.pieces];
        while len(options) > 0: # if there are still possible moves
            piece = piece_prompt(options);
            possibles = player.possible_moves([piece], game);
            if len(possibles) != 0: # if there is possible moves
                return placement_prompt(possibles);
            else: # no possible move for that piece
                options.remove(piece); # remove it from the options
        return None; # no possible move left




# Tyler - AI implementation, based off of BoardState from mancala.py
class BoardState:
    """Holds one state of the Blokus board, used to generate successors."""
    def __init__(self, game=None):
        self.game = game
        self.p1 = [p for p in game.players if p.id == 1][0]
        self.p2 = [p for p in game.players if p.id == 2][0]
        # to_move keeps track of the player whose turn it is to move
        self.to_move = game.players[0]
        self._board = game.board

# Play a round of blokus (all players move), then print board.
def play_blokus(blokus):
    # Make one premature call to blokus.play(), initializes board.
    blokus.play();
    
    a=0
    s=0
    e=0

    # Termination criteria is two consecutive passes (total score did not change)
    # Should this be part of main class?
    
    while e<2:
        old_s = s
        s = 0
        blokus.play()
        for player in blokus.players:
            s+= player.score
        
        if old_s == s:
            e+=1
        else:
            e=0
        
        time.sleep(TS)

# Run a blokus game with two players.
def multi_run(repeat, one, two):
    # Scores for each player
    winner = {1: 0, 2: 0};
    TotalMoveTimes = []

    # Play as many games as indicated by param repeat
    for i in range(repeat):
        print("\nGame", (i + 1), ": Begin!\n")
        global MoveTimes
        MoveTimes = [] # Reset
        order = []; # Reset
        P1 = Player(1, one) # first player
        P2 = Player(2, two) # second player
        
        # Tyler - AI implementation
        # add pieces in order from largest to smallest
        all_pieces = [piece.C0(),piece.C1(),piece.D0(),piece.Z0(),piece.W0(),piece.X0(),piece.F0(),piece.F1(),piece.F2(),piece.F3(),piece.F4(),piece.F5(),\
                      piece.I(),piece.L(),piece.V(),piece.W(),piece.F(),piece.X(),piece.N(),piece.Y(),piece.U(),piece.P(),piece.T(),piece.Z()];

        board = Board(11, 12);
        order = [P1, P2];
        blokus = Blokus(order, board, all_pieces);
        play_blokus(blokus);

        # End of game display.
        if blokus.players[0].id == 1:
            render(blokus.board.state,blokus.board.state2,blokus.players[0].pieces,blokus.players[1].pieces)
        else:
            render(blokus.board.state,blokus.board.state2,blokus.players[1].pieces,blokus.players[0].pieces)            
        blokus.play();
        plist = sorted(blokus.players, key = lambda p: p.id);
        gscores = []
        for player in plist:
            gscores.append(player.score)
            print("Player "+ str(player.id) + " score "+ str(player.score) + ": "
                  + str([sh.id for sh in player.pieces]));
            for sh in player.pieces:
                if sh.id in Names:
                    MCounts[Names.index(sh.id)]+=1
        print("Game end.");
        time.sleep(5*TS)
        # clearGUI()
        TotalMoveTimes.append(MoveTimes)
        
        rn = gscores[0]-gscores[1]
        
        Scores1.append(gscores[0])
        Scores2.append(gscores[1])
        
        if rn>0:
            Outcomes.append(1)
        elif rn<0:
            Outcomes.append(-1)
        else:
            Outcomes.append(0)

    # Tyler - AI implementation, calculate stats to evaluate AI performance
    # used to calculate game stats
    averages = []
    averages_after_two = []
    slowests = []
    fastests = []
    

    
    outcome_switcher = {
        1: "W",
        0: "T",
        -1: "L"
    }

    # if len(TotalMoveTimes) > 0:
    #     # print each individual game's stats
    #     print("\n========================= TIME ANALYSIS =========================")
    #     for game in TotalMoveTimes:
    #         # this line should include the outcome
    #         game_index = TotalMoveTimes.index(game)
    #         outcome_number = Outcomes[game_index]
    #         outcome_letter = outcome_switcher.get(outcome_number)
    #         score = Scores[game_index]
    #         print("\nGame " + str(game_index + 1) + " (" + outcome_letter + ", " + str(score) + ")")
    #         print("Move Times:", game)
    #         average = round(np.mean(game), 2)
    #         averages.append(average)
    #         print("Average Move Time: ", average)
    #         average_after_two = round(np.mean(game[2:]), 2)
    #         averages_after_two.append(average_after_two)
    #         print("    After 2 Moves:   ", average_after_two)
    #         slowest = np.amax(game)
    #         slowests.append(slowest)
    #         print("Slowest Move:      ", slowest)
    #         fastest = np.amin(game)
    #         fastests.append(fastest)
    #         print("Fastest Move:      ", fastest)

    # print stats across all games
    print("\n================== STATISTICS ACROSS ALL GAMES ==================\n")
    games_played = len(Outcomes)
    print("Games Played:      ", games_played)
    games_won = Outcomes.count(1)
    print("Games Won:         ", games_won)
    print("Games Lost:        ", Outcomes.count(-1))
    print("Games Tied:        ", Outcomes.count(0))
    print("Win Rate:          " + str(round((games_won / games_played * 100), 2)) + "%\n")

    print("Average Score P1:     " + str(round(np.mean(Scores1),1)))
    print("Average Score P2:     " + str(round(np.mean(Scores2),1)) + "\n")
    
    print("Missing pieces:     " + str(Names))
    print("                    " + str(MCounts))
    # print("Highest Score:    ", np.amax(Scores))
    # print("Lowest Score:     ", np.amin(Scores), "\n")

    # print("Average Move Time: ", round(np.mean(averages), 2))
    # print("  After 2 Moves:   ", round(np.mean(averages_after_two), 2))
    # print("Slowest Move:      ", np.amax(slowests))
    # print("  Average Slowest: ", round(np.mean(slowests), 2))
    # print("Fastest Move:      ", np.amin(fastests))
    # print("  Average Fastest: ", round(np.mean(fastests), 2), "\n")

def main():
    # NOTE: Jeffbot allows the other (human) player to move first because he
    # is polite (and hard-coded that way)
    # multi_run(Games, Greedy_Player, Greedy_Player_v2);
    multi_run(Games, Greedy_Player_v2, Greedy_Player_v2);

if __name__ == '__main__':
    main();


