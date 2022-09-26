# This file has functions modified from the blokus implementation at
# https://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1305&context=cpesp

'''
Isle of Cats AI
This code implements Isle of Cats family game, using the code-base from poly_ai.py. 
It implements all rules except lessons, and has a greedy player which is decently competitive.

It has been adapted from Blokus code, and contains some hacks that makes it illogical 
(e.g. referring to all points on the board as 'corners' in the piece placement code)

'''

import sys
import math
import random
import copy
import piece_cats as piece
from gui_cats import *
import copy
import operator
import time
import numpy as np
from cats_score import score_board
from cats_score import score_board_0

# cutoff depth for alphabeta minimax search (default 2)
Depth = 1
# number of successor states returned (default 4)
MovesToConsider = 4
# change to adjust the number of games played (defualt 10)
Games = 1
TS = 0

Grid = \
    [[0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0]]

Grid2 = [[0,0,0,0,0,0,0,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,1,1,0,0,0,0,0],
    [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,2,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0],
    [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,6,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0]]
    
Grid3 = \
    [[0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0]]

Grid4 = [\
    [0,0,0,0,0,0,0,3,3,3,3,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,3,3,3,3,3,3,3,1,1,1,1,1,6,0,0,0,0,0],
    [0,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,0,0,0],
    [2,2,2,2,1,5,5,5,5,5,5,1,1,1,1,1,6,6,6,6,7,0],
    [2,2,2,2,1,5,5,5,5,5,5,1,1,1,1,1,6,6,6,6,7,7],
    [2,2,2,2,1,5,5,5,5,5,5,1,1,1,1,1,6,6,6,6,7,0],
    [0,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,0,0,0],
    [0,0,0,0,4,4,4,4,4,4,4,1,1,1,1,1,6,0,0,0,0,0],
    [0,0,0,0,0,0,0,4,4,4,4,1,1,1,1,0,0,0,0,0,0,0]]

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

        self.state = [[0] * ncol for i in range(nrow)];
        self.state2 = [[0] * ncol for i in range(nrow)];
        self.state3 = copy.deepcopy(Grid4); # Rooms on the board, also signifies valid placements
        self.state4 = copy.deepcopy(Grid2); # Resources on the board
        self.adj_state = [[0] * ncol for i in range(nrow)];
        self.treasure = 0
        
    def update(self, player_id, placement,color):
        
        #print(self.state)
        #print(self.state2)
        maxval = max([max(s) for s in self.state2])
        for row in range(self.nrow):
            for col in range(self.ncol):
                if(col, row) in placement:
                    self.state[row][col] = color;
                    self.state2[row][col] = maxval+1
                    if self.state4[row][col]-1 == color:
                        self.treasure = 1

    # Check if the point (y, x) is within the board's bound
    def in_bounds(self, point):
        y = point[1]
        x = point[0]
        return 0<= point[0] < self.ncol and 0<= point[1] < self.nrow and self.state3[y][x]>0; ## Add condition for actually being on the board

    # Check if a piece placement overlap another piece on the board
    def overlap(self, placement):
        return False in[(self.state[y][x] == 0) for x, y in placement]


    # Checks if a piece placement is adjacent to any square on
    # the board which are occupied by the player proposing the move.
    def adj(self, placement):
        adjacents = [];
        # Check left, right, up, down for adjacent square
        for x, y in placement:
            if self.in_bounds((x + 1, y)):
                adjacents += [self.state[y][x + 1] > 0];
            if self.in_bounds((x -1, y)):
                adjacents += [self.state[y][x - 1] > 0];
            if self.in_bounds((x, y -1)):
                adjacents += [self.state[y - 1][x] > 0];
            if self.in_bounds((x, y + 1)):
                adjacents += [self.state[y + 1][x] > 0];

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
class Player:
    def __init__(self, id, board, strategy):
        self.id = id # player's id
        self.pieces = [] # player's unused game piece, list of Pieces
        self.corners = set() # current valid corners on board
        self.strategy = strategy # player's strategy
        self.board = board
        self.score = 0 # player's current score
        self.potential = 0
        self.is_blocked = False

    # Add the player's initial pieces for a game
    def add_pieces(self, pieces):
        self.pieces = pieces;

    # Remove a player's Piece
    def remove_piece(self, piece):
        self.pieces = [p for p in self.pieces if p.id != piece.id];


    # Updates player information after placing a board Piece
    def update_player(self, piece, board):
        # self.score += piece.size;
        
        grid = copy.deepcopy(self.board.state)
        grid2 = copy.deepcopy(self.board.state2)
        grid3 = self.board.state3
        grid4 = self.board.state4
        
        self.score, self.potential = score_board(grid, grid2, grid3, grid4, 2)
        # Score for rooms and rats are counted as negatives
        self.score -= 54
        
        
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
        # Why is this hardcoded?
        for i in range(22):
            for j in range(9):
                locations.append((i,j))
        
        self.free_spaces = set([(x, y) for(x, y) in locations
                            if self.board.state[y][x] == 0 and self.board.state3[y][x]>0]);
        
        # print(self.free_spaces)
        # self.corners = set([(x, y) for(x, y) in self.corners
        #                     if game.board.state[y][x] == '_']);

        placements = [] # a list of possible placements
        colors = []
        visited = [] # a list placements (a set of points on board)

        # Check every available corner
        num = 0
        for cr in self.free_spaces:
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
                                colors.append(sh.color)
                                # print('Piece:' + str(sh.color))
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
        if self.board.treasure == 0:    
            return self.strategy(self, game, 1)
        else:
            return self.strategy(self, game, 0)


