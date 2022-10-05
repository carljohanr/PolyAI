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
import piece_bear as piece
import grids_bear as grids
from gui_bear import *
import operator
import time
import numpy as np
from cats_score import score_board
import cats_score
from bear_score import cpenalty
# from cats_score import score_board_0

# cutoff depth for alphabeta minimax search (default 2)
Depth = 1
# number of successor states returned (default 4)
MovesToConsider = 4
# change to adjust the number of games played (defualt 10)
Games = 500
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
    def __init__(self, nrow, ncol, bcount):
        self.nrow = nrow; # total rows
        self.ncol = ncol; # total columns
        self.moves_played = 0
        self.debug = 0
        self.passed = 0
        self.score = 0
        self.score_breakdown = [0,0]
        self.potential = 0
        self.potential_breakdown = [0,0,0,0,0,0]

        self.state = [[0] * ncol for i in range(nrow)];
        self.state2 = [[0] * ncol for i in range(nrow)];
        self.state3 = [[0] * ncol for i in range(nrow)]; # Rooms on the board, also signifies valid placements
        self.state4 = [[0] * ncol for i in range(nrow)]; # Resources on the board
        # self.room_locations = []
        # for i in range(7):
        #     self.room_locations.append(set())
        self.park_spaces_covered = [0,0,0,0]
        
        self.board_map = [[0,0,0],[0,1,0]]
        self.board_adj_map = [[0,1,0],[1,0,1]]
        
        self.has_expansion = 0
        self.filled_spaces = 0
        self.has_piece = [0,0,0]    
        self.this_completed = 0
        
        # Add a flag to see if any enclosures are available to the player
        # Not yet used. Once enclosures are depleted, change status of remaining ones so they become less valuable.
        self.enclosure_available = 1
        
        self.addon_value = 1
        self.this_score = 0
        
        self.holes = []
        
        self.visited = set()
        
        for row in range(self.nrow):
            for col in range(self.ncol):
                if self.state3[row][col]==0:
                    self.visited.add((row,col))
        
    def update(self, player_id, move_type,proposal,debug = 0):
        
        self.potential_breakdown = [0,0,0,0,0,0]
        self.this_score = 0
        
        if move_type == 'expand_board':
            addon = proposal[2]
            (x,y) = proposal[1]
            self.addon_value += 1
            self.board_map[y][x]=1
            for j in range(4):
                self.state3[4*y+j][4*x:4*x+4]=[self.addon_value]*4
                self.state4[4*y+j][4*x:4*x+4]=addon[j]
                for i in range(4):
                    if addon[j][i] == -1:
                        self.state3[4*y+j][4*x+i] = 0
                        
                

            for j in range(6):
                vc,hc = divmod(j,3)
                if abs(vc-y)+abs(hc-x)==1 and self.board_map[vc][hc]==0:
                    self.board_adj_map[vc][hc]=1
            self.board_adj_map[y][x]=0
            
            self.has_expansion -= 1
            
            # print ('New maps:',self.board_map,self.board_adj_map)
            
        
        elif move_type == 'play_piece':
            placement = proposal.points
            color = proposal.color
            pset = set(placement)
            
            # Note to self: Need to copy the old one when working with arrays
            old_spaces_covered = copy.deepcopy(self.park_spaces_covered)
            
            self.moves_played += 1
            progress = min(1,self.moves_played/20)
            w = max(0,2*(progress-0.5))
            
            #print(self.state)
            #print(self.state2)
            maxval = max([max(s) for s in self.state2])
            for row in range(self.nrow):
                for col in range(self.ncol):
                    if(col, row) in placement:
                        self.state[row][col] = color;
                        self.state2[row][col] = maxval+1
                        this_resource = self.state4[row][col]
                        if this_resource in [1,2,3]:
                            rval = [0.5,2,2]
                            self.has_piece[this_resource-1] += 1
                            self.potential_breakdown[2] += 2*rval[this_resource-1]
                        # Can only expand 3 times. Should probably handle this elsewhere.
                        elif this_resource == 10 and self.has_expansion + self.addon_value < 4:
                            self.potential_breakdown[3] += 5
                            self.has_expansion += 1
                        this_room = self.state3[row][col]
                        if this_room>0:
                            self.park_spaces_covered[this_room-1] +=1
            
           
            self.this_completed = sum([1 for a in zip(self.park_spaces_covered,old_spaces_covered) if a[0]==15 and a[0]-a[1]>0])
            
            self.potential_breakdown[5]+= 3*self.this_completed
            # if self.this_completed>0:
                
            # print('Resources gained:',self.has_piece,self.has_expansion)
            # print('Debug:',self.park_spaces_covered,self.filled_spaces,self.this_completed)
    
            self.filled_spaces += len(pset)  
            # if len(pset) != proposal.size:
            #     print(proposal.id)
            
            piece_type = proposal.id[0:1]
            if piece_type == 'E':
                self.score_breakdown[1] += proposal.score
            elif piece_type == 'A':
                self.score_breakdown[0] += proposal.score
                
                
            self.this_score = proposal.score
             
                
            self.score = sum(self.score_breakdown)
            self.potential_breakdown[0] += self.score
            
            grid = copy.deepcopy(self.state)
            self.potential_breakdown[1] -= cpenalty(grid,self.state3)
            
            
            
            # Perhaps need to handle in player class
            # if new_pieces + len(player.pieces) < 2:
            #     this_score -= 100
            
            # potential_breakdown = [0,0,0,0,0]
            # self.potential = sum(potential_breakdown)
            
        
        self.visited = set()
        
        for row in range(self.nrow):
            for col in range(self.ncol):
                if self.state3[row][col]==0:
                    self.visited.add((row,col))
                    
        groups = list()
        visited = copy.deepcopy(self.visited)
                    
        # Empty spaces on the board represents possible spaces to expand
        self.holes = []
        holes2 = cats_score.connected_cells(self.state, self.visited, groups, 0)
        for hole2 in holes2:
            hole = [(y,x) for (x,y) in hole2]
            self.holes.append(hole)
            
        hole_stats = [len(h) for h in self.holes]
        
        for h in hole_stats:
            if h ==1:
                self.potential_breakdown[4] -= 3
            elif h ==2:
                self.potential_breakdown[4] -= 1.5
                
        self.potential_breakdown[4] -= len(hole_stats)
        self.potential = sum(self.potential_breakdown)
        
        # print('Hole stats:',player_id,[len(h) for h in self.holes])
        # print('Board score',player_id,self.score,self.score_breakdown)
        # print('Potential',player_id,self.potential,self.potential_breakdown)
        
        
        


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
        self.piece_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.corners = set() # current valid corners on board
        self.strategy = strategy # player's strategy
        self.board = board
        self.score = 0 # player's current score
        self.hand_score = 0
        self.potential = 0
        self.score_breakdown = [0,0,0,0,0]
        self.is_blocked = False
        # Has the player picked up resources to expand the board?
        self.has_expansion = 0
        self.has_piece = [0,0,0]
        self.terminal = 0

    # Add the player's initial pieces for a game
    def add_pieces(self, pieces):
        self.pieces = pieces;

    # Remove a player's Piece
    def remove_piece(self, piece):
        self.pieces = [p for p in self.pieces if p.id != piece.id];


    # Updates player information after placing a board Piece
    def update_player(self):
        self.score_breakdown[1:3] = self.board.score_breakdown
        self.score = sum(self.score_breakdown)
        self.potential = self.board.potential  
        # Adjusting the hand score and resetting so we don't do it again. Nicer way to do this?
        self.hand_score -= self.board.this_score
        self.board.this_score = 0
        # print(self.potential)
        if len(self.pieces) + sum(self.has_piece) < 2:
            self.potential -= 100
        self.has_expansion = self.board.has_expansion
        self.has_piece = self.board.has_piece
        # print('Piece counts:',self.piece_counts)
        # print('Filled spaces:',self.board.filled_spaces)
        if self.board.filled_spaces == 60:
            self.terminal = 1
            # print('Player',self.id, 'score:',self.score,self.score_breakdown)
        

    # def possible_moves_pruned(self,pieces,game):
        

    # Get a unique list of all possible placements
    def possible_moves(self,pieces, game,override = 0):

        move_type = game.move_type 
        if override == 1:
            move_type = 'play_piece'

        # Should rename to actions        
        if move_type in ['add_piece','add_piece_forced']:
            
            # What kind of piece did the player obtain? 
            if self.has_piece[2]>0:
                max_index = 20
            elif self.has_piece[1]>0:
                max_index = 8
            else:
                max_index = 4
            
            options = []
            
            for i in range(max_index):
                if game.piece_counts[i] > 0 and game.move_type == 'add_piece':
                    options.append(i)
                elif game.piece_counts[i] > 0 and len(self.possible_moves([game.all_pieces[i][0]],game,1))>0:
                    # print(move_type,i)
                    options.append(i)
                    
            return options
        
        elif move_type == 'expand_board':
            
            options = []
            
            for i in range(2):
                for j in range(6):
                    vc,hc = divmod(j,3)
                    if self.board.board_adj_map[vc][hc]>0:
                        options.append([i,(hc,vc),game.extra_grids[i][0]])
            
            # print(options)
            
            return options
            
        
        elif move_type == 'play_piece':
            
            visited = set()
            pieces_unique = []
            
            for p in pieces:
                if truncId(p) not in visited:
                    visited.add(truncId(p))
                    pieces_unique.append(p)
            # print('Pruning:',len(pieces),len(pieces_unique))
            
            locations = []
            t_counter = 0
            for i in range(self.board.ncol):
                for j in range(self.board.nrow):
                    locations.append((i,j))
            
            self.free_spaces = set([(x, y) for(x, y) in locations
                                if self.board.state[y][x] == 0 and self.board.state3[y][x]>0]);
            
            # print(self.free_spaces)
            # self.corners = set([(x, y) for(x, y) in self.corners
            #                     if game.board.state[y][x] == '_']);
    
            placements = [] # a list of possible placements
            visited = [] # a list placements (a set of points on board)
    
            # Check every available corner
            num = 0
            for cr in self.free_spaces:
                # Check every available piece
                for sh in pieces_unique:
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
        return self.strategy(self, game)


