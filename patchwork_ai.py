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
import piece_patchwork as piece
from gui_patchwork import *
import copy
import operator
import time
import numpy as np
from patchwork_score import cpenalty
# import cats_score
# from cats_score import score_board_0
import grids

# cutoff depth for alphabeta minimax search (default 2)
Depth = 1
# number of successor states returned (default 4)
MovesToConsider = 4
# change to adjust the number of games played (defualt 10)
Games = 50
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



# Blokus Board
class Board:
    def __init__(self, nrow, ncol):
        self.nrow = nrow; # total rows
        self.ncol = ncol; # total columns
        self.moves_played = 0
        self.debug = 0
        # self.passed = 0
        
        # A few of these are dummies and only one state is needed for the board in this game. 2nd state is used for display, 3rd state could be used to alter the board.
        self.state = [[0] * ncol for i in range(nrow)];
        self.state2 = [[0] * ncol for i in range(nrow)];
        self.state3 = [[1] * ncol for i in range(nrow)];
        self.state4 = [[0] * ncol for i in range(nrow)];
        self.money = 7
        self.income = 0
        self.icounter = 9
        self.prev_time_spent = 0
        self.time_spent = 0
        self.empty_spaces = 81
        self.passed = 0
        
        self.score = self.money-2*self.empty_spaces
        self.potential = self.score + self.icounter * self.income
        self.has_square = 0
        self.terminal = 0
        self.piece_incomes = []
        self.income_vector = []
        self.money_vector = []
        self.proposal_vector = []
        self.pass_incomes = []
        self.time_costs = []
        
        
   
        
        
    def update(self, player_id, proposal,income_locations,simplified = 0, debug = 0):

        for i in range(10):
            if income_locations[i]>self.time_spent:
                next_income = income_locations[i]    
                break
        # print (self.passed)

        self.prev_time_spent = self.time_spent        
        
        if self.passed == 1:
            self.time_spent = proposal+1
            self.time_spent = min(self.time_spent,53)
            pass_value = self.time_spent-self.prev_time_spent
            self.money += pass_value 
            self.pass_incomes.append(pass_value)
            self.passed = 0
            # print("Player",player_id, "passed and got:",pass_value,self.time_spent)
        
        else:
            self.moves_played += 1        
            
            # print(proposal)
    
            placement = proposal.points        
            pset = set(placement)
            
            self.time_spent += proposal.time
            self.time_costs.append(proposal.time)
            self.time_spent = min(self.time_spent,53)
            self.income += proposal.income
            self.piece_incomes.append(proposal.income)
            self.empty_spaces -= proposal.size
            self.money -= proposal.cost
            self.proposal_vector.append(proposal.cost)
            
            if simplified ==0:
                maxval = max([max(s) for s in self.state2])
                for row in range(self.nrow):
                    for col in range(self.ncol):
                        if(col, row) in placement:
                            self.state[row][col] = 1;
                            self.state2[row][col] = maxval+1
                        
            # print("My move: ", proposal.id,proposal.cost,proposal.time,proposal.income)
            
        if self.time_spent >= next_income and self.prev_time_spent < next_income:
            # print('I made money!',next_income)
            self.money += self.income
            self.income_vector.append(self.income)
            self.icounter -= 1
        
        self.score = self.money-2*self.empty_spaces
        self.potential = self.score + self.icounter * self.income
        self.money_vector.append(self.money)
        
        if self.time_spent == 53 and self.has_square == 0:
            print('Player',player_id)
            print('Cost:',self.proposal_vector,sum(self.proposal_vector))
            print('Incomes:',self.income_vector,sum(self.income_vector))
            print('Piece income:',self.piece_incomes,sum(self.piece_incomes))
            print('Time cost:',self.time_costs,sum(self.time_costs))
            print('Time pass:', self.pass_incomes,sum(self.pass_incomes))
            print('Money:',self.money_vector)
            print('Debug:',self.empty_spaces,81-sum([sum(s) for s in self.state]))
            # print(sum(s for s in self.state))
            print('')
            self.terminal = 1
        
        
        
        # print("Player",player_id, "new state:", self.score,self.potential,self.time_spent,self.money,self.income,self.empty_spaces,self.terminal,'\n')            



                  
        

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

    def adj_xy(self, placement):
        adj_set = set();
        # Check left, right, up, down for adjacent square
        for x, y in placement:
            if self.in_bounds((x + 1, y)) and self.state[y][x+1]==0:
                adj_set.add((x+1,y))
            if self.in_bounds((x - 1, y)) and self.state[y][x-1]==0:
                adj_set.add((x-1,y))
            if self.in_bounds((x , y+1)) and self.state[y+1][x]==0:
                adj_set.add((x,y+1))
            if self.in_bounds((x , y-1)) and self.state[y-1][x]==0:
                adj_set.add((x,y-1))

        return adj_set

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
        self.has_square = 0
        self.time_spent = 0

    # Add the player's initial pieces for a game
    def add_pieces(self, pieces):
        self.pieces = pieces;

    # Remove a player's Piece
    def remove_piece(self, piece):
        self.pieces = [p for p in self.pieces if p.id != piece.id];


    # Updates player information after placing a board Piece
    def update_player(self):
        
        self.score = self.board.score
        self.time_spent = self.board.time_spent
        self.terminal = self.board.terminal
        # self.potential = self.board.potential        
        

    # Get a unique list of all possible placements
    def possible_moves(self, pieces, game):
        # Updates the corners of the player, in case the
        # corners have been covered by another player's pieces.
        locations = []
        t_counter = 0
        for i in range(self.board.ncol):
            for j in range(self.board.nrow):
                locations.append((i,j))
        
        self.free_spaces = set([(x, y) for(x, y) in locations
                            if self.board.state[y][x] == 0 and self.board.state3[y][x]>0]);
        

        placements = [] # a list of possible placements
        visited = [] # a list placements (a set of points on board)

        # Check every available corner
        num = 0
        for cr in self.free_spaces:
            # Check every available piece
            for sh in pieces:
                if sh.cost <= self.board.money:
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
                                    # print('Piece:' + str(sh.color))
                                    visited.append(set(candidate.points));
                                    
        # print(t_counter)
        return placements;


    # Get a unique list of all possible placements
    def possible_pieces(self, pieces, game):
        # Updates the corners of the player, in case the
        # corners have been covered by another player's pieces.
        
        placements = []
        
        for p in pieces:
            if p.cost <= self.board.money:
                placements.append[p]
        # print(t_counter)
        return placements;

    # Get the next move based off of the player's strategy
    def next_move(self, game):
        # print(self.board.has_square)
        if self.board.has_square == 0:    
            return self.strategy(self, game, 1)
        else:
            return self.strategy(self, game, 0)