class Blokus:
    def __init__(self, players, board, all_pieces):
        self.players = players; 
        self.rounds = 0; 
        self.board = board; 
        self.all_pieces = all_pieces; 
        self.all_pieces = random.sample(self.all_pieces,len(all_pieces))
        self.pieces = []
        self.previous = 0;
        # counter for how many times the total available moves are the same by checking previous round
        self.repeat = 0; 
        self.treasures = [piece.TR1(6),piece.TR2(6),piece.TR3(6),piece.TR4(6)]
        self.win_player = 0; # winner

    # Check if a player's move is valid, including board bounds, pieces' overlap, adjacency, and corners.
    def valid_move(self, player, placement):
        if ((False in [player.board.in_bounds(pt) for pt in placement]) or player.board.overlap(placement)) or \
            ((self.rounds >= len(self.players) or player.board.treasure>0) and player.board.adj(placement) == False):
            return False
        else:
            return True
        
    # Remove a player's Piece
    def remove_piece(self, piece):
        self.pieces = [p for p in self.pieces if p.id != piece.id];

    def remove_treasure(self, piece):
        self.treasures = [p for p in self.treasures if p.id != piece.id];

    # Play the game with the list of players sequentially until the
    # game ends (no more pieces can be placed for any player)
    def play(self):
        
        global Outcomes
 
        current = self.players[0]

        if self.players[0].id == 1:
            firstp = self.players[0]
            secondp = self.players[1]
        else:
            secondp = self.players[0]
            firstp = self.players[1]            
 
        # t = time.time()
        
        # Game is played over 5 days, for each day, add 8 pieces to common pool for players to choose between.
        # Repeat 5 times.
        pcounter = 0
        if self.rounds%8 == 0 and self.rounds<40: 
            while pcounter<8:
                if self.all_pieces[0].id[0:2]!='RT':
                    self.pieces.append(self.all_pieces[0])
                    pcounter+=1
                else:
                    self.treasures.append(self.all_pieces[0])
                self.all_pieces.pop(0)
                
            render([firstp.board.state,firstp.board.state2,firstp.board.state3,firstp.board.state4],\
                       [secondp.board.state,secondp.board.state2,secondp.board.state3,firstp.board.state4],self.pieces,self.pieces)     
            # time.sleep(TS)
        
       

        proposal = current.next_move(self); # get the next move based on
                                            # the player's strategy

        # print(proposal)


        # print(time.time()-t)

        if proposal is not None: # if there a possible proposed move
            color = proposal.color
            # check if the move is valid
            if self.valid_move(current, proposal.points):
                # update the board and the player status
                # print(time.time()-t)
                current.board.update(current.id, proposal.points,color);
                current.update_player(proposal, self.board);
                self.remove_piece(proposal); # remove used piece
                render([firstp.board.state,firstp.board.state2,firstp.board.state3,firstp.board.state4],\
                       [secondp.board.state,secondp.board.state2,secondp.board.state3,firstp.board.state4],self.pieces,self.pieces)                     
                # print(time.time()-t)

            else: # end the game if an invalid move is proposed
                raise Exception("Invalid move by player "+ str(current.id));
        # put the current player to the back of the queue

        if current.board.treasure > 0: # If the player obtained a treasure, give him a chance to place it.
            
            proposal = current.next_move(self); # get the next move based on
                                            # the player's strategy

            # print(time.time()-t)
    
            if proposal is not None: # if there a possible proposed move
                color = proposal.color
                # check if the move is valid
                if self.valid_move(current, proposal.points):
                    # update the board and the player status
                    # print(time.time()-t)
                    current.board.update(current.id, proposal.points,color);
                    current.update_player(proposal, self.board);
                    if proposal.id[0:2] == 'RT':
                        self.remove_treasure(proposal);
                        
                    # self.remove_piece(proposal); # remove used piece
                    render([firstp.board.state,firstp.board.state2,firstp.board.state3,firstp.board.state4],\
                           [secondp.board.state,secondp.board.state2,secondp.board.state3,firstp.board.state4],self.pieces,self.pieces)                     
                    # print(time.time()-t)
    
                else: # end the game if an invalid move is proposed
                    raise Exception("Invalid move by player "+ str(current.id));
            # put the current player to the back of the queue
           
        current.board.treasure = 0
          
        # Round logic is slightly flawed. Game continues as long as both players have not passed.
        # One player can play more than four turns in a row if the other player passes.

        if self.rounds%8 != 7:
            first = self.players.pop(0);
            self.players += [first];
        else:
            for piece in self.pieces:
                self.all_pieces.append(piece)
            self.pieces = []
            self.all_pieces = random.sample(self.all_pieces,len(self.all_pieces))
        
                
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
    print (option_names)
    
    piece = input("Choose a piece: ");
    print("");
    try: 
        i = int(piece)
        piece = options[i-1]
    except:
        if piece in option_names:  # If the piece name is valid, retrieve the piece object
            i = option_names.index(piece);
            piece = options[i];
        else:
            print("INVALID PIECE. Please try again:");
            choice = 0;
    

    # Once they've chosen a piece...
    return piece;

