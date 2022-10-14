#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 13:23:34 2022

@author: carljohan
"""

import random
import copy

from printb import print_board

def reset(positions):
    """

    This is used for setup before starting the search
    Moves the shape's position so that the top left square is at (0, 0)

    """

    min_x, min_y = min(positions, key=lambda x:x[::-1])

    return tuple(sorted((x-min_x, y-min_y) for x, y in positions))

def variation(positions):
    """
  
    This is used for setup before starting the search
    Returns unique rotations and reflections of the shape

    """
    
    # print(positions,len(positions))
    

    return list({reset(var) for var in (
        positions,
        
        [(x,  y) for x, y in positions], # As defined
        [(y,  x) for x, y in positions], # Mirror

        [(-y,  x) for x, y in positions], # Anti-clockwise 90
        [(-x, -y) for x, y in positions], # 180
        [( y, -x) for x, y in positions], # Clockwise 90

        [(-x,  y) for x, y in positions], # Mirror vertical
        [(-y, -x) for x, y in positions], # Mirror diagonal
        [( x, -y) for x, y in positions], # Mirror horizontal
    )})

shapes = [
    (((0, 1), (1, 0), (1, 1), (1, 2), (2, 0)), "F"),
    (((0, 0), (0, 1), (0, 2), (0, 3), (0, 4)), "I"),
    (((0, 0), (0, 1), (0, 2), (0, 3), (1, 3)), "L"),
    (((0, 2), (0, 3), (1, 0), (1, 1), (1, 2)), "N"),
    (((0, 0), (0, 1), (0, 2), (1, 0), (1, 1)), "P"),
    (((0, 0), (1, 0), (1, 1), (1, 2), (2, 0)), "T"),
    (((0, 0), (0, 1), (1, 1), (2, 0), (2, 1)), "U"),
    (((0, 0), (0, 1), (0, 2), (1, 2), (2, 2)), "V"),
    (((0, 0), (0, 1), (1, 1), (1, 2), (2, 2)), "W"),
    (((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)), "X"),
    (((0, 1), (1, 0), (1, 1), (1, 2), (1, 3)), "Y"),
    (((0, 0), (1, 0), (1, 1), (1, 2), (2, 2)), "Z")
]

# shapes2 = [(((0,0),(1,0),(2,0),(3,0),(3,1),(3,2),(3,3),(4,3),(0,1)),"R")]

shapes4 = [(((0,0),(1,0),(2,0),(0,1)),"l"),(((0,0),(1,0),(1,1),(2,1)),"n"),(((0,0),(1,0),(2,0),(1,1)),"t"),(((0,0),(1,0),(1,1),(0,1)),"o")]
shapes3 = [(((0,0),(1,0),(0,1)),"v"),(((0,0),(1,0),(2,0)),"i"),(((0,0),(1,0)),"j"),(((0,0),),"x")]

smap = ['F','I','L','N','P','T','U','V','W','X','Y','Z','l','n','t','o','v','i','j','x']
cmap = [6,5,3,4,6,5,3,3,4,5,4,6,3,4,5,6,2,2,2,2]


# shapes += shapes2
shapes += shapes4
shapes += shapes3

shape_variations = {shape: variation(shape) for shape, name in shapes}

def pprint(grid, size, transpose=False):
    """

    Function to print the grid in a nice format

    """

    width, height = size
    if transpose:
        for x in range(width):
            print("".join([grid[(x, y)] for y in range(height)]))
    else:
        for y in range(height):
            print("".join([grid[(x, y)] for x in range(width)]))


def make_grid(moves,holes,counter):
    
    grid = [[1,1,1,1,1,1,1,1] for i in range(6)]
    grid2 = [[0,0,0,0,0,0,0,0] for i in range(6)]
    grid3 = [[0,0,0,0,0,0,0,0] for i in range(6)]
    grid4 = [[0,0,0,0,0,0,0,0] for i in range(6)]

    grid = [[1,1,1,1,1,1,1,1,1,1,1,1] for i in range(8)]
    grid2 = [[0,0,0,0,0,0,0,0,0,0,0,0] for i in range(8)]
    grid3 = [[0,0,0,0,0,0,0,0,0,0,0,0] for i in range(8)]
    grid4 = [[0,0,0,0,0,0,0,0,0,0,0,0] for i in range(8)]
            

    # grid = [[1,1,1,1,1,1,1,1,1,1,1] for i in range(5)]
    # grid2 = [[0,0,0,0,0,0,0,0,0,0,0] for i in range(5)]
    # grid3 = [[0,0,0,0,0,0,0,0,0,0,0] for i in range(5)]
    # grid4 = [[0,0,0,0,0,0,0,0,0,0,0] for i in range(5)]
    
    # print(grid)
    
    for mc in range(len(moves)):
        m = moves[mc]
        this_locs = m[1]
        this_piece = m[0]
        this_color = cmap[smap.index(this_piece)]
        
        # print (this_locs,this_piece,this_color)
        
        for l in this_locs:
            grid[l[0]][l[1]] = this_color
            grid3[l[0]][l[1]] = mc+1
        
        for l in range(len(holes)):
            x,y = holes[l]
            grid[y][x] = 20
            grid3[y][x] = len(moves)+1
        
    # print(grid)
        
    print_board(grid,grid2,grid3,grid4,counter)
            
        

def solve(grid, size, available_shapes, available_counts, piece_locs =[], start=0):
    """

    Recursive function that yields completed/solved grids
    Max recursion depth is width*height//5+1

    """

    width, height = size

    # Traverse the grid left to right, then top to bottom like reading a book
    # Look for next open space (".")
    # Divmod function returns quotient and remainder
    
    for i in range(start, width*height):
        y, x = divmod(i, width)
        if grid[(x, y)] == ".":
            for j in range(len(available_shapes)):
                shape=available_shapes[j][0]
                name =available_shapes[j][1]
                # Check each rotation and reflection of shape
                for shape_var in shape_variations[shape]:
                    if all(grid.get((x+xs, y+ys)) == "." for xs, ys in shape_var):
                        temp_grid = grid.copy()
                        temp_shapes = available_shapes.copy()
                        for xs, ys in shape_var:
                            temp_grid[(x+xs, y+ys)] = name
                        temp_counts = available_counts.copy()
                        temp_counts[j]-=1
                        if temp_counts[j]==0:
                            temp_counts.pop(j)
                            temp_shapes.pop(j)
                        
                        temp_piece_locs = piece_locs.copy()
                        
                        temp_piece_locs.append([name,[(x+xs, y+ys) for xs, ys in shape_var]])
                        yield from solve(temp_grid, size, temp_shapes, temp_counts, temp_piece_locs, i+1)
            
            return # No more shapes are found, let previous recursion continue
    # yield final grid when all grid values have been checked
    yield grid, piece_locs

from time import time

def main(width, height, counts, holes):
    """

    Program is faster when width is less than height
    if width is greater than height, swap them around

    Iterate over solve() for more solutions

    """
    
    temp_counts = counts.copy()
    temp_shapes = shapes.copy()
    
    counter = 0

    t = time()
    solutions = []
    # Debugging within tiling loop
    # print(width, height)
    print(counts)
    # print(holes)
    print('----------')

    grid = {(x, y): "." for x in range(width) for y in range(height)}
    for x, y in holes:
        grid[(x, y)] = " "

    if width >= height:
        grid = {(y, x): V for (x, y), V in grid.items()}
        
        # print(grid)
    
        
        for i in reversed(range(len(temp_counts))):
            if temp_counts[i]==0:
                temp_counts.pop(i)
                temp_shapes.pop(i)
            

        for solution in solve(grid, (height, width), temp_shapes, temp_counts, []):
            
            if counter%20==0:
                # pprint(solution[0], (height, width), True)
                # print(solution[1])
                make_grid(solution[1],holes,counter)
                print('----------')
            if counter > 1:
                print("Done!","1+ solutions")
                print(f"{time()-t:.3f}s\n")
                break
            counter += 1
        else:
            if counter>0:
                print("Done!",counter,"solutions")
                print(f"{time()-t:.3f}s\n")
                return 1
            else:
                print("No solution")
                print(f"{time()-t:.3f}s\n")
                return 0
    else:
        for solution in solve(grid, (width, height), shapes):
            counter +=1
            if counter%100==0:
                pprint(solution[0], (width, height))
            # break
        else:
            print("No solution")



holes = []
counts = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0]


# ['F','I','L','N','P','T','U','V','W','X','Y','Z','l','n','t','o','v','i','j','x']


test_grid = \
[[3, 3, 3, 3, 3, 1, 1, 1, 0, 0, 0, 0],
 [2, 4, 3, 3, 2, 2, 2, 1, 0, 0, 0, 0],
 [4, 4, 4, 3, 3, 3, 3, 1, 0, 0, 0, 0],
 [4, 4, 4, 4, 3, 2, 2, 4, 0, 0, 0, 0],
 [1, 4, 5, 2, 2, 2, 4, 4, 0, 0, 0, 0],
 [1, 5, 5, 5, 3, 3, 4, 4, 0, 0, 0, 0],
 [1, 1, 5, 1, 3, 2, 4, 4, 0, 0, 0, 0],
 [1, 1, 1, 1, 3, 2, 4, 1, 0, 0, 0, 0]]

pieces = \
[[[2, 2], [2, 0]], [[2, 2, 2]], [[2]], [[3, 3, 3], [3, 0, 0]]]

fcount = 0

for a in range(len(test_grid)*len(test_grid[0])):
    i,j=divmod(a,len(test_grid[0]))
    if test_grid[i][j] != 1:
        holes.append((j,i))
        fcount+=1

em = 96-fcount

# counts = [0,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0, 0,2,1,2]

counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1]

print(counts)

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

print(em, sq)

# if em>sq:
#     counts[19] += em-sq

x=0

temp_counts = counts.copy()

while x==0:
    x=main(12,8,temp_counts,holes) 
    if x==0:
        temp_counts[19] += 1
    else:
        print(temp_counts)


# Attempt to add additional pieces to pool and then tile

for c in range(12):
    x=0
    temp_counts = counts.copy()
    temp_counts[c] +=1
    while x==0:
        x=main(12,8,temp_counts,holes) 
        if x==0:
            temp_counts[19] += 1
        else:
            print(temp_counts)


# # counts = []

# num_list = random.sample(range(48),9)

# for n in num_list:
#     holes.append(divmod(n,6))

# num_list = random.sample(range(12),7)

# for n in num_list:
#     counts[n] += 1

# main(8,6,counts,holes)




# IQ Puzzler Pro examples
counts = [1,0,1,1,1,0,1,1,1,0,0,0,0,1,1,0,1,0,0,0]
holes = [(0,0),(0,1),(0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(3,3)]
holes = [(0,0),(0,1),(0,2),(1,2),(7,2),(8,2),(9,2),(10,2),(9,1), (3,2),(3,3),(3,4),(4,4),(5,4)]