class Blokus:
    def __init__(self, players, all_pieces):
        self.players = players; 
        self.rounds = 0; 
        # self.board = board; 
        self.all_pieces = all_pieces; 
        self.pieces = random.sample(self.all_pieces,len(all_pieces))
        self.available_pieces = []
        self.income_locations = [5, 11, 17, 23, 29, 35, 41, 47, 53, 60]
        self.square_locations = [20, 26, 32, 44, 50, 60]
        self.square = [piece.h()]
        

    # Check if a player's move is valid, including board bounds, pieces' overlap, adjacency, and corners.
    def valid_move(self, player, placement):
        if ((False in [player.board.in_bounds(pt) for pt in placement]) or player.board.overlap(placement)) or \
            ((player.board.moves_played>0) and player.board.adj(placement) == False):
            return False
        else:
            return True
        
    # Remove a player's Piece
    def remove_piece(self, piece):
        i = 0
        for p in self.pieces:
            if p.id == piece.id:
                this_i = i
                break
            i+=1
        # print('This piece index:', this_i)
        for j in range(this_i):
            first = self.pieces.pop(0);
            self.pieces += [first];
        self.pieces.pop(0)

    def remove_treasure(self, piece):
        self.treasures = [p for p in self.treasures if p.id != piece.id];

    # Play the game with the list of players sequentially until the
    # game ends (no more pieces can be placed for any player)

    def play_fast(self):
        
        current = self.players[0]          
        proposal = current.next_move(self); # get the next move based on
                                            # the player's strategy

        if proposal is not None: # if there a possible proposed move
            # print('Making a move')
            color = 1

            current.board.update(current.id, proposal,self.income_locations,1);
            current.update_player();
            
            if current.board.has_square == 1:
                current.board.has_square = 0
            else:
                self.remove_piece(proposal); # remove used piece
                    
                
        else:
            current.board.passed = 1
            current.board.update(current.id, self.players[1].board.time_spent,self.income_locations,1);
            current.update_player();

        if current.board.prev_time_spent<self.square_locations[0] and current.board.time_spent>=self.square_locations[0]:
            # print('I got a square!')
            current.board.has_square = 1
            self.square_locations.pop(0)

        # print('Time:',firstp.time_spent,secondp.time_spent,'\n')

        if current.board.has_square==0 and self.players[0].time_spent > self.players[1].time_spent:
            first = self.players.pop(0);
            self.players += [first];
                
        self.rounds += 1; # update game round

    def play(self):
        
        # print('Piece count:',len(self.pieces))
        
        global Outcomes
 
        if self.players[0].id == 1:
            firstp = self.players[0]
            secondp = self.players[1]
        else:
            secondp = self.players[0]
            firstp = self.players[1]                  
          
        render([firstp.board.state,firstp.board.state2,firstp.board.state3,firstp.board.state4],\
                   [secondp.board.state,secondp.board.state2,secondp.board.state3,secondp.board.state4],self.pieces,self.pieces)     
            # time.sleep(TS)
        
        current = self.players[0]          
        proposal = current.next_move(self); # get the next move based on
                                            # the player's strategy

        if proposal is not None: # if there a possible proposed move
            # print('Making a move')
            color = 1
            # check if the move is valid
            if self.valid_move(current, proposal.points):
                # update the board and the player status
                current.board.update(current.id, proposal,self.income_locations);
                current.update_player();
                
                if current.board.has_square == 1:
                    current.board.has_square = 0
                else:
                    # print('Current index:', self.pieces.index(proposal))
                    self.remove_piece(proposal); # remove used piece
                    
                render([firstp.board.state,firstp.board.state2,firstp.board.state3,firstp.board.state4],\
                       [secondp.board.state,secondp.board.state2,secondp.board.state3,secondp.board.state4],self.pieces,self.pieces)                     
                # print(time.time()-t)

            else: # end the game if an invalid move is proposed
                raise Exception("Invalid move by player "+ str(current.id));
                
        else:
            current.board.passed = 1
            current.board.update(current.id, self.players[1].board.time_spent,self.income_locations);
            current.update_player();

        if current.board.prev_time_spent<self.square_locations[0] and current.board.time_spent>=self.square_locations[0]:
            # print('I got a square!')
            current.board.has_square = 1
            self.square_locations.pop(0)

        # print('Time:',firstp.time_spent,secondp.time_spent,'\n')

        if current.board.has_square==0 and self.players[0].time_spent > self.players[1].time_spent:
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
    print (option_names)
    
    piece = input("Choose a piece: ");
    print("");
    try: 
        if piece in ('p','P'):
            return 'Pass'
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
                    if this_point not in p.points and p not in exclude_list:
                        exclude_list.append(p)
                if len(possibles)-len(exclude_list) == 1:
                    for z in range(len(possibles)):
                        if possibles[z] not in exclude_list:
                            choice = z+1
                elif len(possibles)-len(exclude_list) == 0:
                    exclude_list = []
                
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
        options = [p for p in game.pieces[0:3]];
        # print(option_value)
        # print('Getting a move...',len(options))
    else:
        options = [p for p in game.square]
    while len(options) > 0: # if there are still possible moves
        piece = random.choice(options);
        # Function returns a piece so does not need to return the color as well (possibles[x].color)
        possibles = player.possible_moves([piece], game);
        # print(len(possibles))
        if len(possibles) != 0: # if there is possible moves
            m = random.randint(0,len(possibles)-1)
            return possibles[m]
        else: # no possible move for that piece
            options.remove(piece); # remove it from the options
    return None; # no possible move left