class Blokus:
    def __init__(self, players, all_pieces):
        self.players = players; 
        self.rounds = 0; 
        # self.board = board; 
        self.all_pieces = all_pieces; 
        # self.all_pieces = random.sample(self.all_pieces,len(all_pieces))
        
        self.starting_grids = grids.starting_grids
        self.starting_grids = random.sample(self.starting_grids,len(self.starting_grids))
        
        self.extra_grids = [grids.addon_grids[0:6],grids.addon_grids[6:12]]
        
        for p in self.players:
            start = self.starting_grids.pop(0)
            for j in range(4):
                p.board.state3[4+j][4:8]=[1,1,1,1]
                p.board.state4[4+j][4:8]=start[j]
                for i in range(4):
                    if start[j][i] == -1:
                        # print('-1 found')
                        p.board.state3[4+j][4+i] = 0
        
        # print(p.board.state3)
        # time.sleep(100)
        
        self.pieces = []
        self.previous = 0;
        # counter for how many times the total available moves are the same by checking previous round
        self.repeat = 0; 
        # self.treasures = [piece.TR1(6),piece.TR2(6),piece.TR3(6),piece.TR4(6)]
        self.win_player = 0; # winner
        self.day = 1
        self.piece_ids = ['G1','G2','G3','G4','A1','A2','A3','A4','E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12']

        # print(self.rounds,len(self.all_pieces))
        this_piece = self.all_pieces[0].pop(0)
        self.players[0].pieces.append(this_piece)
        this_piece = self.all_pieces[1].pop(0)
        self.players[1].pieces.append(this_piece)            
            
        self.piece_counts = [len(a) for a in all_pieces]
        # self.piece_counts = [50,12,8,8,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1]
        self.pieces_display = [p[0][0] for p in zip(self.all_pieces,self.piece_counts) if p[1]>0]
        # print('Display:',self.pieces_display)
        self.area_completion_bonus = [16,14,12,10,8,6,4,2]
        
        
        self.move_type = 'play_piece'
        
        
        

    # Check if a player's move is valid, including board bounds, pieces' overlap, adjacency, and corners.
    def valid_move(self, player, placement):
        if ((False in [player.board.in_bounds(pt) for pt in placement]) or player.board.overlap(placement)) or \
            ((player.board.moves_played>0) and player.board.adj(placement) == False):
            return False
        else:
            return True
        
    # Remove a player's Piece
    def remove_piece(self, piece):
        # print(piece,self.players[0].pieces)
        self.pieces = [p for p in self.players[0].pieces if p.id != piece.id];

    def take_piece(self, pindex):
        current = self.players[0]   
        # print(piece,self.players[0].pieces)
        # print(self.piece_counts,current.has_piece,pindex)
        
        for i in range(3):
            if current.has_piece[2-i]>0:
                current.has_piece[2-i]-=1
                break
        # time.sleep(2)
        
        this_piece = self.all_pieces[pindex].pop(0)
        self.piece_counts[pindex]-=1
        # self.players[0].piece_counts[pindex]+=1
        # print(self.piece_counts)
        self.players[0].pieces.append(this_piece)
        # Pieces in hand provides potential for later
        self.players[0].hand_score += this_piece.score
        # print('Hand score:',self.players[0].hand_score)
        self.pieces_display = [p[0][0] for p in zip(self.all_pieces,self.piece_counts) if p[1]>0]

    def remove_treasure(self, piece):
        self.treasures = [p for p in self.treasures if p.id != piece.id];

    # Play the game with the list of players sequentially until the
    # game ends (no more pieces can be placed for any player)
    def play(self):
        
        global Outcomes
 
        if self.players[0].id == 1:
            firstp,secondp = self.players[0],self.players[1]
        else:
            firstp,secondp = self.players[1],self.players[0]
                    
        
        current = self.players[0]   
        
        # print('Filled spaces:',self.players[0].board.filled_spaces, self.players[0].terminal)
            

        # if self.move_type == 'add_piece_forced':
        #     dummy = 0
        # else:
        #     #print(current.has_piece,sum(current.has_piece),current.has_expansion)
        #     if current.has_expansion > 0:
        #         self.move_type = 'expand_board'
        #     elif sum(current.has_piece) > 0:
        #         self.move_type = 'add_piece'
        #     else:
        #         self.move_type = 'play_piece'
                
        # print(self.move_type)
                
        proposal = current.next_move(self); # get the next move based on
                                            # the player's strategy
                                            


        if self.move_type in ('add_piece','add_piece_forced'):
            self.take_piece(proposal)
            current.update_player();
            render([firstp.board.state,firstp.board.state2,firstp.board.state3,firstp.board.state4],\
                   [secondp.board.state,secondp.board.state2,secondp.board.state3,secondp.board.state4],firstp.pieces,secondp.pieces,self.pieces_display)     
        
        elif self.move_type == 'expand_board':
            current.board.update(current.id,self.move_type, proposal,1)
            self.extra_grids[proposal[0]].pop(0)
            current.update_player();
            render([firstp.board.state,firstp.board.state2,firstp.board.state3,firstp.board.state4],\
                   [secondp.board.state,secondp.board.state2,secondp.board.state3,secondp.board.state4],firstp.pieces,secondp.pieces,self.pieces_display)   
                
        elif proposal is not None: # if there a possible proposed move
            color = proposal.color
            # check if the move is valid
            if self.valid_move(current, proposal.points):
                # update the board and the player status
                # print(time.time()-t)
                current.board.update(current.id,self.move_type, proposal,1);
                current.update_player();
                current.remove_piece(proposal); # remove used piece
                for i in range(current.board.this_completed):
                    current.score_breakdown[0] += self.area_completion_bonus.pop(0)
                render([firstp.board.state,firstp.board.state2,firstp.board.state3,firstp.board.state4],\
                       [secondp.board.state,secondp.board.state2,secondp.board.state3,secondp.board.state4],firstp.pieces,secondp.pieces,self.pieces_display)                     
                # print(time.time()-t)

            else: # end the game if an invalid move is proposed
                raise Exception("Invalid move by player "+ str(current.id));
                
        else:
            current.passed = 1
            print('I should not be here...',self.move_type,current.has_piece,current.pieces)
            # input("Press Enter to continue...")
                    
            # put the current player to the back of the queue

        
        # print('Stats before switching:',current.id,self.players,current.has_expansion,current.has_piece)
        # print('Stats by player:',self.players[0].has_expansion,self.players[0].has_piece,self.players[1].has_expansion,self.players[1].has_piece)
        # input("Press Enter to continue...")

        if current.has_expansion == 0 and sum(current.has_piece) == 0:
            if self.players[1].terminal == 0:
                first = self.players.pop(0);
                self.players += [first];
            else:
                self.players[0].terminal = 1
            
            nextp = self.players[0]

            self.move_type = 'play_piece'
            pmoves = nextp.possible_moves(nextp.pieces, self)
            # print('Available moves:',len(pmoves))
            if len(pmoves)==0:
                # print(nextp.pieces)
                self.move_type = 'add_piece_forced'
                self.players[0].has_piece = [1,0,0]
            else:
                self.move_type = 'play_piece'
                
        else:      
            if current.has_expansion > 0:
                self.move_type = 'expand_board'
            elif sum(current.has_piece) > 0:
                self.move_type = 'add_piece'
            else:
                print('To arrive here, player should have expansion or piece')
                
        self.rounds += 1; # update game round
  
        # print('Stats after switching:',current.id,current.has_expansion,current.has_piece)
        # print('Stats by player:',self.players[0].has_expansion,self.players[0].has_piece,self.players[1].has_expansion,self.players[1].has_piece)
        # input("Press Enter to continue...")
        # print('---')
        # time.sleep(1)

    def make_move(self,move,state):
        
        newboard = copy.deepcopy(state)
        current = newboard.to_move;

        proposal = move
                                            
        if newboard.game.move_type in ('add_piece','add_piece_forced'):
            newboard.game.take_piece(proposal)
            current.update_player();  
        
        elif newboard.game.move_type == 'expand_board':
            current.board.update(current.id,newboard.game.move_type, proposal,1)
            newboard.game.extra_grids[proposal[0]].pop(0)
            current.update_player(); 
                
        elif proposal is not None: # if there a possible proposed move
            color = proposal.color
            # check if the move is valid
            if self.valid_move(current, proposal.points):
                # update the board and the player status
                # print(time.time()-t)
                current.board.update(current.id,newboard.game.move_type, proposal,1);
                current.update_player();
                current.remove_piece(proposal); # remove used piece
                for i in range(current.board.this_completed):
                    current.score_breakdown[0] += newboard.game.area_completion_bonus.pop(0)                  
                # print(time.time()-t)

            else: # end the game if an invalid move is proposed
                raise Exception("Invalid move by player "+ str(current.id));
                
        else:
            current.passed = 1
            print('I should not be here...',self.move_type,current.has_piece,current.pieces)
                    
            # put the current player to the back of the queue

        if current.has_expansion == 0 and sum(current.has_piece) == 0:
            if newboard.game.players[1].terminal == 0:
                first = newboard.game.players.pop(0);
                newboard.game.players += [first];
            else:
                newboard.game.players[0].terminal = 1
            
            nextp = newboard.game.players[0]

            newboard.game.move_type = 'play_piece'
            pmoves = nextp.possible_moves(nextp.pieces, newboard.game)
            # print('Available moves:',len(pmoves))
            if len(pmoves)==0:
                # print(nextp.pieces)
                newboard.game.move_type = 'add_piece_forced'
                newboard.game.players[0].has_piece = [1,0,0]
            else:
                newboard.game.move_type = 'play_piece'
                
        else:      
            if current.has_expansion > 0:
                newboard.game.move_type = 'expand_board'
            elif sum(current.has_piece) > 0:
                newboard.game.move_type = 'add_piece'
            else:
                print('To arrive here, player should have expansion or piece')
            
        return newboard


    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        # find and return up to MovesToConsider possible moves as successors
        m = [(move, self.make_move(move, state))
                for move in state.to_move.possible_moves(state.to_move.pieces, state.game)]
        # print('Possible moves',m)
        
        # print(len(m))
        return m

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        # if we have no moves left, it's effectively a final state
        if self.players[0].terminal == 1 and self.players[1].terminal == 1:
            return True
        else:
            return False


    def utility(self, state, actual_turn_number):
        this_player = state.p1
        opponent = state.p2
        
        total = state.p1.score + 0.8*state.p1.hand_score - state.p2.score - 0.8*state.p2.hand_score
        
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
    
    if game.move_type in (['add_piece','add_piece_forced']):
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        this_choice = random.choice(possibles)
        # print('Pieces to select from:',possibles, this_choice)
        return this_choice
        
    elif game.move_type == 'play_piece':
        options = [p for p in player.pieces];
        while len(options) > 0: # if there are still possible moves
            piece = random.choice(options);
            # Function returns a piece so does not need to return the color as well (possibles[x].color)
            possibles = player.possible_moves([piece], game);
            if len(possibles) != 0: # if there is possible moves
                m = random.randint(0,len(possibles)-1)
                return possibles[m]
            else: # no possible move for that piece
                options.remove(piece); # remove it from the options
        return None; # no possible move left


