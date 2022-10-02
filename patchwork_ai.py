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
import random
# import cats_score
# from cats_score import score_board_0
import grids

# cutoff depth for alphabeta minimax search (default 2)
Depth = 5
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
        self.square_fast = 0
        
        
    def update(self, player_id, proposal,income_locations,simplified = 0, debug = 1):

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
    
            if simplified == 0:
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
        
        self.score = self.money-2*self.empty_spaces+2*self.square_fast
        self.potential = self.score + self.icounter * self.income
        self.money_vector.append(self.money)
        
        if self.time_spent == 53 and self.has_square == 0:
            self.terminal = 1
            if debug == 1:
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
                placements.append(p)
        # print(t_counter)
        
        placements.append('Pass')
        
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
        self.pieces.append(piece.A());
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
        #print (piece.id, [p.id for p in self.pieces])
        i = 0
        # print(piece,piece.id)
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

    def play_fast(self,prop_flag = 0):  
        
        current = self.players[0]          
        if prop_flag != 0:
            proposal = prop_flag
        else:
            proposal = current.next_move(self); # get the next move based on
                                            # the player's strategy

        if proposal is not None: # if there a possible proposed move
            color = 1
            current.board.update(current.id, proposal,self.income_locations,1);
            current.update_player();
            self.remove_piece(proposal); # remove used piece                    
                
        else:
            current.board.passed = 1
            current.board.update(current.id, self.players[1].board.time_spent,self.income_locations,1);
            current.update_player();

        if current.board.prev_time_spent<self.square_locations[0] and current.board.time_spent>=self.square_locations[0]:
            # print('I got a square!')
            current.board.score +=2
            current.board.square_fast += 1
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
          
        render(firstp.board,secondp.board,self.pieces)     
            # time.sleep(TS)
        
        current = self.players[0]          
        proposal = current.next_move(self); # get the next move based on
        # print('Proposal:',proposal)                                            # the player's strategy
                                            
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
                    
                # print(time.time()-t)

            else: # end the game if an invalid move is proposed
                raise Exception("Invalid move by player "+ str(current.id));
                
        else:
            current.board.passed = 1
            current.board.update(current.id, self.players[1].board.time_spent,self.income_locations);
            current.update_player();
            # print('New time spent',self.players[0].board.time_spent,self.players[1].board.time_spent)

        if current.board.prev_time_spent<self.square_locations[0] and current.board.time_spent>=self.square_locations[0]:
            # print('I got a square!')
            current.board.has_square = 1
            self.square_locations.pop(0)

        # print('Time:',firstp.time_spent,secondp.time_spent,'\n')

        if current.board.has_square==0 and self.players[0].time_spent > self.players[1].time_spent:
            first = self.players.pop(0);
            self.players += [first];
           
        render(firstp.board,secondp.board,self.pieces)           
        self.rounds += 1; # update game round


    def make_move_fast(self,move,state):  
        
        newboard = copy.deepcopy(state)
        current = newboard.game.players[0]
        other = newboard.game.players[1]
        
        proposal = move
        if move == 'Pass':
            current.board.passed = 1
            current.board.update(current.id, other.board.time_spent,self.income_locations);
        else:
            current.board.update(current.id, proposal,self.income_locations,1);
            newboard.remove_piece(proposal); # remove used piece             
        current.update_player();
        

        if current.board.prev_time_spent < newboard.square_locations[0] and current.board.time_spent>=newboard.square_locations[0]:
            # print('I got a square!')
            current.board.score +=2
            newboard.square_locations.pop(0)

        if current.time_spent > other.time_spent:
            first = newboard.players.pop(0);
            newboard.players += [first];
                
        newboard.rounds += 1; # update game round
        
        return newboard

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
        m = [(move, self.make_move_fast(move, state))
                for move in state.to_move.possible_pieces(state.game.pieces[0:3], state.game)]
        # print('Possible moves',m)
        
        # print(len(m))
        return m

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        # if we have no moves left, it's effectively a final state
        if self.players[0].time_spent == 53 and self.players[1].time_spent == 53:
            return True
        else:
            return False


    def utility(self, state, actual_turn_number):
        this_player = state.p1
        opponent = state.p2
        
        total = state.p1.board.potential - state.p2.board.potential - 3*(state.p1.board.time_spent-state.p2.board.time_spent)
        
        return total

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