def Rollout_Player(player,game,oval = 1):

    if oval == 1:
        icount = player.board.icounter
        options = [p for p in game.pieces[0:3]];
        option_value = [(icount*p.income-p.cost)/p.time for p in options]
    else:
        return Greedy_Player(player,game,oval)
    
    game_copy = copy.deepcopy.game
    game_copy.player1.strategy = 'Random_Player'
    game_copy.player2.strategy = 'Random_Player'
    
    while game_copy.players[0].board.terminal == 0 or game_copy.players[1].board.terminal == 0:
        game_copy.play_fast()
    
    print(game_copy.players[0].id,game_copy.players[0].score)
        

# Greedy Strategy: choose an available piece randomly based on own board only
def Greedy_Player(player, game, oval = 1):
    if oval == 1:
        icount = player.board.icounter
        options = [p for p in game.pieces[0:3]];
        option_value = [(icount*p.income-p.cost)/p.time for p in options]
    else:
        options = [p for p in game.square]
        option_value = [0]
        # print(options)
    scores = []
    all_possibles = []
    debug = []
    grid2 = game.players[0].board.state3
    maxval = max([max(s) for s in game.players[0].board.state2])
    temp_counter = 0
    for piece in options:
        # print('Piece:', piece)
        possibles = player.possible_moves([piece], game);
        # print(len(possibles))
        if len(possibles) != 0: # if there is possible moves
            # print(len(possibles),possibles[m].points,possibles[m].color)
            # print(game.players[0].board.state,game.players[0].board.state2,game.players[0].board.state3)
            for m in range(len(possibles)):
                grid = copy.deepcopy(game.players[0].board.state)
                # Should make a copy of the state and use the update function instead
                for (p0,p1) in possibles[m].points:
                    grid[p1][p0]=1
                
                this_score = option_value[temp_counter]-0.1*cpenalty(grid,grid2)
                # debug.append(fam_dummy)
                scores.append(this_score)
                all_possibles.append(possibles[m])            

        else: # no possible move for that piece
            options.remove(piece); # remove it from the options

        temp_counter+=1

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
        icount = player.board.icounter
        options = [p for p in game.pieces[0:3]];
        option_value = [(icount*p.income-p.cost) for p in options]
    else:
        options = [p for p in game.square]
        option_value = [0]
        # print(options)
    scores = []
    all_possibles = []
    debug = []
    grid2 = game.players[0].board.state3
    maxval = max([max(s) for s in game.players[0].board.state2])
    temp_counter = 0
    for piece in options:
        # print('Piece:', piece)
        possibles = player.possible_moves([piece], game);
        # print(len(possibles))
        if len(possibles) != 0: # if there is possible moves
            # print(len(possibles),possibles[m].points,possibles[m].color)
            # print(game.players[0].board.state,game.players[0].board.state2,game.players[0].board.state3)
            for m in range(len(possibles)):
                grid = copy.deepcopy(game.players[0].board.state)
                # Should make a copy of the state and use the update function instead
                for (p0,p1) in possibles[m].points:
                    grid[p1][p0]=1
                
                this_score = option_value[temp_counter]-0.1*cpenalty(grid,grid2)
                # debug.append(fam_dummy)
                scores.append(this_score)
                all_possibles.append(possibles[m])            

        else: # no possible move for that piece
            options.remove(piece); # remove it from the options

        temp_counter+=1

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
    options = []
    if oval == 1:
        for p in game.pieces:
            possibles = player.possible_moves([p], game);
            if len(possibles) != 0:
                options.append(p)
    else:
        options = [p for p in game.treasures]
        # print(options)
    while len(options) > 0: # if there are still possible moves
        piece = piece_prompt(options);
        if piece=='Pass':
            return None
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
        s = []
        blokus.play()
        for player in blokus.players:
            s.append(player.terminal)
        # print(blokus.day,len(blokus.pieces))
        
        #print(s)
        
        if min(s) >= 1:
            e =2
        
        # if old_s == s:
        #     e+=1
        # else:
        #     e=0
        
        time.sleep(TS)

