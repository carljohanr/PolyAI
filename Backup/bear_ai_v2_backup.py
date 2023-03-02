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
from bear_player_v2 import *
import itertools
# from cats_score import score_board_0

# cutoff depth for alphabeta minimax search (default 2)
Depth = 15
# number of successor states returned (default 4)
# MovesToConsider = 4
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

AllMoves = [[[],[],[]],[[],[],[]]]

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



# Barenpark Board
class Board:
    def __init__(self, nrow, ncol, bcount):
        
        self.debug = 0
        
        self.grizzly = 1
        
        if self.grizzly == 0:
            self.addon_threshold = 3
        else:
            self.addon_threshold = 4
        
        #print('Addon threshold:', self.addon_threshold)
        
        self.nrow = nrow; # total rows
        self.ncol = ncol; # total columns
        self.moves_played = 0
        self.debug = 0
        self.passed = 0
        self.score = 0
        self.score_breakdown = [0,0,0,0]
        self.potential = 0
        self.potential_breakdown = [0,0,0,0,0,0]

        self.state = [[0] * ncol for i in range(nrow)];
        self.state2 = [[0] * ncol for i in range(nrow)];
        self.state3 = [[0] * ncol for i in range(nrow)]; # Rooms on the board, also signifies valid placements
        self.state4 = [[0] * ncol for i in range(nrow)]; # Resources on the board
        # self.room_locations = []
        # for i in range(7):
        #     self.room_locations.append(set())
        self.park_spaces_covered = [0,0,0,0,0]
        
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
        self.piece_count = 0
        
        self.holes = []
        self.hole_stats = []
        
        self.resource_value = 0
        
        self.recent_move = 0
        
        self.visited = set()
        
        for row in range(self.nrow):
            for col in range(self.ncol):
                if self.state3[row][col]==0:
                    self.visited.add((row,col))
        
    def update(self, player_id, move_type,proposal,debug = 0):
        
        
        t0 = time.time()
        
        self.potential_breakdown = [0,0,0,0,0,0]
        self.this_score = 0
        self.recent_move = proposal
        
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
                    # Don't add a resource for expanding board if it has already been expanded 3 times
                    if addon[j][i] == 10 and self.addon_value == self.addon_threshold+1:
                        self.state4[4*y+j][4*x+i] = 0
                    if addon[j][i] == 3 and self.addon_value == self.addon_threshold+1 and self.grizzly ==1:
                        self.state4[4*y+j][4*x+i] = 0
                        
                

            for j in range(6):
                vc,hc = divmod(j,3)
                if abs(vc-y)+abs(hc-x)==1 and self.board_map[vc][hc]==0:
                    self.board_adj_map[vc][hc]=1
            self.board_adj_map[y][x]=0
            
            self.has_expansion -= 1
            
            # print ('New maps:',self.board_map,self.board_adj_map)
            
        
        elif move_type == 'play_piece':
            self.piece_count += 1
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
            # for row in range(self.nrow):
            #     for col in range(self.ncol):
            resource_counts = [0,0,0]
            for (col, row) in placement:
                self.state[row][col] = color;
                self.state2[row][col] = maxval+1
                this_resource = self.state4[row][col]
                if this_resource in [1,2,3]:
                    # Adjusting for grizzly game. Baseline value: [0.5,3,2]
                    rval = [0.5,3,2]
                    self.resource_value += 2*rval[this_resource-1]
                    resource_counts[this_resource-1] += 1
                    self.has_piece[this_resource-1] += 1
                    self.potential_breakdown[2] += 2*rval[this_resource-1]
                # Can only expand 3 times. Should probably handle this elsewhere.
                elif this_resource == 10 and self.has_expansion + self.addon_value <= self.addon_threshold:
                    self.resource_value += 4
                    self.potential_breakdown[3] += 4
                    self.has_expansion += 1
                
                this_room = self.state3[row][col]
                if this_room>0:
                    self.park_spaces_covered[this_room-1] +=1
                else:
                    print('Error')
            
            if min(resource_counts[0:2])>0 and self.addon_value>1:
                # print('Grizzly resources!')
                self.resource_value += 4
           
            self.this_completed = sum([1 for a in zip(self.park_spaces_covered,old_spaces_covered) if a[0]==15 and a[0]-a[1]>0])
            
            self.potential_breakdown[5]+= 5*self.this_completed
            # if self.this_completed>0:
                
            # print('Resources gained:',self.has_piece,self.has_expansion)
            # print('Debug:',self.park_spaces_covered,self.filled_spaces,self.this_completed)
    
            self.filled_spaces += len(pset)  
            # if len(pset) != proposal.size:
            #     print(proposal.id)
            
            piece_type = proposal.id[0:1]
            piece_type2 = proposal.id[0:2]
            if piece_type == 'E':
                self.score_breakdown[1] += proposal.score
            elif piece_type == 'A':
                self.score_breakdown[0] += proposal.score
            elif piece_type2 == 'GR':
                self.score_breakdown[3] += proposal.score
                
            self.this_score = proposal.score
             
                
            self.score = sum(self.score_breakdown)
            self.potential_breakdown[0] += self.score
            
            t1 = time.time()
            
            if self.debug == 1:
                print('(1) Update board time taken ms:', round((t1-t0)*1000,3))
            
            
            grid = copy.deepcopy(self.state)
            self.potential_breakdown[1] -= cpenalty(grid,self.state3)
            
            
            
            # Perhaps need to handle in player class
            # if new_pieces + len(player.pieces) < 2:
            #     this_score -= 100
            
            # potential_breakdown = [0,0,0,0,0]
            # self.potential = sum(potential_breakdown)
          
        t1 = time.time()
        
        if self.debug ==1:
            print('(2) Update board time taken ms:', round((t1-t0)*1000,3))
        
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
            
        self.hole_stats = [len(h) for h in self.holes]
        
        # Testing alternative values (initially -3 for hole of size 1, -1.5 for hole of size 2)
        # Recovered defaults. With large penalties, bot sometimes gets stuck since it cannot expand the board.
        for h in self.hole_stats:
            if h ==1:
                self.potential_breakdown[4] -= 3
            elif h ==2:
                self.potential_breakdown[4] -= 1.5
                
        self.potential_breakdown[4] -= len(self.hole_stats)
        
        self.potential = sum(self.potential_breakdown)
        
        t1 = time.time()
        
        if self.debug == 1:
            print('(3) Update board time taken ms:', round((t1-t0)*1000,3))
            print('--')
            
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
        
        self.debug = 0
        
        self.grizzly = 1
        
        if self.grizzly == 0:
            self.total_park_area = 60
        else:
            self.total_park_area = 75
        
        self.id = id # player's id
        self.pieces = [] # player's unused game piece, list of Pieces
        self.piece_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
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
        
        self.piece_ids = ['G1','G2','G3','G4','A1','A2','A3','A4','E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12','GR1','GR2','GR3','GR4','GR5','GR6','GR7','GR8','GR9','GR10','GR11','GR12'] 
        self.unique_pieces = []
        self.move_type = 'play_piece'
        self.valid_set = []
        self.inbound_set = []
        self.valid_list = []
        self.inbound_list = []
        self.valid_value = []
        self.valid_ranked = []
        self.valid_max = []
        
        self.board_set = set()
        self.board_occupied = set()
        self.board_empty = set()
        self.adj_set = set()
        
        self.next_completion_bonus = 20
        
        self.move_count=1
        
        self.resource_dict = {0:0,1:1,2:6,3:4,10:5}
        self.pieces_by_type = [0,0,0,0]
        
        self.grizzly_option=0
        
        self.possible_moves_cache = [[[],[],[]],[[],[],[]]]
        
        
    def adj_xy(self,placement):
        adj_set = set();
        four_directions = [(1,0),(-1,0),(0,1),(0,-1)]
        
        # Check left, right, up, down for adjacent square
        for y,x in placement:
            for d1,d2 in four_directions:
                (y1,x1) = (y+d1,x+d2)
                if (y1,x1) in self.board_empty:
                    adj_set.add((y1,x1))

        return adj_set

    def adj_xy_score(self,placement):
        score = 0
        four_directions = [(1,0),(-1,0),(0,1),(0,-1)]
        
        # Check left, right, up, down for adjacent square
        for y,x in placement:
            for d1,d2 in four_directions:
                (y1,x1) = (y+d1,x+d2)
                if (y1,x1) not in placement:
                    if (y1,x1) in self.board_empty:
                        score -= 1
                    else:
                        score += 1

        return score

    def create_valid_sets(self):
        
        t0 = time.time()
        
        if self.board.moves_played == 0:
            dummy = 0
        # Generate all valid starting moves (only for the first piece)
        # Using the possible_move_list function
        
        elif self.board.moves_played == 1 and self.move_type == 'play_piece':
            for p in self.board.recent_move.points:
                self.board_occupied.add(p)
                self.board_empty = self.board_set.difference(self.board_occupied)
                self.adj_set = self.adj_xy(self.board_occupied)
            # print(self.board_occupied,self.adj_set)
            # print(self.unique_pieces)
            
            for i in range(len(self.unique_pieces)):
                placement_list = self.possible_move_list(self.unique_pieces[i],(1,1))
                # print(placement_set)
                self.valid_list.append([])
                self.inbound_list.append([])
                for v in placement_list:    
                    if len(v.intersection(self.adj_set))>0:
                        self.valid_list[i].append(v)
                    else:
                        self.inbound_list[i].append(v)
                        
                 
                        
                # if i == 16:
                    # print(self.id,self.unique_pieces[i].id,len(placement_list),len(self.valid_list[i]),len(self.inbound_list[i]))
            
            # time.sleep(5)
        
        elif self.board.moves_played > 1 and self.move_type == 'play_piece':
            
            # print(self.board.recent_move)
            this_move = set(self.board.recent_move.points)
            self.board_occupied.update(this_move)
            self.board_empty.difference_update(this_move)
            adj_next = self.adj_xy(this_move)
            self.adj_set.difference_update(this_move)
            self.adj_set.update(adj_next)

            # print(self.adj_set)

            # Incrementally update valid moves for all pieces:
                
            for i in range(len(self.unique_pieces)):
            
                counter0 = 0    
            
                new_valid_list = []
                
                self.valid_list[i] = [v for v in self.valid_list[i] if len(v.intersection(this_move))==0]
                
                # for v in self.valid_list[i]:
                #     if len(v.intersection(this_move))==0:
                #         counter0 +=1
                #         new_valid_list.append(v)
                #     self.valid_list[i] = copy.deepcopy(new_valid_list)
                    
                counter1,counter2 = 0,0
        
                self.valid_list[i] += [v for v in self.inbound_list[i] if len(v.intersection(this_move))==0 and len(v.intersection(adj_next))>0]
                self.inbound_list[i] = [v for v in self.inbound_list[i] if len(v.intersection(this_move))==0 and len(v.intersection(adj_next))==0]
        
                # new_inbound_list = []
                # for v in self.inbound_list[i]:
                #     if len(v.intersection(this_move))==0:
                #         if len(v.intersection(adj_next))>0:
                #             counter1+=1
                #             self.valid_list[i].append(v)
                #         else:
                #             counter2+=1
                #             new_inbound_list.append(v)
                    
                    # self.inbound_list[i] = copy.deepcopy(new_inbound_list)
                    
                # if i == 16:
                #     print(self.id,self.unique_pieces[i].id,'-',len(self.valid_list[i]),len(self.inbound_list[i]))
                #     print('Counters:',counter1,counter2)
            t1 = time.time()
            
            if self.debug == 1:
                print('(1a) Play move creating sets time taken ms:', round((t1-t0)*1000,3))          
                
        elif self.move_type == 'expand_board':
            
            this_move = self.board.recent_move
            # print('Expanding board:',this_move,this_move[1])
            four_directions = [(1,0),(-1,0),(0,1),(0,-1)]
            location = this_move[1]
            
            #First expand the board_set and board_empty
            board_add_set = set()
            min_x,max_x = 4*location[0],4*location[0]+4
            min_y,max_y = 4*location[1],4*location[1]+4
            
            for x in range(min_x,max_x):
                for y in range(min_y,max_y):
                    # Can simplify by using sets
                    if self.board.state3[y][x] > 0:
                        board_add_set.add((x,y))
            
                               
            self.board_set.update(board_add_set)
            self.board_empty.update(board_add_set)
        
            self.adj_set = self.adj_xy(self.board_occupied)
        
            #Then expand the adjacent set
            
           
            for i in range(len(self.unique_pieces)):
                
                # placement_list = self.possible_move_list(self.unique_pieces[i],location)
                # t1 = time.time()
                # self.valid_list[i] += [v for v in placement_list if len(v.intersection(self.adj_set))>0]
                # self.inbound_list[i] += [v for v in placement_list if len(v.intersection(self.adj_set))==0]
                # t1 = time.time()
                
                placement_list = AllMoves[location[1]][location[0]][i]
                
                t1 = time.time()
                
                # if i ==0:
                #     print(location,[v for v in placement_list if len(v.intersection(self.adj_set))>0 and len(v.difference(self.board_empty))==0])
                
                self.valid_list[i] += [v for v in placement_list if len(v.intersection(self.adj_set))>0 and len(v.difference(self.board_empty))==0]
                self.inbound_list[i] += [v for v in placement_list if len(v.intersection(self.adj_set))==0 and len(v.difference(self.board_empty))==0]
                t1 = time.time()                
                
                # print('(1b) Expand board creating sets time taken ms:', i, round((t1-t0)*1000,3))  
                
                
                # if i == 16:
                #     print(self.id,self.unique_pieces[i].id,len(placement_list),len(self.valid_list[i]),len(self.inbound_list[i]))
                        
                # print('Stats after expanding board:', self.unique_pieces[i].id,len(self.valid_list[i]),len(self.inbound_list[i]))
        
        
        # Computing the value of a move. Taking a resource gives player credit, but increasing entropy loses points
        self.valid_value = []
        # print('Valid list length',len(self.valid_list))
        
        if self.board.moves_played>0:
            self.move_count = 0
        
        # Building policy
        
        psc = self.board.park_spaces_covered
        
        
        for i in range(len(self.valid_list)):
            # print(i,self.piece_counts,self.valid_list)
            if self.piece_counts[i]>0 and self.board.moves_played>0:
                self.move_count += len(self.valid_list[i])
            self.valid_value.append([])
            for j in range(len(self.valid_list[i])):
                this_val1 = 0
                this_val2 = 0
                this_val3 = 0
                this_psc = [0,0,0,0,0]
                resource_list = []
                for k in self.valid_list[i][j]:
                    (x,y)=k
                    this_val1 += self.resource_dict[self.board.state4[y][x]]
                    resource_list.append(self.board.state4[y][x])
                    this_val2 += self.adj_xy_score(self.valid_list[i][j])
                    this_psc[self.board.state3[y][x]-1]+=1
                    for l in range(5):
                        if psc[l]<15 and this_psc[l]+psc[l]==15:
                            this_val3 += self.next_completion_bonus
                            # print('I completed an area!')
                grizzly_value_bonus = 0
                # After player has expanded the board once, try to make sure he is able to exchange for additional grizzlies
                if self.board.addon_value>1 and ((1 in resource_list or self.pieces_by_type[0]>0) and (2 in resource_list or self.pieces_by_type[1]>0)):
                    # print('I got a bonus!',self.pieces_by_type,resource_list)
                    # input('Test')
                    grizzly_value_bonus = self.grizzly * 5
                this_val = this_val1 + grizzly_value_bonus + min(0.5,max(0,-0.2+0.1*self.board.moves_played)) * this_val2 + 0.7 * this_val3
                # this_val = this_val1 + min(0.5,max(0,0.1*self.board.moves_played)) * this_val2
                self.valid_value[i].append(this_val)
        
        t1 = time.time()
        
        if self.debug == 1:
            print('(2) Creating sets time taken ms:', round((t1-t0)*1000,3))        
        
        # print([len(v) for v in self.valid_list])
        # print([len(v) for v in self.valid_value])
        # print('-')
        # time.sleep(2)    
    
        # if self.board.moves_played ==5:
        #     for i in range(20):
        #         print(self.valid_value[i])
                
            #time.sleep(100)
                    
                    # if self.board.moves_played ==1:
                    #     print(self.valid_list[i][j])
            
            
        # elif self.board.moves_played > 1 and self.move_type == 'expand_board:
            
        #     dummy = 0
            
                        
            

    # Add the player's initial pieces for a game
    def add_pieces(self, pieces):
        self.pieces = pieces;

    # Remove a player's Piece
    def remove_piece(self, piece):
        self.pieces = [p for p in self.pieces if p.id != piece.id];


    # Updates player information after placing a board Piece
    def update_player(self,flag = 0):
        
        t0 = time.time()
        
        
        self.score_breakdown[1:5] = self.board.score_breakdown
        self.score = sum(self.score_breakdown)
        self.potential = self.board.potential  
        
        # Adjusting the hand score and resetting so we don't do it again. Nicer way to do this?
        self.hand_score -= self.board.this_score
        
        self.pieces_by_type = [sum(self.piece_counts[0:4]),sum(self.piece_counts[4:8]),sum(self.piece_counts[8:20]),sum(self.piece_counts[20:32])]
        
        
        self.board.this_score = 0
        # print(self.potential)
        if len(self.pieces) + sum(self.has_piece) < 1:
            # print('Hi!',self.pieces)
            self.potential -= 100
        self.has_expansion = self.board.has_expansion
        self.has_piece = self.board.has_piece
        # print('Piece counts:',self.piece_counts)
        # print('Filled spaces:',self.board.filled_spaces)
        if self.board.filled_spaces == self.total_park_area:
            self.terminal = 1
            # print('Player',self.id, 'score:',self.score,self.score_breakdown)
          
        # When updating, player cannot make another grizzly swap if he did on this turn
        # if self.grizzly_option == 1:
        #     self.grizzly_option = 0
        
        v = [sum(self.piece_counts[0:4])+self.has_piece[0],sum(self.piece_counts[4:8])+self.has_piece[1]]
        
        if self.move_type == 'play_piece' and min(v)>0 and self.board.addon_value>1:
            self.grizzly_bonus = self.grizzly * 5
            # print('I got a bonus!')
        else:
            self.grizzly_bonus = 0
        
        if self.debug == 1:
            t1 = time.time()
            print('(1) Update player time taken ms:', round((t1-t0)*1000,3))
        
        
        if flag == 1:
            self.create_valid_sets()
            
        if self.debug == 1:
            t1 = time.time()
            print('(2) Update player time taken ms:', round((t1-t0)*1000,3))
            

    # def possible_moves_pruned(self,pieces,game):
        

    def possible_move_list(self,pieces,location = 0, all = 0):
    
        if location == 0:
            min_x,max_x = 0,self.board.ncol
            min_y,max_y = 0,self.board.nrow
        else:
            min_x,max_x = 4*location[0],4*location[0]+4
            min_y,max_y = 4*location[1],4*location[1]+4
            
    
        visited = set()
        pieces_unique = []
        
        # Pieces unique should be an input instead    
        # for p in pieces:
        #     if truncId(p) not in visited:
        #         visited.add(truncId(p))
        #         pieces_unique.append(p)
        #     # print('Pruning:',len(pieces),len(pieces_unique))
        
        # locations = []
        # t_counter = 0
        
        
        # print('Unique pieces:', pieces_unique)
        
        free_spaces = set()
        
        for x in range(min_x,max_x):
            for y in range(min_y,max_y):
                # Can simplify by using sets
                if (x,y) in self.board_set or all==1: #and self.board.state3[y][x] > 0:
                    free_spaces.add((x,y))
    
        # print('Free spaces:',len(free_spaces))
    
        
        placements = [] # a list of possible placements
        visited = []
        
        pieces_unique = [pieces]
        sh = pieces_unique[0]
        candidate = sh
        
        # Check every available corner
        num = 0
        for cr in free_spaces:
            # Check every available piece
                # Check every flip
            for flip in ["h", "v"]:
                # Check every rotation
                for rot in [0, 90, 180, 270]:
                    # t_counter += 1
                    # Create a copy to prevent an overwrite on the original
                    candidate.create(num, cr);
                    candidate.flip(flip);
                    candidate.rotate(rot);
                    # If the placement is valid and new
                    scp = set(candidate.points)
                    if (len(scp.difference(self.board_empty)) == 0 or all == 1) and (scp not in visited):
                        placements.append(scp);
                        visited.append(scp);
                                    
        return placements;

    def valid_all(self,placement):
        if ((False in [self.board.in_bounds(pt) for pt in placement]) or self.board.overlap(placement)):
            return False
        else:
            return True

    # Get a unique list of all possible placements
    def possible_moves(self,pieces, game,override = 0,simplified = 0):

        move_type = game.move_type 
        if override == 1:
            move_type = 'play_piece'

        # Should rename to actions        
        if move_type in ['add_piece','add_piece_forced']:
            
            # What kind of piece did the player obtain? 
            if self.has_piece[2]>0:
                max_index = 20
                min_index = 8
            elif self.has_piece[1]>0:
                max_index = 8
                min_index = 4
            else:
                max_index = 4
                min_index = 2
            
            options = []
            
            for i in range(max_index):
                if game.piece_counts[i] > 0 and game.move_type == 'add_piece' and (simplified==0 or i>=min_index):
                    options.append(i)
                elif move_type == 'add_piece_forced' and game.piece_counts[i] > 0: #and len(self.possible_moves([game.all_pieces[i][0]],game,1))>0:
                    # print(move_type,i)
                    options.append(i)
                    
            if len(options) == 0:
                print('Its pretty empty here!')
                options.append(0)
                options.append(1)
                    
            return options
        
        elif move_type == 'add_grizzly':
            
            alist = []
            blist = []
            clist = []
            options = []
            
            current = game.players[0]
            
            for i in range(4,8):
                if current.piece_counts[i]>0:
                    alist.append(i)
                    
            for i in range(0,4):
                if current.piece_counts[i]>0:
                    blist.append(i)
                    
            for i in range(20,32):
                if game.piece_counts[i]>0:
                    clist.append(i)
                    
            for a in alist:
                for b in blist:
                    for c in clist:
                        options.append([[a,b],c])
                        
                        
                
            options.append(-1)
            
            # print('Grizzly options:',options)
            # input('Press enter...')
            
            return options
        
        elif move_type == 'expand_board':
            
            options = []
            
            for i in range(2):
                for j in range(6):
                    vc,hc = divmod(j,3)
                    if self.board.board_adj_map[vc][hc]>0:
                        if len(game.extra_grids[i])>0:
                            options.append([i,(hc,vc),game.extra_grids[i][0]])
            
            # print(options)
            
            return options
            
        
        elif move_type == 'play_piece':
            
            visited = set()
            pieces_unique = []
            
            valid_indexes = []
            current = game.players[0]
            if current.board.moves_played == 0:
                if current.id == 1:
                    valid_indexes.append(0)
                elif current.id == 2:
                    valid_indexes.append(1)
            else:
                if current.has_piece[0]>0:
                    valid_indexes+= list(range(0,4))
                if current.has_piece[1]>0:
                    valid_indexes+= list(range(0,8))
                if current.has_piece[2]>0:
                    valid_indexes+= list(range(0,20))
                if current.has_piece[0]>0 and current.has_piece[1]>0:
                    valid_indexes+= list(range(20,32))
                
            # print('Valid indexes:',valid_indexes)
            
            
            for p in pieces:
                # print('Current piece:', truncId(p))
                pindex = game.piece_ids.index(truncId(p))
                if pindex in valid_indexes:
                    pieces_unique.append(p)
            
            # pieces_unique = pieces
            
            # for p in pieces:
            #     if truncId(p) not in visited:
            #         visited.add(truncId(p))
            #         pieces_unique.append(p)
            # print('Pruning:',len(pieces),len(pieces_unique))
            
            locations = []
            t_counter = 0
            for i in range(self.board.ncol):
                for j in range(self.board.nrow):
                    locations.append((i,j))
            
            self.free_spaces = set([(x, y) for(x, y) in locations
                                if self.board.state[y][x] == 0 and self.board.state3[y][x]>0]);
            
    
            placements = [] # a list of possible placements
            visited = [] # a list placements (a set of points on board)
    
            # Check every available place in the board
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

    # Get a unique list of all possible placements
    def possible_moves_ranked(self,pieces, game,override = 0,simplified = 0):

        
        move_type = game.move_type         
        # Should rename to actions        
        if move_type in ['add_piece','add_piece_forced']:
            
            # What kind of piece did the player obtain? 
            if self.has_piece[2]>0:
                max_index = 20
                min_index = 8
            elif self.has_piece[1]>0:
                max_index = 8
                min_index = 0
            else:
                max_index = 4
                min_index = 0
            
            options = []
            scores = []
            
            for i in range(min_index,max_index):
                if game.piece_counts[i] > 0:
                    if len(self.valid_value[i])>0:
                        max_value = max(self.valid_value[i])
                    else:
                        max_value = -100
                    options.append(i)
                    scores.append(max_value+game.all_pieces[i][0].score+0.5*game.all_pieces[i][0].size)
                    if i<=3:
                        scores[-1] -= game.players[0].piece_counts[i]
            new_options = [x for _, x in sorted(zip(scores, options), key=lambda pair: -pair[0])]
                    
            if len(new_options) == 0:
                print('Its pretty empty here!')
                new_options.append(0)
                new_options.append(1)
                    
            return new_options[0:4]
                
            # return options        

        elif move_type == 'add_grizzly':
            
            option = [[]]
            current = game.players[0]
            invalid = 0
            
            for s in range(3):
                
                partial_options = []
                scores = []
                
                if s == 0:
                    min_index,max_index = 4,8
                elif s== 1:
                    min_index,max_index = 0,4
                elif s==2 :
                    min_index,max_index = 20,32
            
                for i in range(min_index,max_index):
                    if (game.piece_counts[i] > 0 and s==2) or (current.piece_counts[i]>0 and s<2):
                        if len(self.valid_value[i])>0:
                            max_value = max(self.valid_value[i])
                        else:
                            max_value = -100
                        
                        for j in reversed(range(len(current.pieces))):
                            if truncId(current.pieces[j])==current.piece_ids[i]:
                                this_pindex = j
                                break
                                         
                        
                        if s<2 or max_value>0:
                            partial_options.append(i)
                            scores.append(max_value+current.pieces[this_pindex].score+0.5*current.pieces[this_pindex].size)
                        if i<=3:
                            scores[-1] -= game.players[0].piece_counts[i]
                            
                
                # print('I came up with...',s,partial_options)
                
                if len(partial_options)==0:
                    invalid =1
                elif s==2:
                    # print('Value by move:', scores)
                    partial_options = [x for _, x in sorted(zip(scores, partial_options), key=lambda pair: -pair[0])]
                    option.append(partial_options[0])
                else:
                    # Pick the lowest value for piece to give up
                    partial_options = [x for _, x in sorted(zip(scores, partial_options), key=lambda pair: pair[0])]
                    option[0].append(partial_options[0])
                    
                # print('Grizzly option selected:',option )
                    
            if invalid==1:
                # print('I dont want a grizzly')
                option = -1
                        
            # print(option)
                
            return [option]

        elif move_type == 'play_piece':
            
            visited = set()
            pieces_unique = []
            
            valid_indexes = []
            current = game.players[0]
            if current.board.moves_played == 0:
                if current.id == 1:
                    valid_indexes.append(0)
                elif current.id == 2:
                    valid_indexes.append(1)
            else:
                if current.has_piece[0]>0:
                    valid_indexes+= list(range(0,4))
                if current.has_piece[1]>0:
                    valid_indexes+= list(range(0,8))
                if current.has_piece[2]>0:
                    valid_indexes+= list(range(0,20))
                if current.has_piece[0]>0 and current.has_piece[1]>0:
                    valid_indexes+= list(range(20,32))
                
            # print('Valid indexes:',valid_indexes)
            
            
            for p in pieces:
                # print('Current piece:', truncId(p))
                pindex = game.piece_ids.index(truncId(p))
                if pindex in valid_indexes:
                    pieces_unique.append(p)
            
            placements = []
            scores = []
            
            for p in pieces_unique:
                pindex = self.piece_ids.index(truncId(p))
                # print(self.valid_list)
                # print('Piece index:', pindex,self.valid_list[pindex])
                
                # print([len(v) for v in self.valid_list])
                # print([len(v) for v in self.valid_value])
                
                for i in range(len(self.valid_list[pindex])):
                    candidate = copy.deepcopy(p)
                    candidate.set_points2(list(self.valid_list[pindex][i]))
                    placements.append(candidate)
                    scores.append(self.valid_value[pindex][i]+p.score+0.5*p.size)
                                        
                    
            new_placements = [x for _, x in sorted(zip(scores, placements), key=lambda pair: -pair[0])]
            
            # print([p.points for p in placements])
            # print(scores)
            # print([p.points for p in new_placements])
            # time.sleep(1000)
            
            # print(t_counter)
            return new_placements;
     
    def getAllMax(self,list1,rank_list):
        
        result = []
        
        m = max(rank_list)
        for i in range(len(rank_list)):
            if rank_list[i]==m:
                result.append(list1[i])
        
        return result
            
     
    def possible_moves_pruned(self,pieces, game,override = 0,simplified = 0):
        
        if (game.move_type == 'play_piece' and game.players[0].board.moves_played>0) or (game.move_type in ['add_piece','add_piece_forced','add_grizzly']):
            candidate_moves = self.possible_moves_ranked(pieces,game,override,simplified)
            # Pruning
            candidate_moves = candidate_moves[0:3]
            # print (candidate_moves[0].points)
            # time.sleep(100)
        else:
            candidate_moves = self.possible_moves(pieces,game,override,simplified)
            
        return candidate_moves
        

    # Get the next move based off of the player's strategy
    def next_move(self, game): 
        return self.strategy(self, game)


