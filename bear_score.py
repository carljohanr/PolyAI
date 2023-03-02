#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 19:31:34 2022

@author: carljohan
"""

def in_bounds(i,j,nrow,ncol):
    if i<0 or i>=nrow or j<0 or j>ncol:
        return 0
    else:
        return 1

def cpenalty(grid,grid3):
    
    # Correct to give penalty for empty spaces on the side (perhaps pad first)
    
    nrow = len(grid)
    ncol = len(grid[0])
    
    
    cpenalty = 0
    
    
    for  i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]>0:
                grid[i][j]=1
            if grid3[i][j]==-1:
                print('Not sure...')
                grid[i][j]=1
                

    for  i in range(len(grid)):
        for j in range(len(grid[0])):
            if in_bounds(i,j,nrow,ncol)==0 or grid3[i][j]==0:
                val1 = 1
            else: 
                val1 = grid[i][j]
            if in_bounds(i-1,j,nrow,ncol)==0 or grid3[i-1][j]==0:
                val2 = 1
            else: 
                val2 = grid[i-1][j]
                
            cpenalty+=abs(val1-val2)

    for  i in range(len(grid)):
        for j in range(len(grid[0])):
            
            if in_bounds(i,j,nrow,ncol)==0 or grid3[i][j]==0:
                val1 = 1
            else: 
                val1 = grid[i][j]
            if in_bounds(i,j-1,nrow,ncol)==0 or grid3[i][j-1]==0:
                val2 = 1
            else: 
                val2 = grid[i][j-1]
                
            cpenalty+=abs(val1-val2)
                
    return cpenalty


# 1. 8p 3 koalas
# 2. 8p 3 pandas
# 3. 8p 3 polar bears
# 4. 8p 3 gobis
# 5. 9p 6 connected green areas (use family code from cats?)
# 6. 9p 3 connected food streets
# 7. 10p 3 connected rivers
# 8. 9p 3 connected enclosures
# 9. 8p One animal house of each kind
# 10. 10p Two areas completed at the same time
# 11. 8p Place an enclosure that doesnt cover anything
# 12. 8p Two+ enclosure tiles gained in one turn (need to gain)
# 13. 8p Two toilets 11 spaces apart
# 14. 9p Three different pairs of park areas have food street across
# 15. 9p Three park areas have river in corners
# 16. 9p 3 bear statues are next to a playground


# def achievements (...):
    
    