# Random Strategy: choose an available piece randomly
def Random_Piece(player, game, oval = 1):
    options = []
    icount = player.board.icounter
        
    for p in game.pieces[0:3]:
        if p.cost <= player.board.money:
            options.append(p)

    option_value = [(icount*p.income-p.cost)/p.time+random.random() for p in options]

    max_score = -1000
    if len(options)>0:
        for a in range(len(options)):
            if option_value[a]>max_score:
                max_index = a
                max_score = option_value[a]
        #print(all_possibles[max_index].id)
        return options[max_index]
    else:
        return None; # no possible move left

def Rollout_Player(player,game,oval = 1):

    print('Round',game.rounds)    

    if oval == 1 and game.rounds<25:
        options = []
        for p in game.pieces[0:3]:
            if p.cost <= player.board.money:
                options.append(p)
        icount = player.board.icounter
        option_value = [round((icount*p.income-p.cost)/p.time,1) for p in options]
    else:
        return Greedy_Player(player,game,oval)
    
    if len(options)<2:
        return Greedy_Player(player,game,oval)        
    
    
    win_list = []
    
    for j in range(len(options)):
        
        game_temp = copy.deepcopy(game)
        game_temp.play_fast(options[j])
        
        wins = 0
        score_diff = 0
    
        for i in range(1000):
        
            game_copy = copy.deepcopy(game_temp)
            current = game_copy.players[0]
            other = game_copy.players[1]
            current.strategy = Random_Piece
            other.strategy = Random_Piece
            
            while current.board.terminal == 0 or other.board.terminal == 0:
                game_copy.play_fast()
                # print('Hi!')
                # print(current.time_spent,other.time_spent)
            
            
            if player.id == game_copy.players[0].id:
                my_score = game_copy.players[0].score
                your_score = game_copy.players[1].score
            else:
                my_score = game_copy.players[1].score
                your_score = game_copy.players[0].score        
            
            if my_score>your_score:
                win = 1
            elif my_score==your_score:
                win = 0.5
            else:
                win = 0
                
            wins += win
            score_diff += my_score-your_score
            #print(win, my_score,your_score)
            
        win_list.append(wins)
        print('Rollout outcomes:', wins,score_diff,option_value[j])
       
    max_score = -1000
    if len(options)>0:
        for a in range(len(options)):
            if win_list[a]>max_score:
                max_index = a
                max_score = win_list[a]
        # print(all_possibles[max_index].id,all_possibles[max_index].color,round(scores[a],0),sorted(debug[a],reverse=True))
        #print (options[a].id)
        return Greedy_Player(player,game,2,[options[a]])
    else:
        return None; # no possible move left
       
    # time.sleep(100)
        

def Patchy(player, game, oval = 1):
    # track start time for use in post-game move time analysis
    if oval == 0:
        return Greedy_Player(player,game,0)        
    elif game.rounds>20:
        return Greedy_Player(player,game,1)   

    
    start_time = time.time()
    turn_number = 1
    
    # if no possible moves in this state, return None
    # plausible_moves returns a possible move (if any) faster than possble_moves
    
    options = player.possible_pieces(game.pieces[0:3], game)
    #print('Options:',options)
    
    if len(player.possible_pieces(game.pieces, game)) <= 1:
        return None; # no possible move left

    # copy current game info into a BoardState to be used within ab search
    game_copy = copy.deepcopy(game)
    state = BoardState(game_copy)
    
    #print(state.game.successors(state))
    # perform alphabeta search and return a useful move
    this_move = alphabeta_search(state, Depth, None, None, start_time, turn_number)
    
    # print(this_move, this_move =='Pass')

    if this_move == 'Pass':
        return None
    else:
        # print(this_move,this_move.id,options)
        for p in options:
            # print('Checking that one option matches')
            # print(p.id,this_move.id)
            if p.id == this_move.id:
                # print('Ready to return move')
                return Greedy_Player(player,game,2,[p])
    
    #time.sleep(100)

# AI implementation, taken from mancala.py