# Run a game with two players.
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
        
        all_pieces = []
        all_pieces.append(piece.A());
        all_pieces.append(piece.B());
        all_pieces.append(piece.C());
        all_pieces.append(piece.D());
        all_pieces.append(piece.E());
        all_pieces.append(piece.F());
        all_pieces.append(piece.G());
        all_pieces.append(piece.H());
        all_pieces.append(piece.I());
        all_pieces.append(piece.J());
        all_pieces.append(piece.K());
        all_pieces.append(piece.L());
        all_pieces.append(piece.M());
        all_pieces.append(piece.N());
        all_pieces.append(piece.O());
        all_pieces.append(piece.P());
        all_pieces.append(piece.Q());
        all_pieces.append(piece.R());
        all_pieces.append(piece.S());
        all_pieces.append(piece.T());
        all_pieces.append(piece.U());
        all_pieces.append(piece.V());
        all_pieces.append(piece.W());
        all_pieces.append(piece.X());
        all_pieces.append(piece.Y());
        all_pieces.append(piece.Z());
        all_pieces.append(piece.a());
        all_pieces.append(piece.b());
        all_pieces.append(piece.c());
        all_pieces.append(piece.d());
        all_pieces.append(piece.e());
        all_pieces.append(piece.f());
        all_pieces.append(piece.g());


        board = Board(9, 9);
        board1 = Board(9, 9);
        board2 = Board(9, 9);

        P1 = Player(1, board1, one) # first player
        P2 = Player(2, board2, two) # second player

        order = [P1, P2];
        blokus = Blokus(order, all_pieces);
        
        firstp = P1
        secondp = P2  
        
        # Start of game display
        # Need to clear board before rendering
        # render([firstp.board.state,firstp.board.state2,firstp.board.state3,firstp.board.state4],\
        # [secondp.board.state,secondp.board.state2,secondp.board.state3,secondp.board.state4],blokus.pieces+blokus.treasures,P2.pieces)          
        
        
        play_blokus(blokus);

        # End of game display.
        
        firstp = P1
        secondp = P2  
        
        # render([firstp.board.state,firstp.board.state2,firstp.board.state3,firstp.board.state4],\
        # [secondp.board.state,secondp.board.state2,secondp.board.state3,secondp.board.state4],blokus.pieces,P2.pieces)  
                
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
    Games = 10
    multi_run(Games, Greedy_Player, Random_Player);

if __name__ == '__main__':
    main();


