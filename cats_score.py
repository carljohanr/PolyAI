#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 20:52:14 2022

@author: carljohan
"""

# def try_move(grid,grid2,grid3, placement,color):
    
#     #print(self.state)
#     #print(self.state2)
#     nrow = 9
#     ncol = 22
    
#     maxval = max([max(s) for s in grid2])
#     for row in range(nrow):
#         for col in range(ncol):
#             if(col, row) in placement:
#                 grid[row][col] = color;
#                 grid2[row][col] = maxval+1


import copy

four_directions = [[0,1],[0,-1],[1,0],[-1,0]]

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

def score_board(grid,grid2,grid4):
    
    famscores = [0,2,5,8,11,15,20,25,30,35,40,45,50,55,60]
    roomfilled = [0,0,0,0,0,0,0]
    roomsizes = [60, 18, 11, 11, 18, 20, 4]
    hall = []
    
    this_score = 0 
    

    for i in range(1,6):
       groups = list()
       visited = set()
       ifams = connected_cells(grid, visited, groups, i)
       hsizes = [len(hole) for hole in ifams]
       # print(hsizes)
       if len(ifams)>0:
           hscores = [famscores[int((len(ifam)+1)/5)] for ifam in ifams]
           hall += hscores
           this_score += sum(hscores)   
 
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

    for  i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]>0:
                grid[i][j]=1

    for  i in range(len(grid)-1):
        for j in range(len(grid[0])):
            if min(grid[i][j],grid[i+1][j])>0:
                this_score-=0.1*abs(grid[i][j]-grid[i+1][j])

    for  i in range(len(grid)):
        for j in range(len(grid[0])-1):
            if min(grid[i][j],grid[i][j+1])>0:
                this_score-=0.1*abs(grid[i][j]-grid[i][j+1])

    # for  i in range(len(grid)):
    #     for j in range(len(grid[0])):
    #         this_score+=10*gridt[i][j]


    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > 0: 
                # this_score += grid[i][j]*0.25*((i-5.5)**2+(j-5.5)**2)
                # this_score += 0.2*((i-5.5)**2+(j-5.5)**2)
                this_score += 0
                


                    

                
    # groups = list()
    # visited = set()
    # holes = connected_cells(gridt, visited, groups, 1)
    
    # hsizes = [len(hole) for hole in holes]


    # for i in range(len(hsizes)):
    #     this_score -= 5/hsizes[i]
            
    # this_score -= 5*len(holes)



    return this_score, hall


