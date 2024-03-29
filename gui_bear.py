'''
Written for CS 480 - Artificial Intelligence
The following sources were used in developing this code.

https://lorenzod8n.wordpress.com/2007/05/27/pygame-tutorial-2-drawing-lines/
https://realpython.com/pygame-a-primer/
https://sites.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/

Senay - GUI Implementation

'''

# Import the pygame module
import pygame
import copy
import config
# import numpy as np

Names = ['G1','G2','G3','G4','A1','A2','A3','A4','E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12',\
         'GR1','GR2','GR3','GR4','GR5','GR6','GR7','GR8','GR9','GR10','GR11','GR12'] #'TR1','TR2','TR3','TR4']

    
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

Shapes = [[[0],[0],[1],[0],[0]],[[0],[1],[1],[0],[0]],[[0,0],[1,0],[1,1],[0,0],[0,0]],[[0],[1],[1],[1],[0]],\
          [[0,0],[1,1],[1,0],[1,0],[0,0]],[[0,0],[1,0],[1,1],[0,1],[0,0]],[[0,0],[1,0],[1,1],[1,0,],[0,0]],[[0,0],[1,1],[1,1],[0,0],[0,0]],\
          [[0,0],[1,1],[1,0],[1,1],[0,0]],[[0,0,0],[1,1,1],[0,0,1],[0,0,1],[0,0,0]],[[1,0],[1,0],[1,0],[1,1],[0,0]],[[0,0,0],[1,1,0],[0,1,1],[0,0,1],[0,0,0]],\
          [[1,0],[1,0],[1,1],[0,1],[0,0]],[[0,1],[1,1],[0,1],[0,1],[0,0]],[[0,0,0],[0,1,0],[1,1,1],[0,1,0],[0,0,0]],[[0,0,0],[1,1,1],[0,1,0],[0,1,0],[0,0,0]],\
          [[1],[1],[1],[1],[1]],[[0,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,0]],[[0,0,0],[0,0,1],[1,1,1],[0,1,0],[0,0,0]],[[0,0],[1,1],[1,1],[1,0],[0,0]],\
              
          [[1,1,1,1],[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,0,0,0]],[[1,1,0,0],[0,1,1,0],[0,0,1,1],[0,0,0,1],[0,0,0,0]],[[0,1,0,0],[1,1,1,0],[0,0,1,1],[0,0,1,0],[0,0,0,0]],\
            [[1,0,1],[1,1,1],[0,0,1],[0,0,1],[0,0,0]],[[1,1,1],[1,0,0],[1,0,0],[1,1,0],[0,0,0]],[[1,0,1],[1,1,1],[0,1,0],[0,1,0],[0,0,0]],\
            [[0,0,0],[1,1,1],[0,1,0],[1,1,1],[0,0,0]],[[1,1,1],[1,0,0],[1,1,1],[0,0,0],[0,0,0]],[[0,0,0],[1,1,1],[1,0,1],[1,1,0],[0,0,0]],\
            [[0,0,0],[1,1,1],[1,1,1],[0,1,0],[0,0,0]],[[0,0,0],[1,1,0],[1,1,1],[0,1,1],[0,0,0]],[[1,1],[1,0],[1,1],[1,1],[0,0]]]

    
# Shapes = Shapes[0:20]
    
# Initialize pygame
pygame.init()

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1320
SCREEN_HEIGHT = 1100

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fill the screen with white
screen.fill((255, 255, 255))

def truncId(piece):
    
    if len(piece.id)==4 and piece.size<=3:
        return piece.id[0:-2]
    elif piece.size <=4:
        return piece.id[0:-1]
    else:
        return piece.id


