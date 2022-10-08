#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 10:35:20 2022

@author: carljohan
"""
  
nrow = 8
ncol = 12

state = [[0] * ncol for i in range(nrow)];
state2 = [[0] * ncol for i in range(nrow)];
state3 = [[1] * ncol for i in range(nrow)]; # Rooms on the board, also signifies valid placements
state4 = [[0] * ncol for i in range(nrow)]; # Resources on the board

import piece_bear as piece
from gui_bear import *
import copy
  
pieces = [] 
pieces.append(piece.A1(0));


def possible_moves(state,state3,pieces,sub_location = 0):

    if sub_location == 0:
        min_x,max_x = 0,ncol
        min_y,max_y = 0,nrow
    else:
        min_x,max_x = 4*location[0],4*location[0]+4
        min_y,max_y = 4*location[1],4*location[1]+4
        

    visited = set()
    pieces_unique = []
    
    # Pieces unique should be an input instead    
    for p in pieces:
        if truncId(p) not in visited:
            visited.add(truncId(p))
            pieces_unique.append(p)
        # print('Pruning:',len(pieces),len(pieces_unique))
    
    locations = []
    free_spaces = set()
    t_counter = 0
    for x in range(min_x,max_x):
        for y in range(min_y,max_y):
            # Can simplify by using sets
            if state[y][x] == 0 and state3[y][x] > 0:
                free_spaces.add((x,y))

    
    placements = [] # a list of possible placements
    visited = [] # a list placements (a set of points on board)
    
    # Check every available corner
    num = 0
    for cr in free_spaces:
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
                    if valid_all(candidate.points):
                        if not set(candidate.points) in visited:
                            placements.append(candidate);
                            # print('Piece:' + str(sh.color))
                            visited.append(set(candidate.points));
                            
    placement_set = set([p.points for p in placements])
                                
    return placement_set;


# Check if a player's move is valid, including board bounds, pieces' overlap, adjacency, and corners.
# def valid_move(self, player, placement):
#     if ((False in [player.board.in_bounds(pt) for pt in placement]) or player.board.overlap(placement)) or \
#         ((player.board.moves_played>0) and player.board.adj(placement) == False):
#         return False
#     else:
#         return True


def valid_all(placement):
    if ((False in [in_bounds(pt) for pt in placement]) or overlap(placement)):
        return False
    else:
        return True
    
    
# Check if the point (y, x) is within the board's bound
def in_bounds(point):
    y = point[1]
    x = point[0]
    return 0<= point[0] < ncol and 0<= point[1] < nrow and state3[y][x]>0; ## Add condition for being on the board

# Check if a piece placement overlap another piece on the board
def overlap(placement):
    return False in[(state[y][x] == 0) for x, y in placement]
           

def adj_xy(placement):
    adj_set = set();
    four_directions = [(1,0),(-1,0),(0,1),(0,-1)]
    
    # Check left, right, up, down for adjacent square
    for y,x in placement:
        for d1,d2 in four_directions:
            (y1,x1) = (y+d1,x+d2)
            if (y1,x1) in board_empty:
                adj_set.add((y1,x1))

    return adj_set
   
pm = possible_moves(state,state3,pieces)  

print('Example move:',pm[0].points)


board_set = set()
board_occupied = set()
adj_set = set()

first_move = {(4,7)}
board_occupied.update(first_move)

# Initiate one sub-board with one space removed
for y in range(4,8):
    for x in range(4,8):
        board_set.add((x,y))
board_set.remove((6,5))
    
# Empty spaces on the board
board_empty = board_set.difference(board_occupied)
print('Empty spaces:',len(board_empty))

# Adjacent spaces that are also on the board
adj_test = adj_xy(board_occupied)
print(adj_test)

# Generating all valid moves on this_board from the full set of possible moves
valid_moves = set()
inbound_moves = set()

# Generate the initial set of valid moves (only done once, and partially when new sub-boards are added)
for p in pm:
    if len(set(p.points).intersection(board_empty))==p.size:
        if len(set(p.points).intersection(adj_test))>0:
            valid_moves.add(p)
        else:
            inbound_moves.add(p)

print(len(valid_moves),len(inbound_moves))

# Make another move and update the sets
next_move = {(5,6),(5,7),(6,7)}
board_occupied.update(next_move)
board_empty.difference_update(next_move)
adj_next = adj_xy(next_move)
adj_test.difference_update(next_move)
adj_test.update(adj_next)

print(adj_test)

non_valid = set()
for v in valid_moves:
    vset = set(v.points)
    if len(vset.intersection(next_move))>0:
        non_valid.add(v)

valid_moves.difference_update(non_valid)

non_in = set()

for v in inbound_moves:
    vset = set(v.points)
    if len(vset.intersection(next_move))>0:
        non_in.add(v)
    elif len(vset.intersection(adj_next))>0:
        valid_moves.add(v)
        non_in.add(v)
        
inbound_moves.difference_update(non_in)
        
print([v.points for v in inbound_moves])

# New set of valid moves and potential future candidates
print(len(valid_moves),len(inbound_moves))      
        




            
# piece_id

# valid_moves
# nonadj_moves


# canonical piece
