#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 19:31:34 2022

@author: carljohan
"""

def cpenalty(grid,grid3):
    
    # Correct to give penalty for empty spaces on the side (perhaps pad first)
    
    cpenalty = 0
    
    for  i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]>0:
                grid[i][j]=1
            if grid3[i][j]==-1:
                print('Not sure...')
                grid[i][j]=1
                

    for  i in range(len(grid)-1):
        for j in range(len(grid[0])):
            if min(abs(grid3[i][j]),abs(grid3[i+1][j]))>0:
                cpenalty+=abs(grid[i][j]-grid[i+1][j])

    for  i in range(len(grid)):
        for j in range(len(grid[0])-1):
            if min(abs(grid3[i][j]),abs(grid3[i][j+1]))>0:
                cpenalty+=abs(grid[i][j]-grid[i][j+1])
                
    return cpenalty