def alphabeta_search(state, d=1, cutoff_test=None, eval_fn=None, start_time=None, turn_number=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    global count
    global testing
    global BigInitialValue
    global MoveTimes
    
    testing = False

    print('Starting search',d)

    player = state.to_move
    if state.to_move.id == 1:
        flip = 1
    else:
        flip = -1
    count = 0

    def max_value(state, alpha, beta, depth):
        global count, testing
        if testing:
            print("  "* depth, "Max  alpha: ", alpha, " beta: ", beta, " depth: ", depth)
        if cutoff_test(state, depth):
            if testing:
                print("  "* depth, "Max cutoff returning ", eval_fn(state))
            return eval_fn(state)
        v = -BigInitialValue
        succ = state.game.successors(state)
        count = count + len(succ)
        if testing:
            print("  "*depth, "maxDepth: ", depth, "Total:", count, "Successors: ", len(succ))
        for (a, s) in succ:
            # Decide whether to call max_value or min_value, depending on whose move it is next.
            # A player can move repeatedly if opponent is completely blocked
            if state.to_move == s.to_move:
                v = max(v, max_value(s, alpha, beta, depth))
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
        succ = state.game.successors(state)
        count = count + len(succ)
        if testing:
            print("  "*depth, "minDepth: ", depth, "Total:", count, "Successors: ", len(succ))
        for (a, s) in succ:
            # Decide whether to call max_value or min_value, depending on whose move it is next.
            # A player can move repeatedly if opponent is completely blocked
            if state.to_move == s.to_move:
                v = min(v, min_value(s, alpha, beta, depth))
            else:
                v = min(v, max_value(s, alpha, beta, depth+1))
            if testing:
                print("  "*depth, "min best value:", v)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def right_value(s, alpha, beta, depth):
        if s.to_move.id == state.to_move.id:
            return max_value(s, -BigInitialValue, BigInitialValue, 0)
        else:
            return min_value(s, -BigInitialValue, BigInitialValue, 0)

    def argmin(seq, fn):
        """Return an element with lowest fn(seq[i]) score; tie goes to first one.
        >>> argmin(['one', 'to', 'three'], len)
        'to'
        """
        # print(seq)        
        
        best = seq[0]; best_score = fn(best)
        # print(best,best_score)
        for x in seq:
            x_score = fn(x)
            if x_score < best_score:
                best, best_score = x, x_score
        return best

    def argmax(seq, fn):
        """Return an element with highest fn(seq[i]) score; tie goes to first one.
        >>> argmax(['one', 'to', 'three'], len)
        'three'
        """
        return argmin(seq, lambda x: -fn(x))

    # Body of alphabeta_search starts here:
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or state.game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: flip*state.game.utility(state, turn_number))
    action, state = argmax(state.game.successors(state),
                            lambda a_s: right_value(a_s[1], -BigInitialValue, BigInitialValue, 0))

    print('Total nodes evaluated:', count)

    # calculate move time, round to 2 decimal places, store for analysis
    MoveTimes.append(round(time.time() - start_time, 2))
    return action




# Greedy Strategy: choose an available piece randomly based on own board only
def Greedy_Player(player, game, oval = 1, single_option = 0):
    # print(player.id,game.rounds)
    if oval == 2:
        #print('Hi',single_option)
        icount = player.board.icounter
        options = single_option;
        option_value = [(icount*p.income-p.cost)/p.time for p in options]
    elif oval == 1:
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
        #print(all_possibles[max_index].id)
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

# Need to fix how to keep track of players
class BoardState:
    """Holds one state of the Blokus board, used to generate successors."""
    def __init__(self, game=None):
        self.game = game
        self.p1 = [p for p in game.players if p.id == 1][0]
        self.p2 = [p for p in game.players if p.id == 2][0]
        # to_move keeps track of the player whose turn it is to move
        self.to_move = game.players[0]
        self.p1._board = game.players[0].board
        self.p2._board = game.players[1].board
        self.remove_piece = game.remove_piece
        self.square_locations = game.square_locations
        self.players = game.players
        self.rounds = game.rounds

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
        
        # print('State:', s, blokus.players[0].time_spent,blokus.players[1].time_spent)
        
        #print(s)
        
        if min(s) >= 1:
            e =2
        
        # if old_s == s:
        #     e+=1
        # else:
        #     e=0
        
        # TS=0.5
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
            # for sh in player.pieces:
            #     if sh.id in Names:
            #         MCounts[Names.index(sh.id)]+=1
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
    Games = 1
    multi_run(Games, Patchy, Greedy_Player);
    # multi_run(Games, Greedy_Player, Random_Player);

if __name__ == '__main__':
    main();