class Blokus:
    def __init__(self, players, all_pieces, grizzly = 0):
        self.grizzly = grizzly
        
        
        self.players = players; 
        self.rounds = 0; 
        # self.board = board; 
        self.all_pieces = all_pieces; 
        # self.all_pieces = random.sample(self.all_pieces,len(all_pieces))
        self.unique_pieces = []
        # Adjusted to support grizzlies
        for i in range(20+12*self.grizzly):
            self.unique_pieces.append(copy.deepcopy(self.all_pieces[i][0]))
        
        for p in self.players:
            p.unique_pieces = self.unique_pieces
            # print(self.unique_pieces)
            # input('Stop')
            
            # Build placement cache
            
            for j in range(6):
                vc,hc = divmod(j,3)
                for i in range(len(self.unique_pieces)):
                    all_candidates = p.possible_move_list(self.unique_pieces[i],(hc,vc),1)
                    # print(len(all_candidates))
                    AllMoves[vc][hc].append(all_candidates)
            # input('Stop')
            
        # print('Row 0, Col 0',AllMoves[0][0][0])
        # print('Row 0, Col 1',AllMoves[0][1][0])
        # print('Row 1, Col 0',AllMoves[1][0][0])
        # input('Stop')
        
        
        self.starting_grids = grids.starting_grids
        self.starting_grids = random.sample(self.starting_grids,len(self.starting_grids))
        
        self.extra_grids = random.sample(grids.addon_grids,len(grids.addon_grids))
        self.extra_grids = [self.extra_grids[0:6],self.extra_grids[6:12]]
        
        self.extra_grids_display = [grid[0] for grid in self.extra_grids if len(grid)>0]
        
        # print(self.extra_grids_display)
        
        # self.extra_grids[0] = random.sample(self.extra_grids[0],len(self.extra_grids[0]))
        # self.extra_grids[1] = random.sample(self.extra_grids[1],len(self.extra_grids[1]))
        
        for p in self.players:
            p.grizzly = self.grizzly
            p.board.grizzly = self.grizzly
            start = self.starting_grids.pop(0)
            for j in range(4):
                p.board.state3[4+j][4:8]=[1,1,1,1]
                p.board.state4[4+j][4:8]=start[j]
                for i in range(4):
                    if start[j][i] == -1:
                        # print('-1 found')
                        p.board.state3[4+j][4+i] = 0
                    else:
                        p.board_set.add((4+i,4+j))
        
        # print(p.board.state3)
        # time.sleep(100)
        
        self.pieces = []
        self.previous = 0;
        # counter for how many times the total available moves are the same by checking previous round
        self.repeat = 0; 
        # self.treasures = [piece.TR1(6),piece.TR2(6),piece.TR3(6),piece.TR4(6)]
        self.win_player = 0; # winner
        self.day = 1
        self.piece_ids = ['G1','G2','G3','G4','A1','A2','A3','A4','E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12','GR1','GR2','GR3','GR4','GR5','GR6','GR7','GR8','GR9','GR10','GR11','GR12']

        # print(self.rounds,len(self.all_pieces))
        # this_piece = self.all_pieces[0].pop(0)
        # self.players[0].pieces.append(this_piece)
        # self.players[0].piece_counts[0] += 1
        # this_piece = self.all_pieces[1].pop(0)
        # self.players[1].pieces.append(this_piece)
        # self.players[1].piece_counts[1] += 1  
        self.players[0].has_piece = [1,0,0]
        self.players[1].has_piece = [1,0,0]          
            
        self.piece_counts = [len(a) for a in all_pieces]
        # self.piece_counts = [50,12,8,8,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1]
        self.pieces_display = [p[0][0] for p in zip(self.all_pieces,self.piece_counts) if p[1]>0]
        # print('Display:',self.pieces_display)
        if grizzly == 1:
            self.area_completion_bonus = [20,18,16,14,12,10,8,6,4,2]
        else:
            self.area_completion_bonus = [16,14,12,10,8,6,4,2]
        
        
        self.move_type = 'play_piece'
        self.animal_depleted = 0
        
        
        
        
        

    # Check if a player's move is valid, including board bounds, pieces' overlap, adjacency, and corners.
    
    def valid_all(placement):
        if ((False in [player.board.in_bounds(pt) for pt in placement]) or player.board.overlap(placement)):
            return False
        else:
            return True
    
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
        self.players[0].piece_counts[pindex]+=1
        # print(self.piece_counts)
        self.players[0].pieces.append(this_piece)
        # Pieces in hand provides potential for later
        self.players[0].hand_score += this_piece.score
        # print('Hand score:',self.players[0].hand_score)
        self.pieces_display = [p[0][0] for p in zip(self.all_pieces,self.piece_counts) if p[1]>0]
        
        # Remove bonuses for animal houses once they are depleted
        if sum(self.piece_counts[4:8]) == 0 and self.animal_depleted == 0:
            for p in range(2):
                for i in range(self.players[p].board.ncol):
                    for j in range(self.players[p].board.nrow):
                        if self.players[p].board.state4[j][i]==2:
                            self.players[p].board.state4[j][i]=1
            self.animal_depleted = 1


    def take_grizzly(self, proposal):
        current = self.players[0]   
        # print(piece,self.players[0].pieces)
        # print(self.piece_counts,current.has_piece,pindex)
        
        # print('Proposed move:',proposal)
        
        if current.grizzly_option == 1:
            current.grizzly_option = 0
        
        if proposal == -1:
            return 0
        
        # time.sleep(2)
        
        return_pieces = proposal[0]
        new_pindex = proposal[1]
        
        remove_list = []
        piece_ids = []
        
        # print('Grizzly move selected',proposal)
        
        # print('Player pieces before:',current.id,[truncId(p) for p in current.pieces])
        
        l = len(current.pieces)
        for i in range(l):
            # print('Piece to be returned:', current.pieces[i],truncId(current.pieces[i]))
            this_index = self.piece_ids.index(truncId(current.pieces[i]))
            piece_ids.append(this_index)
           
        # print('Current player piece ids:',piece_ids)
           
        # print (piece_ids)
        
        # Do in reverse order to pick up least valuable piece
        for pindex in return_pieces:
            current.piece_counts[pindex]-=1
            for i in range(l):
                if pindex == piece_ids[l-i-1]:
                    remove_list.append(l-i-1)
                    break
                
        remove_list.sort(reverse = True)
        
        # print('Remove list:',remove_list)
        
        for index in remove_list:
            this_piece = current.pieces[index]
            current.hand_score -= this_piece.score
            current.pieces.pop(index)
            
        # print('Player pieces after:',current.id,[truncId(p) for p in current.pieces])
        
        # Not validated. Player needs to take a piece with index from 20-31
        this_piece = self.all_pieces[new_pindex].pop(0)
          
        
        # Piece counts does not yet take grizzlies into account, neither does piece ids
        self.piece_counts[new_pindex]-=1
        self.players[0].piece_counts[new_pindex]+=1
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
    
    
    def update_state(self,proposal,flag=1):
        
        current = self.players[0] 
        
        
        if self.move_type == 'expand_board':
            current.board.update(current.id,self.move_type, proposal,1)
            self.extra_grids[proposal[0]].pop(0)
            self.extra_grids_display = [grid[0] for grid in self.extra_grids if len(grid)>0]
            current.update_player(1);
            #print('Taking a break...')
            #time.sleep(1000)
            
        elif self.move_type == 'add_piece_forced':
            self.players[0].has_piece[0] += 1
                
        elif proposal is not None: # if there a possible proposed move
            # if current.board.moves_played == 9:
            #     input("Press Enter to continue...")
            color = proposal.color
            # check if the move is valid
            if self.valid_move(current, proposal.points):
                # update the board and the player status
                # print(time.time()-t)
                current.board.update(current.id,self.move_type, proposal,1); # remove used piece

                pindex = self.piece_ids.index(truncId(proposal))
                self.piece_counts[pindex] -= 1
                # Take away one piece of corresponding type from pool
                this_piece = self.all_pieces[pindex].pop(0)
                for i in range(current.board.this_completed):
                    # print('Area filled:',self.players[0].id,self.players[0].board.park_spaces_covered,self.area_completion_bonus[0])
                    current.score_breakdown[0] += self.area_completion_bonus.pop(0)
                    
                self.pieces_display = [p[0][0] for p in zip(self.all_pieces,self.piece_counts) if p[1]>0]
                
                if pindex in list(range(0,4)) and current.has_piece[0]>0:
                    current.has_piece[0]-=1
                elif pindex in list(range(0,4)) and current.has_piece[1]>0:
                    current.has_piece[1]-=1
                elif pindex in list(range(0,4)) and current.has_piece[2]>0:
                    current.has_piece[2]-=1
                if pindex in list(range(4,8)) and current.has_piece[1]>0:
                    current.has_piece[1]-=1
                elif  pindex in list(range(4,8)) and current.has_piece[2]>0:
                    current.has_piece[2]-=1
                if pindex in list(range(8,20)):
                    current.has_piece[2]-=1
                if pindex in list(range(20,32)):
                    current.has_piece[0]-=1
                    current.has_piece[1]-=1
                
                # print('Current resource_count:',current.has_piece)
                
                current.update_player(flag);                     
                # print(time.time()-t)

            else: # end the game if an invalid move is proposed
                raise Exception("Invalid move by player "+ str(current.id));
                
        else:
            current.passed = 1
            print('I should not be here...',self.move_type,current.has_piece,current.pieces)
            
            input("Press Enter to continue...")
                    
            # put the current player to the back of the queue
    
    
    def play(self):
        
        global Outcomes
 
        if self.players[0].id == 1:
            firstp,secondp = self.players[0],self.players[1]
        else:
            firstp,secondp = self.players[1],self.players[0]
                    
        
        current = self.players[0]  
        current.move_type = self.move_type
        current.next_completion_bonus = self.area_completion_bonus[0]
        
        # print('Player:',current.id,self.move_type,current.has_piece)
        
        if self.rounds == 0:
            render(firstp,secondp,firstp.pieces,secondp.pieces,self.pieces_display,self.extra_grids_display)
                        
                          
        proposal = current.next_move(self); # get the next move based on
                                            # the player's strategy   

        self.update_state(proposal)



        render(firstp,secondp,firstp.pieces,secondp.pieces,self.pieces_display,self.extra_grids_display)        

        # print('Stats before switching:',current.id,self.players,current.has_expansion,current.has_piece)
        # print('Stats by player:',self.players[0].has_expansion,self.players[0].has_piece,self.players[1].has_expansion,self.players[1].has_piece)
        # input("Press Enter to continue...")


        # Adjust the state for the next action
        if current.has_expansion == 0:
            
            if self.players[1].terminal == 0:
                first = self.players.pop(0);
                self.players += [first];
                # self.players[0].grizzly_option = 1
            else:
                self.players[0].terminal = 1
            self.move_type = 'play_piece'
            
            nextp = self.players[0]

            # self.move_type = 'play_piece'
            # pmoves = nextp.possible_moves(nextp.pieces, self)
            # print('Available moves:',len(pmoves))
            # if nextp.board.moves_played>0 and nextp.id == 2:
                # print('Move counts:',nextp.id,len(pmoves),nextp.move_count,nextp.piece_counts,nextp.valid_list[0])
                # print('Move counts:',nextp.piece_counts)
            # if len(pmoves)==0:
            if nextp.has_piece == [0,0,0]:
                # print(nextp.pieces)
                self.move_type = 'add_piece_forced'
            else:
                self.move_type = 'play_piece'
                
        else:      
            self.move_type = 'expand_board'
                
        self.rounds += 1; # update game round
  
        # print('Stats after switching:',current.id,current.has_expansion,current.has_piece)
        # print('Stats by player:',self.players[0].has_expansion,self.players[0].has_piece,self.players[1].has_expansion,self.players[1].has_piece)
        # input("Press Enter to continue...")
        # print('---')
        # time.sleep(1)

    def make_move(self,move,state,flag=1):
        
        
        newboard = copy.deepcopy(state)
        current = newboard.to_move;
        current.move_type = newboard.game.move_type
        current.next_completion_bonus = newboard.game.area_completion_bonus[0]

        proposal = move
                                            
        newboard.game.update_state(proposal,flag)
                    

        if current.has_expansion == 0:

            newboard.game.move_type = 'play_piece'
            # pmoves = current.possible_moves(current.pieces, newboard.game)
            # print('Available moves:',len(pmoves))
            if current.has_piece == [0,0,0]:
               # print(nextp.pieces)
               newboard.game.move_type = 'add_piece_forced'
            else:
               newboard.game.move_type = 'play_piece'
                
                
        else:      
            newboard.game.move_type = 'expand_board'
          
        return newboard


    def successors(self, state, flag=1):
        "Return a list of legal (move, state) pairs."
        # find and return up to MovesToConsider possible moves as successors
        
        m = [(move, self.make_move(move, state, flag))
                for move in state.to_move.possible_moves_pruned([p[0] for p in state.game.all_pieces if len(p)>0], state.game,0,1)]
        
        # Pruning to 5 options to make the search space smaller - doesn't work well with or without pruning
        
        game_progress = state.to_move.board.piece_count
        
        # Sort moves by utility, for pruning the search tree. But requires playing the moves first.
        if state.game.move_type in ('play_piece'):
            u = []     
            for mm in m:
                u.append(self.utility(mm[1],game_progress))
            f_1 = {}         
            # initializing blank list
            new_m = []
            # Addition of two list in one dictionary
            f_1 = {m[i]: u[i] for i in range(len(m))}
            # sorting of dictionary based on value
            f_lst = {k: v for k, v in sorted(f_1.items(), key=lambda item: -item[1])}
             
            # Element addition in the list
            for i in f_lst.keys():
                new_m.append(i)
            m = new_m[0:2]
        elif state.game.move_type == 'expand_board':
            m = m[0:3]
        else:
            m = m[0:1]
            
            

            
            # print([mm[0].points for mm in m])
            # time.sleep(10)
        
        #print('Possible moves:',len(m))
        
        # print(len(m))
        
        
        
        return m

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        # if we have no moves left, it's effectively a final state
        if self.players[0].terminal == 1 and self.players[1].terminal == 1:
            return True
        else:
            return False


    def utility(self, state, progress):
        this_player = state.p1
        opponent = state.p2
        
        # total = state.p1.score + 0.8*state.p1.hand_score + state.p1.board.potential_breakdown[4] + state.p1.board.potential_breakdown[1] + \
            # state.p1.board.filled_spaces + sum([p.size for p in state.p1.pieces])
        
            
        # if state.to_move.board.moves_played <13:
        #     total_breakdown = [(0.8-progress*0.05)*state.p1.hand_score,state.p1.score-0.3*state.p1.score_breakdown[0],sum([p.size for p in state.p1.pieces]),\
        #                        state.p1.board.potential_breakdown[1],state.p1.board.potential_breakdown[4],0.75*state.p1.board.resource_value]   
        # else:        
        #     total_breakdown = [state.p1.score]

        resource_value = 0

        resource_dict = {0:0,1:1,2:6,3:4,10:5}
        has_piece = state.p1.has_piece

        if has_piece[0]>0:
            resource_value += 1
        elif has_piece[1]>0:
            resource_value += 6
        elif has_piece[2]>0:
            resource_value += 4
        
        resource_value += state.p1.grizzly_bonus 
            

        # Grizzly version
        if state.to_move.board.moves_played <100:
            total_breakdown = [state.p1.score,
                               state.p1.board.potential_breakdown[1],0.5*state.p1.board.potential_breakdown[3],state.p1.board.potential_breakdown[4],resource_value] 
        else:        
            total_breakdown = [state.p1.score]
            
        #total_breakdown[5] = 0
            
        #print(total_breakdown)
        
        total = sum(total_breakdown) + 0.5*len(state.p1.board_empty) + len(state.p1.board_occupied)
        # print(state.game.move_type,state.p1.pieces,total)
        
        return total



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
            
        
        c = blokus.players[0].board.piece_count
        
        current = blokus.players[0]
        
        # print("Player 1 score: "+ str(current.score), current.score_breakdown, current.hand_score);
        
        # if c==12 and blokus.move_type=='play_piece' and d==0:
        #     input("Press Enter to continue...")
        #     d=1
        # time.sleep(1)
        time.sleep(TS)