def render(p1,p2,p1_pieces,p2_pieces, game_pieces,extra_grids,all_pieces):
    
    global Shapes
    Shapes = Shapes[0:20] + config.Omino_map
    # print(len(Shapes))
    
    pygame.draw.rect(screen,(255, 255, 255), (0, 0, 1400, 1120), 0) 
    
    # print(p1_pieces)
    # print(p2_pieces)
    
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                pygame.exit()
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            pygame.exit()
    
    
    size = 30
    
    x,y = 0,0
    pad = int(size/15)
    pads = 0
    psize = 20
    
    bsize = int(size/3)
    bpad = int((size-bsize)/2)
    
    pad2 = int(size/4)
    
    xoffset = 20
    
    # pygame.draw.rect(screen,(255, 255, 255), (0, 0, 100, 660), 0)
    # pygame.draw.rect(screen,(255, 255, 255), (860, 0, 960, 660), 0)

    x_adj = 20

    temp_counter = 0

    #boardsize
    #adaptible size

    config.params = []

    for player in [p1,p2]:
        
        
        
        y_adj = 310
        if temp_counter >0:
            y_adj = 310
            x_adj = 700
        
        
        boards = player.board
        
        # Add text statistics on board
        black = (0,0,0)
        score = copy.deepcopy(player.score_breakdown)
        gi_string = str(sum(score))+' ' +str(score)
        font1 = pygame.font.SysFont("helveticaneue", 40)
        # font1 = pygame.font.SysFont('Helvetica.ttc', 48)
        img1 = font1.render(gi_string, True, black)
        screen.blit(img1, (x_adj,990))

        black = (0,0,0)
        score = copy.deepcopy(player.has_piece)
        # score = copy.deepcopy(player.board.hole_stats)
        # score = [truncId(p) for p in player.pieces]
        gi_string = str(score)
        font1 = pygame.font.SysFont('helveticaneue', 40)
        img1 = font1.render(gi_string, True, black)
        screen.blit(img1, (x_adj,1040))
        
        board = boards.state
        pieces = boards.state2
        rooms = boards.state3
        items = boards.state4
        
        xs = []
        ys = []
        for i in range(len(rooms)):
            for j in range(len(rooms[0])):
                if rooms[i][j]>0:
                    ys.append(i)
                    xs.append(j)
            
        min_x,max_x,min_y,max_y = min(xs),max(xs),min(ys),max(ys)
        xdim = max_x-min_x+1
        ydim = max_y-min_y+1
        
        size = int(min(75,600/xdim,600/ydim))
        
        xtemp = int((600-size*xdim)/2)
        ytemp = int((600-size*ydim)/2)
        
        x_adj += xtemp
        y_adj += ytemp
        
        
        config.params.append([size,x_adj,y_adj,min_x,min_y])
        
        x,y = 0,0
        pad = int(size/15)
        pads = 0
        psize = 20
        
        bsize = int(size/3)
        bpad = int((size-bsize)/2)
        
        pad2 = int(size/4)
        
        epad = int(size/10)
        
        xoffset = 20
        
        # [board[i][min_x:max_x+1] for i in range(min_y,max_y+1)]
        
        # print(board)
        
        board = copy.deepcopy([board[i][min_x:max_x+1] for i in range(min_y,max_y+1)])
        pieces = copy.deepcopy([pieces[i][min_x:max_x+1] for i in range(min_y,max_y+1)])
        rooms = copy.deepcopy([rooms[i][min_x:max_x+1] for i in range(min_y,max_y+1)])
        items = copy.deepcopy([items[i][min_x:max_x+1] for i in range(min_y,max_y+1)])
        
        # print(min_x,max_x,min_y,max_y)
        # print(board)
        # print(pieces)
        # print(rooms)
        # print(items)
        
        
        
        
        hsize = len(board)
        vsize = len(board[0])        


    
        # y=0
    
        # for a in range(len(p2_pieces)):
        #     this_piece = p2_pieces[a].id
        #     if this_piece in Names:
        #         y+=4*psize
        #         x=870
        #         # print(this_piece)
        #         this_shape = Shapes[Names.index(this_piece)]
        #         # print(this_shape)
        #         for i in range(len(this_shape)):
        #             y-=3*psize
        #             for j in range(len(this_shape[i])):
        #                 #print("The current element is " + str(board[i][j]))
        #                 if(this_shape[i][j] == 1):
        #                     pygame.draw.rect(screen,(0, 255, 0), (x, y, psize, psize), 0)     
        #                 else:
        #                     pygame.draw.rect(screen,(255, 255, 255), (x, y, psize, psize), 0) 
                            
        #                 y += psize
        #             x += psize
    
        # for i in range(0, size*len(board[0])+1, size):
        #     pygame.draw.line(screen, (200,200,200), (i+xoffset-1, y_adj-1), (i+xoffset-1, y_adj+size*hsize-1), 2)
        # for i in range(0, size*len(board)+1, size):        
        #     pygame.draw.line(screen, (200,200,200), (xoffset-1, y_adj+i-1), (xoffset+size*vsize-1, y_adj+i-1), 2)

 
        color_map = [(0,0,255),(0,255,0),(255,0,0),(255,255,255)]
        color_map = [(11, 185, 35),(0, 100, 0),(140, 140, 140),(0, 191, 255),(238, 188, 29),(181, 101, 29)]
        color_map2 = [(0,0,0),(255,255,255),(255,132,0)]
        black = (0,0,0)
        white = (255,255,255)
        
        
        # Board - regular squares
        
        y = y_adj
        for i in range(len(board)):   
            x = x_adj
            for j in range(len(board[i])):
                this_loc = board[i][j]
                this_item = items[i][j]
                #print("The current element is " + str(board[i][j]))
                rc_map = [1,1,1,1,1,1,1]
                if rooms[i][j]>0:
                    rc = rooms[i][j]
                    rcval = rc_map[rc-1]
                    pygame.draw.rect(screen,(220-rcval*30,220-rcval*30,220-rcval*30), (x+pads, y+pads, size-2*pads, size-2*pads), 0)
                else:
                    useless = 0
                    # pygame.draw.rect(screen,(255,255,255), (x+pads, y+pads, size-2*pads, size-2*pads), 0)                    
                if this_loc in [1,2,3,4,5,6]:
                    this_color = color_map[this_loc-1]
                    pygame.draw.rect(screen,this_color, (x+pad, y+pad, size-2*pad, size-2*pad), 0)
                # Items/resources on board
                if this_item in [1,2,3] and this_loc == 0:
                    this_color = color_map2[this_item-1]
                    t = this_item
                    pygame.draw.rect(screen,this_color, (x+bpad-t, y+bpad-t, size-2*bpad+2*t, size-2*bpad+2*t), 0)
                elif this_item in [10] and this_loc == 0:
                    this_color = black
                    pygame.draw.rect(screen,this_color, (x+bpad+epad, y+pad2, size-2*bpad-2*epad, size-2*pad2), 0)
                    pygame.draw.rect(screen,this_color, (x+pad2, y+bpad+epad, size-2*pad2, size-2*bpad-2*epad), 0)
                else:
                    # pygame.draw.rect(screen, (255,255,255), (x+pad, y+pad, size-2*pad, size-2*pad), 0)   
                    useless = 0
                x += size
            y += size
        
        # Board - piece beautification
        
        y = y_adj
        for i in range(len(board)):   
            x = x_adj
            for j in range(len(board[i])):
                this_loc = board[i][j]
                #print("The current element is " + str(board[i][j]))
                if this_loc in [1,2,3,4,5,6]:
                    this_color = color_map[this_loc-1]
                    if j<len(board[i])-1 and pieces[i][j] == pieces[i][j+1]:
                        # pygame.draw.rect(screen,(255,255,255), (x+size-pads, y+pads, 2*pads, size-2*pads), 0)
                        pygame.draw.rect(screen,this_color, (x+size-pad, y+pad, 2*pad, size-2*pad), 0)
                    if i<len(board)-1 and pieces[i+1][j] == pieces[i][j]:
                        # pygame.draw.rect(screen,(255,255,255), (x+pads, y+size-pads, size-2*pads, 2*pads), 0)  
                        pygame.draw.rect(screen,this_color, (x+pad, y+size-pad, size-2*pad, 2*pad), 0) 
                        
                x += size
            y += size    
    
        y = y_adj
        x = x_adj
        for i in range(len(board)):   
            x = x_adj
            for j in range(len(board[i])):
                this_loc = board[i][j]
                #print("The current element is " + str(board[i][j]))
                if this_loc in [1,2,3,4,5,6]:
                    this_color = color_map[this_loc-1]
                    if j<len(board[i])-1 and i<len(board)-1 and pieces[i][j] == pieces[i][j+1] == pieces[i+1][j] == pieces [i+1][j+1]:
                        pygame.draw.rect(screen,this_color, (x+size-pad, y+size-pad, 2*pad, 2*pad), 0) 
                        
                x += size
            y += size
            
         
        # Board - edges/boundary   
         
        tc = 0
        for i in range(0, size*len(board[0])+1, size):
            for j in range(len(board)):
                if (tc==0 and rooms[j][tc]>0) or (tc==len(board[0]) and rooms[j][tc-1]>0) or (tc>0 and tc<len(board[0]) and rooms[j][tc-1]!=rooms[j][tc]):
                    pygame.draw.line(screen, (0,0,0), (i+x_adj-1, y_adj+j*size-1), (i+x_adj-1, y_adj+(j+1)*size-1), 2)   
            tc+=1
           
        tc=0
        for i in range(0, size*len(board)+1, size):
            for j in range(len(board[0])):
                if (tc==0 and rooms[tc][j]>0) or (tc==len(board) and rooms[tc-1][j]>0) or (tc>0 and tc<len(board) and rooms[tc-1][j]!=rooms[tc][j]):
                    # pygame.draw.line(screen, (0,0,0), (i+xoffset-1, y_adj+j*size-1), (i+xoffset-1, y_adj+(j+1)*size-1), 2) 
                    pygame.draw.line(screen, (0,0,0), (x_adj+j*size-1, y_adj+i-1), (x_adj+(j+1)*size-1, y_adj+i-1), 2)
            
            tc+=1
            
            
        temp_counter +=1
            
    y_adj = 120
            
    # pygame.draw.rect(screen,(255, 255, 255), (0, y_adj + 9*size + 20, 1140, 5*psize), 0)     

    y2nd = 0
    u = 0

    x = 20
    # print(len(p1_pieces))                    
    for a in range(len(game_pieces)):
        # print(game_pieces[a])
        this_piece = truncId(game_pieces[a])
        this_color = game_pieces[a].color
        if this_piece[0:2]=='GR' and u == 0:
            y2nd = 120
            x = 20
            u = 1
        if this_piece in Names:
            # print(this_piece)
            # print(this_piece)
            y= 20+y2nd
            # print(this_piece)
            this_shape = Shapes[Names.index(this_piece)]
            xminus = len(this_shape[0])
            x+=(xminus+1)*psize
            # print(this_shape)
            
            if game_pieces[a].score>0:
                gi_string = str(this_piece)+' ('+str(game_pieces[a].score)+')'
            else:
                gi_string = str(this_piece)
            font1 = pygame.font.SysFont("helveticaneue", 14)
            # font1 = pygame.font.SysFont('Helvetica.ttc', 48)
            img1 = font1.render(gi_string, True, black)
            screen.blit(img1, (x-int(len(this_shape[0])/2*psize)-4*len(gi_string),y-psize))
            
            
            for i in range(len(this_shape)):
                x-=len(this_shape[0])*psize
                for j in range(len(this_shape[i])):
                    #print("The current element is " + str(board[i][j]))
                    if(this_shape[i][j] == 1):
                        pygame.draw.rect(screen,color_map[this_color-1], (x, y, psize, psize), 0)     
                    else:
                        pygame.draw.rect(screen,(255, 255, 255), (x, y, psize, psize), 0) 
                        
                    x += psize
                y += psize

    color_dict = {-1:(255,0,0),0:(200,200,200),1:(0,0,0),2:(255,255,255),3:(255,132,0),10:(0,0,0)}

    for a in range(len(extra_grids)):
        this_shape = extra_grids[a]
        xminus = len(this_shape[0])
        x+=(xminus+1)*psize
        y= 20+y2nd
        for i in range(len(this_shape)):
            x-=len(this_shape[0])*psize
            for j in range(len(this_shape[i])):
                tl = this_shape[i][j]
                if tl != -1:
                    pygame.draw.rect(screen,color_dict[0], (x, y, psize, psize), 0)
    
                if tl == 10:
                    pygame.draw.rect(screen,color_dict[tl], (x+8, y+2, psize-16, psize-4), 0) 
                    pygame.draw.rect(screen,color_dict[tl], (x+2, y+8, psize-4, psize-16), 0) 
                elif tl in [1,2,3]:
                    pygame.draw.rect(screen,color_dict[tl], (x+5, y+5, psize-10, psize-10), 0) 
                        
                x += psize
            y += psize


    
    x = 20
    # print(len(p1_pieces))                    
    for a in range(len(p1_pieces)):
        this_piece = truncId(p1_pieces[a])
        this_color = p1_pieces[a].color
        if this_piece in Names:
            # print(this_piece)
            # print(this_piece)
            y=y_adj + 9*size + 100
            # print(this_piece)
            this_shape = Shapes[Names.index(this_piece)]
            xminus = len(this_shape[0])
            x+=(xminus+1)*psize
            # print(this_shape)
            for i in range(len(this_shape)):
                x-=len(this_shape[0])*psize
                for j in range(len(this_shape[i])):
                    #print("The current element is " + str(board[i][j]))
                    if(this_shape[i][j] == 1):
                        pygame.draw.rect(screen,color_map[this_color-1], (x, y, psize, psize), 0)     
                    else:
                        pygame.draw.rect(screen,(255, 255, 255), (x, y, psize, psize), 0) 
                        
                    x += psize
                y += psize
                
    x = 720
    # print(len(p1_pieces))                    
    for a in range(len(p2_pieces)):
        this_piece = truncId(p2_pieces[a])
        this_color = p2_pieces[a].color
        if this_piece in Names:
            # print(this_piece)
            # print(this_piece)
            y=y_adj + 9*size + 100
            # print(this_piece)
            this_shape = Shapes[Names.index(this_piece)]
            xminus = len(this_shape[0])
            x+=(xminus+1)*psize
            # print(this_shape)
            for i in range(len(this_shape)):
                x-=len(this_shape[0])*psize
                for j in range(len(this_shape[i])):
                    #print("The current element is " + str(board[i][j]))
                    if(this_shape[i][j] == 1):
                        pygame.draw.rect(screen,color_map[this_color-1], (x, y, psize, psize), 0)     
                    else:
                        pygame.draw.rect(screen,(255, 255, 255), (x, y, psize, psize), 0) 
                        
                    x += psize
                y += psize
    
    # Update the display
    pygame.display.flip()

def clearGUI():
    screen.fill((255, 255, 255))
    pygame.display.flip()