# This function will prompt the user for their placement
def placement_prompt(possibles):
    choice = -1; # An invalid "choice" to start the following loop

    exclude_list=[]

    # While the user hasn't chosen a valid placment...
    while (choice < 1 or choice > len(possibles)):
        # print(exclude_list)
        count = 1; # Used to index each placement; initialized to 1
        # Prompt the user for their placement
        print("Select one of the following placements:")
        for x in possibles:
            if x not in exclude_list:
                # print(x)
                print("     " + str(count) + " - " + str(x.points));
            count += 1;

        # See if the user enters an integer; if they don't, handle the exception
        try:
            this_input = input("Choose a placement: ")
            # print(this_input,'-' in this_input)
            if '-' in this_input:
                x,y = this_input.split('-')
                this_point = (int(x)-1,int(y)-1)
                # print('P: ', this_point)
                for p in possibles:
                    if this_point not in p.points:
                        exclude_list.append(p)
            else:
                choice = int(this_input);
        except:
            # Do nothing; if the user doesn't enter an integer, they will be prompted again
            pass;
        print("");

    # Once they've made a valid placement...
    placement = possibles[choice - 1];
    return placement;    

# Random Strategy: choose an available piece randomly
def Random_Player(player, game, oval = 1):
    if oval == 1:
        options = [p for p in game.pieces];
    else:
        options = [p for p in game.treasures]
    while len(options) > 0: # if there are still possible moves
        piece = random.choice(options);
        # Function returns a piece so does not need to return the color as well (possibles[x].color)
        possibles,colors = player.possible_moves([piece], game);
        if len(possibles) != 0: # if there is possible moves
            m = random.randint(0,len(possibles)-1)
            return possibles[m],colors[m]
        else: # no possible move for that piece
            options.remove(piece); # remove it from the options
    return None; # no possible move left

