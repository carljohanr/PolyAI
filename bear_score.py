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
    
    