def Random_Player_v2(player, game, oval = 1):
    
    if game.move_type in (['add_piece','add_piece_forced']):
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        # this_choice = random.choice(possibles)
        this_choice = max(possibles)
        # print('Pieces to select from:',possibles, this_choice)
        return this_choice

    elif game.move_type == 'expand_board':
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        this_choice = random.choice(possibles)
        return this_choice
        
    elif game.move_type == 'play_piece':
        options = [p for p in player.pieces];
        while len(options) > 0: # if there are still possible moves
            piece = random.choice(options);
            # Function returns a piece so does not need to return the color as well (possibles[x].color)
            possibles = player.possible_moves([piece], game);
            if len(possibles) != 0: # if there is possible moves
                m = random.randint(0,len(possibles)-1)
                return possibles[m]
            else: # no possible move for that piece
                options.remove(piece); # remove it from the options
        return None; # no possible move left

# Greedy Strategy: choose an available piece randomly based on own board only
def Greedy_Player(player, game, oval = 1, single_option = 0):
    
    
    if game.move_type in (['add_piece','add_piece_forced']):
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        
        scores = []
        for p in possibles:
            scores.append(game.all_pieces[p][0].score+game.all_pieces[p][0].size)
          
        max_index,max_score = getMax(possibles,scores)
        
        # print('Scores by piece:',scores,max_index,max_score,possibles[max_index])
        # The heuristic makes sense, but player ends up with holes that cannot be filled. Just picking the top index gets more square pieces
        return possibles[max_index]
        # return max(possibles)

    elif game.move_type == 'expand_board':
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        this_choice = random.choice(possibles)
        return this_choice
        
    elif game.move_type == 'play_piece':
        options = [p for p in player.pieces];
        scores = []
        all_possibles = []
        debug = []
        grid2 = game.players[0].board.state3
        maxval = max([max(s) for s in game.players[0].board.state2])
        temp_counter = 0
        
        # print('Pieces in hand:', options)
        
        # Copying a partial state and evaluating it is unnecessary. Better do it in the update_board class.
        for piece in options:
            # print('Piece:', piece)
            possibles = player.possible_moves([piece], game);
            # print('Options for piece:',piece,len(possibles))
            if len(possibles) != 0: # if there is possible moves
                for m in range(len(possibles)):
                    this_score = 0
                    new_pieces = 0
                    grid = copy.deepcopy(game.players[0].board.state)
                    grid3 = copy.deepcopy(game.players[0].board.state4)
                    # Should make a copy of the state and use the update function instead
                    for (p0,p1) in possibles[m].points:
                        grid[p1][p0]=1
                        if grid3[p1][p0]<10:
                            this_score += 2*grid3[p1][p0]
                            new_pieces +=1
                        elif grid3[p1][p0]==10:
                            this_score += 5
                    if new_pieces + len(player.pieces) < 2:
                        this_score -= 100
                    this_score += possibles[m].score-cpenalty(grid,grid2)
                    # debug.append(fam_dummy)
                    scores.append(this_score)
                    all_possibles.append(possibles[m])            

            else: # no possible move for that piece
                dummy = 0 # Do nothing
                # This statement created issues in the loop since we are looping over options
                # options.remove(piece); # remove it from the options
        
        # print('--')

        temp_counter+=1


        if len(all_possibles)>0:
            max_index,max_score = getMax(all_possibles,scores)
    
            # print(all_possibles[max_index].id)
            return all_possibles[max_index]
        else:
            print('No possible options')
            return None; # no possible move left