# Greedy Strategy: choose an available piece randomly based on own board only
def Greedy_Player(player, game, oval = 1):
    if oval == 1:
        options = [p for p in game.pieces];
    else:
        options = [p for p in game.treasures]
        # print(options)
    scores = []
    all_possibles = []
    debug = []
    maxval = max([max(s) for s in game.players[0].board.state2])
    for piece in options:
        # print('Piece:', piece)
        possibles = player.possible_moves([piece], game);
        # print(len(possibles))
        if len(possibles) != 0: # if there is possible moves
            # print(len(possibles),possibles[m].points,possibles[m].color)
            # print(game.players[0].board.state,game.players[0].board.state2,game.players[0].board.state3)
            for m in range(len(possibles)):
                grid = copy.deepcopy(game.players[0].board.state)
                grid2 = copy.deepcopy(game.players[0].board.state2)
                grid3 = game.players[0].board.state3
                grid4 = game.players[0].board.state4
                this_color = possibles[m].color
                
                # Should make a copy of the state and use the update function instead
                for (p0,p1) in possibles[m].points:
                    grid[p1][p0]=this_color
                    grid2[p1][p0] = maxval+1
                
                this_score, fam_dummy = score_board(grid, grid2, grid3, grid4)
                # debug.append(fam_dummy)
                scores.append(this_score)
                all_possibles.append(possibles[m])
            

        else: # no possible move for that piece
            options.remove(piece); # remove it from the options

    max_score = -1000
    if len(all_possibles)>0:
        for a in range(len(all_possibles)):
            if scores[a]>max_score:
                max_index = a
                max_score = scores[a]
        # print(all_possibles[max_index].id,all_possibles[max_index].color,round(scores[a],0),sorted(debug[a],reverse=True))
        return all_possibles[max_index]
    else:
        return None; # no possible move left


# Greedy Strategy: choose an available piece randomly based on own board only
def Greedy_Player_v0(player, game, oval = 1):
    if oval == 1:
        options = [p for p in game.pieces];
    else:
        options = [p for p in game.treasures]
        # print(options)
    scores = []
    all_possibles = []
    debug = []
    maxval = max([max(s) for s in game.players[0].board.state2])
    for piece in options:
        # print('Piece:', piece)
        possibles = player.possible_moves([piece], game);
        # print(len(possibles))
        if len(possibles) != 0: # if there is possible moves
            # print(len(possibles),possibles[m].points,possibles[m].color)
            # print(game.players[0].board.state,game.players[0].board.state2,game.players[0].board.state3)
            for m in range(len(possibles)):
                grid = copy.deepcopy(game.players[0].board.state)
                grid2 = copy.deepcopy(game.players[0].board.state2)
                grid3 = game.players[0].board.state3
                grid4 = game.players[0].board.state4
                this_color = possibles[m].color
                
                # Should make a copy of the state and use the update function instead
                for (p0,p1) in possibles[m].points:
                    grid[p1][p0]=this_color
                    grid2[p1][p0] = maxval+1
                
                this_score, fam_dummy = score_board_0(grid, grid2, grid3, grid4)
                # debug.append(fam_dummy)
                scores.append(this_score)
                all_possibles.append(possibles[m])
            

        else: # no possible move for that piece
            options.remove(piece); # remove it from the options

    max_score = -1000
    if len(all_possibles)>0:
        for a in range(len(all_possibles)):
            if scores[a]>max_score:
                max_index = a
                max_score = scores[a]
        # print(all_possibles[max_index].id,all_possibles[max_index].color,round(scores[a],0),sorted(debug[a],reverse=True))
        return all_possibles[max_index]
    else:
        return None; # no possible move left


