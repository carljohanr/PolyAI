#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 12:53:19 2021

@author: carljohan
"""

import random

from PIL import Image
import numpy as np
import copy
import piece_dict as pd
import os


# from concat_image import get_concat_h_blank



four_directions = [[0,1],[0,-1],[1,0],[-1,0]]

COLOR_MAP = {
    range(0, 1): (220, 220, 220),
    range(-1, 0): (170, 170, 170),
    range(1, 2): (194, 24, 7),
    range(2, 3): (11, 132, 35),
    range(3, 4): (6,77, 160),
    range(4, 5): (255, 170, 0),
    range(5, 6): (128, 37, 118),
    range(6, 7): (108,47,0),
    range(7, 8): (255, 105, 180),
    range(8, 12): (30, 30, 30)
}

# Barenpark color map

COLOR_MAP = {
    range(0, 1): (240, 240, 240),
    range(-1, 0): (170, 170, 170),
    range(1, 2): (254, 227, 180),
    range(2, 3): (11, 185, 35),
    range(3, 4): (0, 100, 0),
    range(4, 5): (140, 140, 140),
    range(5, 6): (0, 191, 255),
    range(6, 7): (238, 188, 29),
    
    range(10, 11): (194, 24, 7),
    range(11, 12): (6,77, 160),
    range(12, 13): (255, 170, 0),
    range(13, 14): (240, 240, 240),
    range(20, 21): (30, 30, 30),
    range(100, 101): (30, 30, 30)
}

COLOR_MAP = {
    range(0, 1): (240, 240, 240),
    range(-1, 0): (170, 170, 170),
    range(1, 2): (254, 227, 180),
    range(2, 3): (126, 67, 177),
    range(3, 4): (26, 148, 208),
    range(4, 5): (83, 198, 56),
    range(5, 6): (239, 130, 40),
    range(6, 7): (222, 68, 57),
    range(7, 8): (155,103,60),

    
    range(10, 11): (194, 24, 7),
    range(11, 12): (6,77, 160),
    range(12, 13): (255, 170, 0),
    range(13, 14): (240, 240, 240),
    range(20, 21): (30, 30, 30),
    range(100, 101): (30, 30, 30)
}

# COLOR_MAP = {
#     range(0, 1): (220, 220, 220),
#     range(-1, 0): (170, 170, 170),
#     range(1, 2): (11, 175, 45),
#     range(2, 3): (11, 165, 40),
#     range(3, 4): (11, 155, 35),
#     range(4, 5): (11, 145, 30),
#     range(5, 6): (11, 135, 25),
#     range(6, 7): (11, 125, 20),
#     range(7, 8): (11, 115, 15),
#     range(8, 9): (11, 105, 10),
#     range(9, 10): (11, 95, 5),
    
#     range(10, 11): (194, 24, 7),
#     range(11, 12): (6,77, 160),
#     range(12, 13): (255, 170, 0),
#     range(20, 21): (220, 220, 220)
# }


h_const = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

v_const = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


def explore(grid, x, y, visited, groups,n):
    groups[-1].append((x, y))
    visited.add((x, y))
    for i, j in four_directions:
        next_x = x + i
        next_y = y + j
        if in_bound(grid, next_x, next_y) and \
           grid[next_x][next_y] == n and (next_x, next_y) not in visited:
           explore(grid, next_x, next_y, visited, groups, n)
 
def in_bound(grid, i, j):
    return i >= 0 and i < len(grid) and \
           j >= 0 and j < len(grid[0])
 
def connected_cells(grid, visited, groups, n):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == n and (i,j) not in visited:
                groups.append(list())
                explore(grid, i, j, visited, groups, n)
    return groups


def create_grid(n):
    return [[random.randint(-10, 20) for _ in range(n)] for _ in range(n)]


def map_to_color(x):
    for r, c in COLOR_MAP.items():
        if x in r:
            return c
    else:
        raise ValueError(x)


def map_values_to_colors(value_grid):
    return [[map_to_color(x) for x in row] for row in value_grid]


def print_board(grid,grid2,grid3,grid4,player_counts,pcount_map,counter,ran):
    
    # for i in range(len(grid)):
    #     for j in range(len(grid[0])):
    #         if grid2[i][j]==20:
    #             grid[i][j]=1
    
    # print(grid2)
    
    h_grid = copy.deepcopy(h_const)
    v_grid = copy.deepcopy(v_const)
    
    p1 = grid
    
    s = 100
    p = 45
    p2 = 25
    pad = 5
    epad = 0
    
    p1 = np.kron(p1, np.zeros((s,s)))
    
    # print(p1.size)
    
    d1 = len(grid)
    d2 = len(grid[0])
    
    # print(p1,len(p1))
    # print(grid)
    
    for h in range(4):
        
        h_grid = copy.deepcopy(h_const)
        v_grid = copy.deepcopy(v_const)
    
        # print('h',h)
        hp = pad*h+epad
        lw =2
        
        # print(h)
        # print('Grid:' + str(grid[2][2]))
        for i in range(d1):
            for j in range(d2):
                if h==0 and grid[i][j]>h:
                    for m in range(s*i+hp,s*(i+1)-hp):
                        for n in range(s*j+hp,s*(j+1)-hp):
                            # print(j,k,m,n,grid[j][k])
                            # print(i)
                            p1[m,n]=1
                if h==1 and grid[i][j]>h:
                    for m in range(s*i+hp,s*(i+1)-hp):
                        for n in range(s*j+hp,s*(j+1)-hp):
                            # print(j,k,m,n,grid[j][k])
                            # print(i)
                            p1[m,n]=grid[i][j]
                
                    if i<d1-1 and grid3[i][j]==grid3[i+1][j]:
                        v_grid[i][j] = 1
                        for m in range(s*(i+1)-hp,s*(i+1)+hp):
                            for n in range(s*j+hp,s*(j+1)-hp):
                                p1[m,n]=grid[i][j]

                    if j<d2-1 and grid3[i][j]==grid3[i][j+1]:
                        h_grid[i][j] = 1
                        for m in range(s*i+hp,s*(i+1)-hp):
                            for n in range(s*(j+1)-hp,s*(j+1)+hp):
                                p1[m,n]=grid[i][j]
                            

                    if i>0 and j>0 and (h_grid[i][j-1] + h_grid[i-1][j-1] + v_grid[i-1][j] + v_grid[i-1][j-1] >= 3):
                        # print (i,j, h_grid[i][j-1] , h_grid[i][j] , v_grid[i-1][j] , v_grid[i][j])
                        for m in range(s*(i)-hp,s*(i)+hp):
                            for n in range(s*(j)-hp,s*(j)+hp):
                                p1[m,n]=grid[i][j]
                                
                if h==2:
                    if grid2[i][j]>=100:
                        for m in range(s*i+p2,s*(i+1)-p2):
                            for n in range(s*j+p2,s*(j+1)-p2):
                                # print(j,k,m,n,grid[j][k])
                                # print(i)
                                # print ('circle?',m,n)
                                if (m-s*(i+0.5))**2 + (n-s*(j+0.5))**2 <= (s-2*p2)**2/4:
                                #     print ('circle',m,n)
                                    p1[m,n]=grid2[i][j] 
                    # if grid2[i][j]>=20:
                    #     for m in range(s*i+p2,s*(i+1)-p2):
                    #         for n in range(s*j+p2,s*(j+1)-p2):
                    #             # print(j,k,m,n,grid[j][k])
                    #             # print(i)
                    #             # print ('circle?',m,n)
                    #             if (m-s*(i+0.5))**2 + (n-s*(j+0.5))**2 <= (s-2*p2)**2/4:
                    #             #     print ('circle',m,n)
                    #                 p1[m,n]=grid2[i][j] 
                    elif grid2[i][j]>=1:
                        gv = min(grid2[i][j],2)
                        p3 = max(p - (gv)*5,10)
                        for m in range(s*i+p3-5,s*(i+1)-p3+5):
                            for n in range(s*j+p3-5,s*(j+1)-p3+5):
                                if gv>1:
                                    p1[m,n]=1
                        for m in range(s*i+p3,s*(i+1)-p3):
                            for n in range(s*j+p3,s*(j+1)-p3):
                                if gv>1:
                                    p1[m,n]=grid2[i][j]
                                else:
                                    p1[m,n]=20
                                    
                if h==3 and i<d1 and j<d2-1:
                    for m in range(s*(i),s*(i+1)):
                            for n in range(s*(j+1)-lw,s*(j+1)+lw):
                                if grid4[i][j]!=grid4[i][j+1]:
                                    p1[m,n]=20
                if h==3 and i<d1-1 and j<d2:
                    for m in range(s*(i+1)-lw,s*(i+1)+lw):
                            for n in range(s*(j),s*(j+1)):
                                if grid4[i+1][j]!=grid4[i][j]:
                                    p1[m,n]=20                    
        # if h == 0:
        #     print(h_grid)
        #     print(v_grid)

    # print(p1,len(p1))
    # print(grid)
    
    print_grid = p1
    
    a = np.array(print_grid)
    # n = 10
    # temp_grid = np.kron(a, np.ones((n,n)))
    
    temp_grid = print_grid
    
    print_grid = np.ndarray.tolist(temp_grid)
    
    # print(len(print_grid),len(print_grid[0]))
    
    
    out_location = 'grid'
    
    x,y = divmod(counter+1,2)
    
    out_path = out_location+'-'+ran+'-'+str(y)+'-'+str(x)
    
    color_grid = map_values_to_colors(print_grid)
    draw_image_from_color_grid(color_grid,'out-test/'+out_path)
    
    im1 = Image.open('out-test/'+out_path+'.png')
    
    imlist = []
    
    for j in range(len(player_counts)):
        for k in range(player_counts[j]):
            imlist.append(j)

    imlist2 = []
    
    for j in range(16):
        for k in range(pcount_map[j]):
            imlist2.append(j)
    
    # imlist = [1,2,3,4,5,6,7,8,9,10]
    
    # get_concat_h_blank(im1,imlist,imlist2).save('out-cat/'+out_path+'.png') #,quality=95)


def valid_moves(local_player_counts,grid,grid2,grid3,counter):

    grid = gridPad1(grid,grid2)    
    valid = [] 
    grid5 = copy.deepcopy(grid)
    

    
    g1 = 10
    g2 = 23
    
    directions = [[0,1],[0,-1],[1,0],[-1,0]]
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid5[i][j]=0
            for d in directions:
                if grid[i][j]>0 and ((i<len(grid)-1 and grid[i+1][j]>1) or (j<len(grid[0])-1 and grid[i][j+1]>1) or \
                (i>0 and grid[i-1][j]>1) or (j>0 and grid[i][j-1]>1)):
                    grid5[i][j] = 1
    
    # print(grid5)
    
    
    for p in range(len(local_player_counts)):
        # print(local_player_counts)
        if local_player_counts[p]>0:
            this_piece = pshape_map[p]
            # print("This piece:", this_piece)
            # Need to fix so it only looks at correct rotations and flips for each piece
            for r in range(4):
                for f in range(2):
                    piece = getPiece(this_piece,r,f)
                    # print(piece)
                    p1,p2 = len(piece),len(piece[0])
                    for k in range(g1-p1):
                        for l in range(g2-p2):
                            levels = []
                            same = []
                            llama = []
                            adj = 0
                            for i in range(p1):
                                for j in range(p2):
                                    ip = i+k
                                    jp = j+l
                                    if piece[i][j]>0:
                                        levels.append(grid[ip][jp])
                                        same.append(grid3[ip][jp])
                                        llama.append(grid2[ip][jp])
                                        if grid5[ip][jp]>0: adj = 1
                            if max(levels) == min(levels) and min(levels)==1 and (counter<2 or adj>0) and (20 not in llama):
                                # if max(levels) == 3:
                                #     print(2)
                                valid.append([p,k,l,r,f])
                            
    return(valid)
                        
     
                        
def score_board(grid,grid2,grid4):
    
    famscores = [0,2,5,8,11,15,20,25,30,35,40,45,50,55,60]
    roomfilled = [0,0,0,0,0,0,0]
    roomsizes = [60, 18, 11, 11, 18, 20, 4]
    
    
    this_score = 0 
    
    gridt = copy.deepcopy(grid)

    for i in range(2,7):
       groups = list()
       visited = set()
       ifams = connected_cells(gridt, visited, groups, i)
       hsizes = [len(hole) for hole in ifams]
       # print(hsizes)
       if len(ifams)>0:
           hscores = [famscores[int((len(ifam)+1)/5)] for ifam in ifams]
           this_score += sum(hscores)   
        
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]>1 or grid2[i][j]==20:
                gridt[i][j]=2
 
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid4[i][j]>0 and grid[i][j]>1:
                roomfilled[grid4[i][j]-1] += 1
                
    rleft = [r1-r2 for (r1,r2) in zip(roomsizes,roomfilled)]
                
    for r in rleft:
        this_score += 5*1/(r+1)
        
    

    # print('Grid + score:')
    # print(grid)
    # print(grid4)
    # print(roomfilled) 

    for  i in range(len(grid)-1):
        for j in range(len(grid[0])):
            if min(grid[i][j],grid[i+1][j])>0:
                this_score-=0.2*abs(gridt[i][j]-gridt[i+1][j])

    for  i in range(len(grid)):
        for j in range(len(grid[0])-1):
            if min(grid[i][j],grid[i][j+1])>0:
                this_score-=0.2*abs(gridt[i][j]-gridt[i][j+1])

    # for  i in range(len(grid)):
    #     for j in range(len(grid[0])):
    #         this_score+=10*gridt[i][j]


    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > 0: 
                # this_score += grid[i][j]*0.25*((i-5.5)**2+(j-5.5)**2)
                # this_score += 0.2*((i-5.5)**2+(j-5.5)**2)
                this_score += 0
                


                    

                
    groups = list()
    visited = set()
    holes = connected_cells(gridt, visited, groups, 1)
    
    hsizes = [len(hole) for hole in holes]


    # for i in range(len(hsizes)):
    #     this_score -= 5/hsizes[i]
            
    # this_score -= 5*len(holes)



    return this_score            


def valid_llama(grid,grid2):
    candidates = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > 0 and grid2[i][j]==0: 
                candidates.append([i,j])

    return candidates

def add_llama(grid2,pos):
    
    temp_grid2 = copy.deepcopy(grid2)
    temp_grid2[pos[0]][pos[1]] = 20
    
    return temp_grid2


def is_inside(a,b):
    ab = 8
    bb = 12
    if a>0 and a<ab and b>0 and b<ab:
        return 1
    else: 
        return 0


def try_move(grid,temp_grid2,player_counts,piece,location,fr):
    
    temp_grid = copy.deepcopy(grid)
    
    res_score = 0
    new_pieces = 0
    new_boards = 0
    
    if fr != 0:
        piece = getPiece(piece,fr[0],fr[1])
    
    l = location
    p1,p2 = len(piece),len(piece[0])
    pa = sum(player_counts)-1
    
    for i in range(p1):
        for j in range(p2):
            ip = i+l[0]
            jp = j+l[1]
            if piece[i][j]>0:
                # temp_grid[ip][jp] += 1
                temp_grid[ip][jp] = piece[i][j]
                if temp_grid2[ip][jp]==1:
                    res_score+=1
                elif temp_grid2[ip][jp]>1:
                    if temp_grid[ip][jp]==temp_grid2[ip][jp]:
                        res_score += 2
                        new_pieces += 1
                    else:
                        res_score -= 1
    
    # if sum(new_pieces)+pa== 0:
    #     res_score -= 100
        
    return temp_grid, res_score, new_pieces, new_boards


def make_move(grid,grid2,grid3,grid4,piece,location,fr,su,n):
    
    # print(piece,location)
    
    if fr != 0:
        piece = getPiece(piece,fr[0],fr[1])
    
    l = location
    covered = set()
    p1,p2 = len(piece),len(piece[0])
    
    for i in range(p1):
        for j in range(p2):
            ip = i+l[0]
            jp = j+l[1]
            if piece[i][j]>0:
                if grid[ip][jp]>0:
                    covered.add(grid3[ip][jp])
                grid[ip][jp] += 1
                grid[ip][jp] = piece[i][j]
                # grid2[ip][jp] = 0
                grid3[ip][jp] = n
                # grid4[ip][jp] = 1
           
    # print(covered)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid3[i][j] in covered: # and grid3[ip][jp]!=n:
                hej = 1
                # grid4[i][j]=0
                # print(i,j)
                
                
    return grid,grid2,grid3,grid4
                
            

def draw_image_from_color_grid(color_grid,name):
    im = Image.new(mode='RGB', size=(len(color_grid[0]), len(color_grid)))
    #im = Image.new(mode='RGB', size=(288,588))
    im.putdata([x for row in color_grid for x in row])
    #print(im.size)
    #im.show()
    im.save(name+'.png', 'PNG',quality=100)

def draw_image_from_color_grid2(color_grid,name):
    im = Image.new(mode='RGB', size=(len(color_grid[0]), len(color_grid)))
    #im = Image.new(mode='RGB', size=(288,588))
    im.putdata([x for row in color_grid for x in row])
    #print(im.size)
    #im.show()
    im.save(name+'.jpg', 'JPEG',quality=100)

def getPiece(this_piece,rot,flip):

    
    if flip == 1:
        this_piece = this_piece[::-1]
    if rot > 0:
        for i in range(0,rot):
            this_piece = np.rot90(np.array(this_piece)).tolist()    

    return this_piece


def getBestMove(valid,player_counts,grid,grid2,grid4,game_type):
    
    scores = []
    
    if game_type == 'random':
        lv = random.randint(0,len(valid)-1)
        this_move = valid[lv]
    
    else:
        # "Optimized move"
        
        for x in range(len(valid)):
            this_move = valid[x]
            p = this_move[0]
            piece = pshape_map[p]
            l1 = this_move[1]
            l2 = this_move[2]
            r = this_move[3]
            f = this_move[4]
            
            temp_grid = copy.deepcopy(grid)
            temp_grid, res_score, new_pieces, new_boards = try_move(grid,grid2,player_counts,piece,[l1,l2],[r,f])
            scores.append(res_score+score_board(temp_grid,grid2,grid4))
            # res_scores.append(res_score)
        
        max_value = max(scores)
        
        max_scores = []
        
        for x in range(len(scores)):
            if scores[x]==max_value:
                max_scores.append(x)
        
        max_index = random.choice(max_scores)           
        this_move = valid[max_index]  
        
        return this_move,max_value
        
def countX(lst, x):
    return lst.count(x)

def get_minvalue(inputlist):
 
    #get the minimum value in the list
    min_value = min(inputlist)
 
    #return the index of minimum value 
    min_index=inputlist.index(min_value)
    return min_index

def gridPad(grid,grid2):
    for i1 in range(len(grid)):
        for j1 in range(len(grid[0])):
            if grid2[i1][j1]==20:
                grid[i1][j1]=2
    return grid

def gridPad1(grid,grid2):
    for i1 in range(len(grid)):
        for j1 in range(len(grid[0])):
            if grid2[i1][j1]==20:
                grid[i1][j1]=1
    return grid

def pCounter(counts):
    sq = 0
    for i in range(len(counts)):
        if i <12:
            sq += 5*counts[i]
        elif i<16:
            sq += 4*counts[i]
        elif i<18:
            sq += 3*counts[i]
        elif i==18:
            sq += 2*counts[i]
        else:
            sq += counts[i]
    return sq

def main(ran,verbose=0):
    
    # grid = shapes on the board
    # grid2 = resources on the board (rats/treasures)
    # grid3 = move counter (swap with state2)
    # grid4 = 'rooms' on the board (for scoring)

    grid = \
        [[0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0]]
    
    grid2 = [[0,0,0,0,0,0,0,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,1,1,0,0,0,0,0],
        [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,2,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0],
        [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,6,0,1,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0]]
        
    grid3 = \
        [[0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0]]
    
    grid4 = [\
        [0,0,0,0,0,0,0,3,3,3,3,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,3,3,3,3,3,3,3,1,1,1,1,1,6,0,0,0,0,0],
        [0,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,0,0,0],
        [2,2,2,2,1,5,5,5,5,5,5,1,1,1,1,1,6,6,6,6,7,0],
        [2,2,2,2,1,5,5,5,5,5,5,1,1,1,1,1,6,6,6,6,7,7],
        [2,2,2,2,1,5,5,5,5,5,5,1,1,1,1,1,6,6,6,6,7,0],
        [0,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,0,0,0],
        [0,0,0,0,4,4,4,4,4,4,4,1,1,1,1,1,6,0,0,0,0,0],
        [0,0,0,0,0,0,0,4,4,4,4,1,1,1,1,0,0,0,0,0,0,0]]
    
    # board_map = [[0,0,0],[0,1,0]]
    # board_adj_map = [[0,1,0],[1,1,1]]
    
    # Defining the deck
    
    pcount_map = [1,1,1,1,1,1,1,1,1,1,1,1,4,4,4,4,8,8,10,20]
    pcount_map = [1]*85
       
    piece_record = []
        
    # One modified map for added potential when some scoring criteria are used
    # pscore_map = [[8],[6],[7],[6],[9],[8],[10],[8],[8],[7],[7],[6],[6,4,2],[6,4,2],[6,4,2],[6,4,2]]
    pscore_map = [[8],[7],[6],[8],[7],[6],[8],[7],[6],[8],[7],[6],[6,4,2],[6,4,2],[6,4,2],[6,4,2]]

    # Grizzly test
    pscore_map = [[10],[10],[10],[9],[9],[9],[8],[8],[8],[7],[7],[7],[8,6,4,2],[8,6,4,2],[8,6,4,2],[8,6,4,2]]

    anames = ['Koala','Panda','Polar','Gobi','Green','Long Food','Long River','Enclosures','All Fours','Double Area']
    anames_exp = ['Empty Enclosure','Double Enclosure','Toilets apart','Food crossing','Corner River','Playground Statue']
    ascore_map = [[8,5],[8,5],[8,5],[8,5],[9,6],[9,6],[10,7],[9,6],[8,5],[10,7]]
    ascore_exp_map = [[8,5],[8,5],[8,5],[9,6],[9,6],[9,6]]
    
    pscores = [20,18,16,14,12,10,8,6,4,2]
    
    # Make directory for export
    # ran = str(random.randint(0,10000))
    ran = str(ran)
    # os.mkdir('out-test/'+ran)
    
    # for i in range(2):
    #     r = random.randint(0,3)
    #     pcount_map[12+r]-=1
        
    # ra = random.sample(range(12),3)
    # # ra = [0,1,3,11]
    # for i in ra:
    #     pcount_map[i]-=1
        
        
    start = pd.starting_grids
    addon = pd.addon_grids
    
    # No need to initiate the grid
    # r = random.randint(0,len(start)-1)
    # for j in range(4):
    #     grid2[4+j][4:8]=start[r][j]
    
    pieces = []
    
    common_pool = set()
    
    supply_counts = [1]*85 + [0]*4 + [5]*5
    
    player_counts = [0]*94
    player_board_counts = [0]*94
    player_record = []
    player_reserve_score = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    player_board_score = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    player_achs = [0,0,0,0,0,0,0,0,0,0]
    player_completed_parks = []
    player_completed_park_scores = []
 
    game_achs = random.sample(range(10),3)
    #Hardcoded values for testing
    # game_achs = [0,1,2,3,4,5,6,7,8,9]
    game_achs = []
    game_achs.sort()
    game_type = 'o'
    # game_score = 0
    # llama_points = 0
    nb_count = 0   
    p_offset = 0
    
    player1_result = []
    player2_result = []
 
 
    # Very hacky way to setup player states for two players 
    # Adjustments in multiple parts of the code:
    # - Player can play anywhere on first turn
    # - Correctly number moves for each player as they are retrieved from the player record to check achievements
    # - Correctly number output files
 
    player1 = dict()
    player2 = dict()
    
    player1['grid'] = copy.deepcopy(grid)
    player1['grid2'] = copy.deepcopy(grid2)
    player1['grid3'] = copy.deepcopy(grid3)
    player1['grid4'] = copy.deepcopy(grid4)
    player1['player_counts'] = copy.deepcopy(player_counts)
    player1['player_board_counts'] = copy.deepcopy(player_board_counts)
    player1['player_record'] = copy.deepcopy(player_record)
    player1['player_reserve_score'] = copy.deepcopy(player_reserve_score)
    player1['player_board_score'] = copy.deepcopy(player_board_score)
    player1['player_achs'] = copy.deepcopy(player_achs)
    player1['player_completed_parks'] = copy.deepcopy(player_completed_parks)
    player1['player_completed_park_scores'] = copy.deepcopy(player_completed_park_scores)
    player1['piece_record'] = copy.deepcopy(piece_record)
    player1['nb_count'] = copy.deepcopy(nb_count)
    player1['p_offset'] = copy.deepcopy(p_offset)

    player2['grid'] = copy.deepcopy(grid)
    player2['grid2'] = copy.deepcopy(grid2)
    player2['grid3'] = copy.deepcopy(grid3)
    player2['grid4'] = copy.deepcopy(grid4)
    player2['player_counts'] = copy.deepcopy(player_counts)
    player2['player_board_counts'] = copy.deepcopy(player_board_counts)
    player2['player_record'] = copy.deepcopy(player_record)
    player2['player_reserve_score'] = copy.deepcopy(player_reserve_score)
    player2['player_board_score'] = copy.deepcopy(player_board_score)
    player2['player_achs'] = copy.deepcopy(player_achs)
    player2['player_completed_parks'] = copy.deepcopy(player_completed_parks)
    player2['player_completed_park_scores'] = copy.deepcopy(player_completed_park_scores)    
    player2['piece_record'] = copy.deepcopy(piece_record)    
    player2['nb_count'] = copy.deepcopy(nb_count)
    player2['p_offset'] = copy.deepcopy(p_offset)
    
    stop = 0
    stop1 = 0 
    stop2 = 0
    s=0
    
    
    # Don't print initial board, just the final one
    # print_board(grid,grid2,grid3,grid4,0,ran)
    
    # print(grid2)
    
    
    for i in range(40):
        
        # Update player states before turn - player is not aware of player state for opponent, but common resources are shared.

        if i%2 == 0:
            grid = copy.deepcopy(player1['grid'])
            grid2 = copy.deepcopy(player1['grid2'])
            grid3 = copy.deepcopy(player1['grid3'])
            grid4 = copy.deepcopy(player1['grid4'])
            player_counts = copy.deepcopy(player1['player_counts'])
            player_board_counts = copy.deepcopy(player1['player_board_counts'])
            player_record = copy.deepcopy(player1['player_record'])
            player_reserve_score = copy.deepcopy(player1['player_reserve_score'])
            player_board_score = copy.deepcopy(player1['player_board_score'])
            player_achs = copy.deepcopy(player1['player_achs'])
            player_completed_parks = copy.deepcopy(player1['player_completed_parks'])
            player_completed_park_scores = copy.deepcopy(player1['player_completed_park_scores'])
            piece_record = copy.deepcopy(player1['piece_record'])
            nb_count = copy.deepcopy(player1['nb_count'])
            p_offset = copy.deepcopy(player1['p_offset'])
        else:
            grid = copy.deepcopy(player2['grid'])
            grid2 = copy.deepcopy(player2['grid2'])
            grid3 = copy.deepcopy(player2['grid3'])
            grid4 = copy.deepcopy(player2['grid4'])
            player_counts = copy.deepcopy(player2['player_counts'])
            player_board_counts = copy.deepcopy(player2['player_board_counts'])
            player_record = copy.deepcopy(player2['player_record'])
            player_reserve_score = copy.deepcopy(player2['player_reserve_score'])
            player_board_score = copy.deepcopy(player2['player_board_score'])
            player_achs = copy.deepcopy(player2['player_achs'])
            player_completed_parks = copy.deepcopy(player2['player_completed_parks'])
            player_completed_park_scores = copy.deepcopy(player2['player_completed_park_scores'])
            piece_record = copy.deepcopy(player2['piece_record'])
            nb_count = copy.deepcopy(player2['nb_count'])
            p_offset = copy.deepcopy(player2['p_offset'])

        if verbose == 1:
            print(i,grid,grid2,player_counts)
    
        
        # print('Player record',player_record)
    
        # grid = gridPad(grid, grid2)
        
        clen = 0
        
        if i%8 == 0:
            while clen<8:
                r = random.choices(range(len(supply_counts)),weights = supply_counts)
                # r = random.randint(0,84)
                supply_counts[r[0]]-=1    
                # Common pool needs to handle duplicate and be a list instead of a set
                common_pool.add(r[0])
                if r[0]<85:
                    clen+=1
        
        for r in common_pool:
            if r<85:
                player_counts[r]+=1
        
    
        # if i==0:
        #     # print('Adding a toilet...')
        #     # pieces.append(small_pieces[0])
        #     player_counts[19]+=1
        # elif i==1:
        #     player_counts[18]+=1
    
        # print("Player counts:", player_counts)
    
        # if i%1==0: print(i)
    
        valid = valid_moves(player_counts,grid,grid2,grid3,i)
        # print('Valid moves',len(valid),player_counts)
        scores = []
        res_scores = []
        
        if len(valid)==0 and stop==0:
            print(i)
            if (i%2==0 and stop1==0) or (i%2==1 and stop2==0):
                print_board(grid,grid2,grid3,grid4,player_counts,pcount_map,i+s,ran)
            # print(player_record)
            # print(player_counts[0:12],player_counts[12:16],player_counts[16:20])
            # print(player_board_counts)
            # print(pcount_map)
            
            if (i%2==0 and stop1==0) or (i%2==1 and stop2==0):
            
                piece_score = [sum([sum(p) for p in player_board_score[:12]]),sum([sum(p) for p in player_board_score[12:]])]
                # print([sum(p) for p in player_reserve_score])
                total_score = sum(piece_score)+sum(player_completed_park_scores)+sum(player_achs)
                print(ran,i%2+1,total_score,piece_score, player_completed_park_scores,player_achs)
                
                if i%2==0:
                    player1_result=[total_score,piece_score,player_completed_park_scores,player_achs]
                else:
                    player2_result=[total_score,piece_score,player_completed_park_scores,player_achs]
                
            if i%2==0:
                stop1=1
            elif i%2==1:
                stop2=1
            if stop1==1 and stop2==1:
                stop=1
            # print('----------')
            # stop=1       
        elif len(valid)==0:
            a = 2+2
        else:
            
            # print(player_counts, sum(player_counts))
            
            
            this_move,max_value = getBestMove(valid,player_counts,grid,grid2,grid4,'o')
            p,l1,l2,r,f = this_move
            piece = pshape_map[p]
    
            temp_grid, res_score, new_pieces, new_boards = try_move(grid,grid2,player_counts,piece,[l1,l2],[r,f])
            
            # print(this_move, new_pieces)
            
            x,y = divmod(i,2)
            
            grid,grid2,grid3,grid4 = make_move(grid, grid2, grid3, grid4, piece, [l1,l2],[r,f],0, x+p_offset+2)
    
            player_counts = [0]*94
            common_pool.remove(p)
            player_record.append(this_move)
            player_board_counts[p]+=1
            
            # print(player_counts)
            
            if new_pieces > 0:
                p_offset += 1
                player_counts[85:89] = [1,1,1,1]
                for r in common_pool:
                    if r>=89:
                        player_counts[r]+=1
                # Need to check that there are valid moves, or bring out to the outside loop. In practice there should always be a valid move
                valid = valid_moves(player_counts,grid,grid2,grid3,i+2*p_offset)
                # print(player_counts)
                this_move,max_value = getBestMove(valid,player_counts,grid,grid2,grid4,'o')
                p,l1,l2,r,f = this_move
                piece = pshape_map[p]
        
                temp_grid, res_score, new_pieces, new_boards = try_move(grid,grid2,player_counts,piece,[l1,l2],[r,f])
                
                # print(this_move, new_pieces)
                
                x,y = divmod(i,2)
                
                grid,grid2,grid3,grid4 = make_move(grid, grid2, grid3, grid4, piece, [l1,l2],[r,f],0, x+p_offset+2)
        
                # player_counts[p] -= 1
                player_record.append(this_move)
                player_board_counts[p]+=1
                if p>=89:
                    common_pool.remove(p)
                
                player_counts = [0]*94

            print_board(grid,grid2,grid3,grid4,player_counts,pcount_map,i+s,ran)
            
            # Need to recover the scores later
            # if p<=15:
            #     player_board_score[p].append(player_reserve_score[p][0])
                # player_reserve_score[p].pop(0)
            
                    
            if verbose == 1:
                print_board(grid,grid2,grid3,grid4,player_counts,pcount_map,i+s+1,ran)

            if i%2 == 0:
                player1['grid'] = copy.deepcopy(grid)
                player1['grid2'] = copy.deepcopy(grid2)
                player1['grid3'] = copy.deepcopy(grid3)
                player1['grid4'] = copy.deepcopy(grid4)
                player1['player_counts'] = copy.deepcopy(player_counts)
                player1['player_board_counts'] = copy.deepcopy(player_board_counts)
                player1['player_record'] = copy.deepcopy(player_record)
                player1['player_reserve_score'] = copy.deepcopy(player_reserve_score)
                player1['player_board_score'] = copy.deepcopy(player_board_score)
                player1['player_achs'] = copy.deepcopy(player_achs)
                player1['player_completed_parks'] = copy.deepcopy(player_completed_parks)
                player1['player_completed_park_scores'] = copy.deepcopy(player_completed_park_scores)
                player1['piece_record'] = copy.deepcopy(piece_record)
                player1['nb_count'] = copy.deepcopy(nb_count)
                player1['p_offset'] = copy.deepcopy(p_offset)
        
            else:
                player2['grid'] = copy.deepcopy(grid)
                player2['grid2'] = copy.deepcopy(grid2)
                player2['grid3'] = copy.deepcopy(grid3)
                player2['grid4'] = copy.deepcopy(grid4)
                player2['player_counts'] = copy.deepcopy(player_counts)
                player2['player_board_counts'] = copy.deepcopy(player_board_counts)
                player2['player_record'] = copy.deepcopy(player_record)
                player2['player_reserve_score'] = copy.deepcopy(player_reserve_score)
                player2['player_board_score'] = copy.deepcopy(player_board_score)
                player2['player_achs'] = copy.deepcopy(player_achs)
                player2['player_completed_parks'] = copy.deepcopy(player_completed_parks)
                player2['player_completed_park_scores'] = copy.deepcopy(player_completed_park_scores)    
                player2['piece_record'] = copy.deepcopy(piece_record)
                player2['nb_count'] = copy.deepcopy(nb_count)
                player2['p_offset'] = copy.deepcopy(p_offset)
            
    
            # groups = list()
            # visited = set()
            # holes = connected_cells(grid, visited, groups, 1)
            if verbose == 1:
                print(player_counts[0:12],player_counts[12:16],player_counts[16:20])
                print(player_board_counts)
                print(pcount_map)
                print([sum(p) for p in player_reserve_score])
                print(player_completed_park_scores)
                print(player_achs)
                print('-----------')
            # print(holes)
            # print('--')
            
            
            # print(pieces)
            
            
            # if i%3 == 0:
                
            #     l_scores = []
            #     max_l_scores = []
            #     llama_candidates = valid_llama(grid,grid2)  
                
            #     if game_type == 'random':
            #         lv = random.randint(0,len(llama_candidates)-1)
            #         temp_grid2 = add_llama(grid2,llama_candidates[lv])
                    
            #     else:
            #         for x in range(len(llama_candidates)):
            #             temp_grid2 = add_llama(grid2,llama_candidates[x])
            #             l_score = llama_score(grid,temp_grid2)
            #             l_scores.append(l_score)
                    
            #         max_value = max(l_scores)
            #         # print(max_value)
                    
            #         for x in range(len(l_scores)):
            #             if l_scores[x]==max_value:
            #                 max_l_scores.append(x)
            
            #         max_l_index = random.choice(max_l_scores)
                
            #         llama_points = l_scores[max_l_index]
                
            #         # print(llama_candidates,max_l_index)
                
            #         grid2 = add_llama(grid2,llama_candidates[max_l_index])
            
            
    
    grid = gridPad(grid, grid2)

    groups = list()
    visited = set()
    holes = connected_cells(grid, visited, groups, 1)
    
    # print(len(test))
    
    
    
    # print(grid)
    if verbose == 1:
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in grid]))
        print('-----------------------')
        print(llama_points, game_score)
    # print('\n'.join([' '.join([str(cell) for cell in row]) for row in grid2]))
    # print('-----------------------')
    # print('\n'.join([' '.join([str(cell) for cell in row]) for row in grid3]))
    # print('-----------------------')
    # print('\n'.join([' '.join([str(cell) for cell in row]) for row in grid4]))
    # print('-----------------------')
    
    print('-----------------------')  
    return player1_result,player2_result
    # print_board(grid,grid2,grid3,grid4,i)
    

empty_grid = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    
temp_grid = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

big_pieces = [[[1,1,1],[0,1,0],[0,1,0]],[[0,1,1],[1,1,0],[1,0,0]],[[0,1,0],[1,1,1],[0,1,0]],[[0,0,1],[1,1,1],[1,0,0]],[[1,1,1],[1,0,1]]]#,[[1,1,1,1,1]]]
medium_pieces = [[[3,3,3],[3,0,0]],[[4,4,0],[0,4,4]],[[5,5,5],[0,5,0]],[[6,6],[6,6]]]
small_pieces = [[[2,2],[2,0]],[[2,2,2]],[[2,2]],[[2]]]




big_pieces = [[[3,3,3],[3,0,3]],[[3,3,3],[3,0,0],[3,0,0]],[[3,3,3,3],[3,0,0,0]],\
                [[0,4,4],[4,4,0],[4,0,0]],[[4,4,4,0],[0,0,4,4]],[[4,4,4,4],[0,4,0,0]],\
              [[0,5,0],[5,5,5],[0,5,0]],[[5,5,5],[0,5,0],[0,5,0]],[[5,5,5,5,5]],\
                  [[0,0,6],[6,6,6],[6,0,0]],[[0,6,0],[6,6,6],[6,0,0]],[[6,6,6],[6,6,0]]]

big_pieces = [[[1,0,0],[1,1,1],[1,0,1]],[[1,1,1,1],[0,1,0,0],[0,1,0,0]],[[1,1,1,0],[0,1,1,1]],\
            [[0,1,1],[1,1,1],[0,0,1]],[[0,1,0,0],[1,1,1,1],[0,1,0,0]],[[0,1,1,1],[1,1,0,1]],\
          [[0,1,0],[1,1,1],[0,1,0]],[[1,1,1],[0,1,0],[0,1,0]],[[1,1,1,1,1]],\
              [[0,1,1],[1,1,0],[1,0,0]],[[1,1,1],[1,0,0],[1,0,0]],[[1,1,1],[1,0,1]],[[1,1,1],[1,1,0]],\
        [[0,1,1,1],[1,1,0,0]],[[1,1,1,1],[0,1,0,0]],[[1,1,1,1],[1,0,0,0]],[[1,1,0],[0,1,1]]]
    

big_pieces_adj = []

for i in range(2,7):
    for j in range(len(big_pieces)):
        # print([[_el if _el != 1 else i for _el in _ar] for _ar in big_pieces[j]])
        big_pieces_adj.append([[_el if _el != 1 else i for _el in _ar] for _ar in big_pieces[j]])

treasure_pieces = [[[7]],[[7,7]],[[7,7],[7,0]],[[7,7,7]]]

rare_treasures = [[[7,7,7,7]],[[7,7],[7,7]],[[7,7,0],[0,7,7]],[[7,7,7],[0,7,0]],[[7,7,7],[7,0,0]]]
    
big_piece_scores = [8,7,6,8,7,6,8,7,6,8,7,6]


# big_pieces = [[[3,3,0,0],[0,3,3,0],[0,0,3,3],[0,0,0,3]],[[0,3,0,0],[3,3,3,0],[0,0,3,3],[0,0,3,0]],[[3,3,3,3],[0,3,0,0],[0,3,0,0],[0,3,0,0]],
#               [[4,4,4,4],[0,4,0,0],[4,4,0,0]],[[4,4,0,0],[0,4,4,4],[4,4,0,0]],[[4,4,4,4],[4,0,0,4],[4,0,0,0]],
#               [[5,5,5],[5,0,5],[5,5,0]],[[5,0,5],[5,5,5],[5,0,5]],[[5,5,5],[5,0,5],[5,0,5]],
#               [[6,6,6],[6,6,6],[0,6,0]],[[6,6,0],[6,6,6],[0,6,6]],[[6,6,6,6],[6,6,0,6]]]
# big_piece_scores = [10,10,10,9,9,9,8,8,8,7,7,7]

medium_piece_scores = [4,4,4,4]    
# big_pieces.pop(11)
# big_piece_scores.pop(11)

# Piece definitions and point values. pcolor_map is redundant
pname_map = ['I','L','N','Y','T','W','X','Z','U','V','F','P','l','n','t','o','v','i','j','x']
pshape_map = big_pieces + medium_pieces + small_pieces

pshape_map = big_pieces_adj + treasure_pieces + rare_treasures
pcolor_map = [6,5,3,4,6,5,3,3,4,5,4,6,3,4,5,6,2,2,2,2]

player1_results = []
player2_results = []
    
for m in range(1):
    player1_result,player2_result = main(m+1)
    player1_results.append(player1_result)
    player2_results.append(player2_result)
                
    
    
        