# Greedy Strategy: choose an available piece randomly based on own board only
def Winnie(player, game, oval = 1):
    
    # Move selection logic, could also be used for move ranking in search
    # Player prefers pieces that have higher point value, but does not want repeat pieces (mainly relevant for corner and straight pieces)
    
    if game.move_type in (['add_piece','add_piece_forced']):
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        
        scores = []
        mcounts = []
        
        in_stock = 0
        for p in possibles:
            for i in range(len(player.pieces)):
                pid1 = game.all_pieces[p][0].id
                pid2 = player.pieces[i].id
                if pid1 == pid2 or pid1[:-1] == pid2[:-1]:
                    in_stock += 1
            
            mcount =len(player.possible_moves([game.all_pieces[p][0]],game,1))
            if mcount ==0:
                adj = 0
            else:
                adj = 1
            mcounts.append(mcount)
            # if in_stock > 0:
            #     print(in_stock,'already in stock!')
            scores.append(adj*game.all_pieces[p][0].score+adj*game.all_pieces[p][0].size-0.5*in_stock)
         
        # print('Move counts:', mcounts)
        max_index,max_score = getMax(possibles,scores)
        
        # print('Scores by piece:',scores,max_index,max_score,possibles[max_index])
        # The heuristic makes sense, but player ends up with holes that cannot be filled. Just picking the top index gets more square pieces
        return possibles[max_index]
        # return max(possibles)

    elif game.move_type == 'expand_board':
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        
        scores = []
        all_possibles = []
        
        for m in possibles:
            player_copy = copy.deepcopy(game.players[0])
            player_copy.board.update(player.id,game.move_type,m)   
            player_copy.update_player()
            this_score = player_copy.potential
            # Pieces that are more valuable for the opponent more likely to be considered
            # But the player does not need to worry about where they are placed since board are indpendent
            scores.append(this_score)
            all_possibles.append(m)  
        
        if len(all_possibles)>0:
            max_index,max_score = getMax(all_possibles,scores)
            
        return all_possibles[max_index]
        
        # this_choice = random.choice(possibles)
        # return this_choice
        
    elif game.move_type == 'play_piece':
        options = [p for p in player.pieces];
        # print('Piece ids:', [p.id for p in options])
        scores = []
        all_possibles = []
        debug = []
        
        # print('Pieces in hand:', options)
        
        for piece in options:
            # print('Piece:', piece)
            possibles = player.possible_moves([piece], game);
            # print(len(possibles))
            if len(possibles) != 0: # if there is possible moves
                for m in possibles:
                    player_copy = copy.deepcopy(game.players[0])
                    player_copy.board.update(player.id,game.move_type,m)   
                    player_copy.update_player()
                    this_score = player_copy.potential
                    # Pieces that are more valuable for the opponent more likely to be considered
                    # But the player does not need to worry about where they are placed since board are indpendent
                    scores.append(this_score)
                    all_possibles.append(m)            
    
            # else: # no possible move for that piece
            #     options.remove(piece); # remove it from the options
                
            
        if len(all_possibles)>0:
            max_index,max_score = getMax(all_possibles,scores)
        
            # print(all_possibles[max_index].id)
            return all_possibles[max_index]
        else:
            print('No possible options')
            return None; # no possible move left