# Greedy Strategy: Converge the estimated potential to the actual score as the game progresses. No significant improvement.
def Greedy_Player_v3(player, game, oval = 1):
    if oval == 1:
        options = [p for p in game.pieces];
    else:
        options = [p for p in game.treasures]
        # print(options)
    progress = min(1,int(game.rounds/2)/20)
    scores = []
    all_possibles = []
    debug = []
    maxval = max([max(s) for s in game.players[0].board.state2])
    for piece in options:
        # print('Piece:', piece)
        possibles,colors = player.possible_moves([piece], game);
        # print(len(possibles))
        if len(possibles) != 0: # if there is possible moves
            # print(len(possibles),possibles[m].points,possibles[m].color)
            # print(game.players[0].board.state,game.players[0].board.state2,game.players[0].board.state3)
            for m in range(len(possibles)):
                grid = copy.deepcopy(game.players[0].board.state)
                grid2 = copy.deepcopy(game.players[0].board.state2)
                grid3 = game.players[0].board.state3
                grid4 = game.players[0].board.state4
                this_color = possibles[m].color
                
                # Should make a copy of the state and use the update function instead
                for (p0,p1) in possibles[m].points:
                    grid[p1][p0]=this_color
                    grid2[p1][p0] = maxval+1
                
                this_score, this_potential = score_board(grid, grid2, grid3, grid4, 0)
                # debug.append(fam_dummy)
                scores.append((1-progress)*this_potential+progress*this_score)
                all_possibles.append(possibles[m])
            

        else: # no possible move for that piece
            options.remove(piece); # remove it from the options

    max_score = -1000
    if len(all_possibles)>0:
        for a in range(len(all_possibles)):
            if scores[a]>max_score:
                max_index = a
                max_score = scores[a]
        # print(all_possibles[max_index].id,all_possibles[max_index].color,round(scores[a],0),sorted(debug[a],reverse=True))
        return all_possibles[max_index]
    else:
        return None; # no possible move left

# Greedy Strategy: choose an available piece randomly based on own board only
def Greedy_Player_v2(player, game, oval = 1):
    if oval == 1:
        options = [p for p in game.pieces];
    else:
        # Opponent scores don't matter for treasures as they won't be available to the other player
        move = Greedy_Player(player, game, oval)
        return move
        
        # options = [p for p in game.treasures]
        # print(options)
    scores = []
    all_possibles = []
    debug = []
    p_scores = []
    maxval = max([max(s) for s in game.players[0].board.state2])

    grid = copy.deepcopy(game.players[1].board.state)
    grid2 = copy.deepcopy(game.players[1].board.state2)
    grid3 = game.players[1].board.state3
    grid4 = game.players[1].board.state4
    base_score, fam_dummy = score_board(grid, grid2, grid3, grid4)
    
    # Estimate opportunity score for the current player for selected piece. Small or no improvement.
    for piece in options:
        # print('Piece:', piece)
        possibles,colors = game.players[1].possible_moves([piece], game);
        max_pscore = base_score
        
        # print(len(possibles))
        if len(possibles) != 0: # if there is possible moves
            # print(len(possibles),possibles[m].points,possibles[m].color)
            # print(game.players[0].board.state,game.players[0].board.state2,game.players[0].board.state3)
            for m in range(len(possibles)):
                grid = copy.deepcopy(game.players[1].board.state)
                grid2 = copy.deepcopy(game.players[1].board.state2)
                grid3 = game.players[1].board.state3
                grid4 = game.players[1].board.state4
                this_color = possibles[m].color
                
                # Updating board state locally                
                # Should make a copy of the state and use the update function instead to allow search
                for (p0,p1) in possibles[m].points:
                    grid[p1][p0]=this_color
                    grid2[p1][p0] = maxval+1
                
                this_score, fam_dummy = score_board(grid, grid2, grid3, grid4)
                if this_score > max_pscore:
                    max_pscore = this_score
        
        p_scores.append(max_pscore)
        
    # print(p_scores)

    c = 0

    for piece in options:
        # print('Piece:', piece)
        possibles,colors = player.possible_moves([piece], game);
        # print(len(possibles))
        if len(possibles) != 0: # if there is possible moves
            # print(len(possibles),possibles[m].points,possibles[m].color)
            # print(game.players[0].board.state,game.players[0].board.state2,game.players[0].board.state3)
            for m in range(len(possibles)):
                grid = copy.deepcopy(game.players[0].board.state)
                grid2 = copy.deepcopy(game.players[0].board.state2)
                grid3 = game.players[0].board.state3
                grid4 = game.players[0].board.state4
                this_color = possibles[m].color
                
                # Updating board state locally                
                # Should make a copy of the state and use the update function instead to allow search
                for (p0,p1) in possibles[m].points:
                    grid[p1][p0]=this_color
                    grid2[p1][p0] = maxval+1
                
                this_score, fam_dummy = score_board(grid, grid2, grid3, grid4)
                debug.append(fam_dummy)
                scores.append(this_score-p_scores[c])
                all_possibles.append(possibles[m])
                

            

        else: # no possible move for that piece
            options.remove(piece); # remove it from the options

        c+=0

    max_score = -1000
    if len(all_possibles)>0:
        for a in range(len(all_possibles)):
            if scores[a]>max_score:
                max_index = a
                max_score = scores[a]
        # print(all_possibles[max_index].id,all_possibles[max_index].color,round(scores[a],0),sorted(debug[a],reverse=True))
        return all_possibles[max_index]
    else:
        return None; # no possible move left