# Run a blokus game with two players.
def multi_run(repeat, one, two):
    # Scores for each player
    winner = {1: 0, 2: 0};
    TotalMoveTimes = []

    gr = 0

    # Play as many games as indicated by param repeat
    for j in range(repeat):
        print("\nGame", (j + 1), ": Begin!\n")
        global MoveTimes
        MoveTimes = [] # Reset
        order = []; # Reset
        
        # Tyler - AI implementation
        # add pieces in order from largest to smallest
        all_pieces = []
        
        for i in range(20+12):
            all_pieces.append([])
        all_pieces.append([])
        for i in range(50):
            all_pieces[0].append(piece.G1(i));
        for i in range(12):
            all_pieces[1].append(piece.G2(i));
        for i in range(8):
            all_pieces[2].append(piece.G3(i));
            all_pieces[3].append(piece.G4(i));
        for i in range(3+gr):
            all_pieces[4].append(piece.A1(6+2*gr-2*i));
            all_pieces[5].append(piece.A2(6+2*gr-2*i));
            all_pieces[6].append(piece.A3(6+2*gr-2*i));
            all_pieces[7].append(piece.A4(6+2*gr-2*i));
            
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

        all_pieces[20].append(piece.GR1());
        all_pieces[21].append(piece.GR2());
        all_pieces[22].append(piece.GR3());
        all_pieces[23].append(piece.GR4());
        all_pieces[24].append(piece.GR5());
        all_pieces[25].append(piece.GR6());
        all_pieces[26].append(piece.GR7());
        all_pieces[27].append(piece.GR8());
        all_pieces[28].append(piece.GR9());
        all_pieces[29].append(piece.GR10());
        all_pieces[30].append(piece.GR11());
        all_pieces[31].append(piece.GR12());


        board = Board(8, 12, 0);
        board1 = Board(8, 12, 0);
        board2 = Board(8, 12, 0);

        P1 = Player(1, board1, one) # first player
        P2 = Player(2, board2, two) # second player

        order = [P1, P2];
        blokus = Blokus(order, all_pieces, 1);
        
        firstp = P1
        secondp = P2         
        
        play_blokus(blokus);

        # End of game display.
                
        # blokus.play();
        plist = sorted(blokus.players, key = lambda p: p.id);
        gscores = []
        for player in plist:
            gscores.append(player.score)
            print("Player "+ str(player.id) + " score: ", player.score, player.score_breakdown,player.board.filled_spaces,player.board.piece_count);
                  # + str([sh.id for sh in player.pieces]));
            for sh in player.pieces:
                if sh.id in Names:
                    MCounts[Names.index(sh.id)]+=1
        print("Game end.");
        pygame.image.save(screen, "Games/screenshot"+str(j)+".jpeg")
        # input("Game end. Press Enter to continue...")
        # time.sleep(5*TS)
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
    multi_run(Games, Paddington, PaddingtonPlus);

if __name__ == '__main__':
    main();