def Paddington(player, game, oval = 1):
    # track start time for use in post-game move time analysis     
    if game.rounds<50:
        return Winnie(player,game,1)   

    
    start_time = time.time()
    turn_number = 1
    
    # if no possible moves in this state, return None
    # plausible_moves returns a possible move (if any) faster than possble_moves
    
    possibles = player.possible_moves(player.pieces, game);

    game_copy = copy.deepcopy(game)
    state = BoardState(game_copy)
    
    #print(state.game.successors(state))
    # perform alphabeta search and return a useful move
    this_move = alphabeta_search(state, Depth, None, None, start_time, turn_number)
    
    return this_move
    
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



def getMax(candidates,scores):  
    max_score = -1000000
    max_index = 0
    for a in range(len(candidates)):
         if scores[a]>max_score:
             max_index = a
             max_score = scores[a]
    return max_index,max_score

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
        # self._board = game.board

# Play a round of blokus (all players move), then print board.
def play_blokus(blokus):
    # Make one premature call to blokus.play(), initializes board.    
    a=0
    s=0
    e=0
    c=0
    d=0
    
    while e<2:
        
        blokus.play()     
        if blokus.players[0].terminal + blokus.players[1].terminal == 2:
            e =2
        
        c = blokus.players[0].board.addon_value
        
        current = blokus.players[0]
        
        # print("Player 1 score: "+ str(current.score), current.score_breakdown, current.hand_score);
        
        # if c==4 and blokus.move_type=='play_piece' and d==0:
        #     input("Press Enter to continue...")
        #     d=1
        # time.sleep(1)
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
        
        for i in range(20):
            all_pieces.append([])
        all_pieces.append([])
        for i in range(50):
            all_pieces[0].append(piece.G1(i));
        for i in range(12):
            all_pieces[1].append(piece.G2(i));
        for i in range(8):
            all_pieces[2].append(piece.G3(i));
            all_pieces[3].append(piece.G4(i));
        for i in range(3):
            all_pieces[4].append(piece.A1(6-2*i));
            all_pieces[5].append(piece.A2(6-2*i));
            all_pieces[6].append(piece.A3(6-2*i));
            all_pieces[7].append(piece.A4(6-2*i));
            
        all_pieces[8].append(piece.E1());
        all_pieces[9].append(piece.E2());
        all_pieces[10].append(piece.E3());
        all_pieces[11].append(piece.E4());
        all_pieces[12].append(piece.E5());
        all_pieces[13].append(piece.E6());
        all_pieces[14].append(piece.E7());
        all_pieces[15].append(piece.E8());
        all_pieces[16].append(piece.E9());
        all_pieces[17].append(piece.E10());
        all_pieces[18].append(piece.E11());
        all_pieces[19].append(piece.E12());

        dm = divmod(i,50)[0]
        d1 = [0.1,0.2,0.3,0.4,0.5,0.2,0.2,0.2,0.2,0.2]
        d2 = [0.2,0.2,0.2,0.2,0.2,0.1,0.2,0.3,0.4,0.5]

        board = Board(8, 12, 0);
        board1 = Board(8, 12, 0);
        board2 = Board(8, 12, 0);

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
                
        # blokus.play();
        plist = sorted(blokus.players, key = lambda p: p.id);
        gscores = []
        for player in plist:
            gscores.append(player.score)
            print("Player "+ str(player.id) + " score: "+ str(player.score), player.score_breakdown);
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
    Games = 100
    multi_run(Games, Paddington, Winnie);

if __name__ == '__main__':
    main();