# Human Strategy: choose an available piece and placement based on user input
def Human_Player(player, game, oval = 1):
    if oval == 1:
        options = [p for p in game.pieces];
    else:
        options = [p for p in game.treasures]
        # print(options)
    while len(options) > 0: # if there are still possible moves
        piece = piece_prompt(options);
        possibles = player.possible_moves([piece], game);
        if len(possibles) != 0: # if there is possible moves
            return placement_prompt(possibles);
        else: # no possible move for that piece
            options.remove(piece); # remove it from the options
    return None; # no possible move left


# Human Strategy: choose an available piece and placement based on user input
def Human_Player_Fast(player, game, oval = 1):
    # turn_number = (TotalStartingPieces - len(player.pieces) + 1)
    if game.rounds<2:
        move = Greedy_Player(player,game,oval)
        return move

    else:

        move = Human_Player(player,game,oval)
        return move

# Board state is no longer used
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
            s+= player.potential
        
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
        
        # Tyler - AI implementation
        # add pieces in order from largest to smallest
        all_pieces = []
        for i in range(1,6):
            all_pieces.append(piece.I(i));
            all_pieces.append(piece.T(i));
            all_pieces.append(piece.X(i));
            all_pieces.append(piece.V(i));
            all_pieces.append(piece.W(i));
            all_pieces.append(piece.L(i));
            all_pieces.append(piece.U(i));
            all_pieces.append(piece.P(i));
            all_pieces.append(piece.N(i));
            all_pieces.append(piece.Y(i));
            all_pieces.append(piece.N0(i));
            all_pieces.append(piece.N1(i));
            all_pieces.append(piece.T0(i));
            all_pieces.append(piece.T1(i));
            all_pieces.append(piece.P0(i));
            all_pieces.append(piece.P1(i));
            all_pieces.append(piece.NN(i));   
            all_pieces.append(piece.RT1(6,i));
            all_pieces.append(piece.RT2(6,i));
            all_pieces.append(piece.RT3(6,i));
            all_pieces.append(piece.RT4(6,i));
            all_pieces.append(piece.RT5(6,i));

        board = Board(9, 22);
        board1 = Board(9, 22);
        board2 = Board(9, 22);

        P1 = Player(1, board1, one) # first player
        P2 = Player(2, board2, two) # second player

        order = [P1, P2];
        blokus = Blokus(order, board, all_pieces);
        play_blokus(blokus);

        # End of game display.
        
        firstp = P1
        secondp = P2  
        
        render([firstp.board.state,firstp.board.state2,firstp.board.state3,firstp.board.state4],\
        [secondp.board.state,secondp.board.state2,secondp.board.state3,secondp.board.state4],blokus.pieces,P2.pieces)  
                
        blokus.play();
        plist = sorted(blokus.players, key = lambda p: p.id);
        gscores = []
        for player in plist:
            gscores.append(player.score)
            print("Player "+ str(player.id) + " score "+ str(player.score) + ": ");
                  # + str([sh.id for sh in player.pieces]));
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
    
    # print("Missing pieces:     " + str(Names))
    # print("                    " + str(MCounts))
    
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
    multi_run(Games, Human_Player, Greedy_Player);

if __name__ == '__main__':
    main();


