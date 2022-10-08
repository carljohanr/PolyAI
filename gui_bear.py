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

Names = ['G1','G2','G3','G4','A1','A2','A3','A4','E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12'] #'TR1','TR2','TR3','TR4']

    
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

Shapes = [[[0,0,0],[0,0,0],[0,1,0],[0,0,0],[0,0,0]],[[0,0,0],[0,1,0],[0,1,0],[0,0,0],[0,0,0]],[[0,0,0],[0,1,0],[0,1,1],[0,0,0],[0,0,0]],[[0,0,0],[0,1,0],[0,1,0],[0,1,0],[0,0,0]],\
          [[0,0,0],[0,0,0],[1,1,1],[1,0,0],[0,0,0]],[[0,0,0],[0,1,0],[0,1,1],[0,0,1],[0,0,0]],[[0,0,0],[1,1,1],[0,1,0],[0,0,0],[0,0,0]],[[0,0,0],[0,1,1],[0,1,1],[0,0,0],[0,0,0]],\
          [[0,0,0],[1,1,1],[1,0,1],[0,0,0],[0,0,0]],[[0,0,0],[1,1,1],[0,0,1],[0,0,1],[0,0,0]],[[0,1,0],[0,1,0],[0,1,0],[1,1,0],[0,0,0]],[[0,0,0],[1,1,0],[0,1,1],[0,0,1],[0,0,0]],\
          [[0,1,0],[0,1,0],[0,1,1],[0,0,1],[0,0,0]],[[0,1,0],[1,1,0],[0,1,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,0],[1,1,1],[0,1,0],[0,0,0]],[[0,0,0],[1,1,1],[0,1,0],[0,1,0],[0,0,0]],\
          [[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],[[0,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,0]],[[0,0,0],[0,0,1],[1,1,1],[0,1,0],[0,0,0]],[[0,0,0],[0,1,1],[0,1,1],[0,1,0],[0,0,0]],\
          [[0,1,0],[0,1,1],[0,1,1],[0,1,0],[0,0,0]],[[0,1,1],[0,1,0],[1,1,0],[1,0,0],[0,0,0]],[[1,0,0],[1,1,1],[0,0,1],[0,0,1],[0,0,0]],[[0,1,0],[0,1,1],[1,1,0],[0,1,0],[0,0,0]],\
          [[0,1,0],[1,1,1],[0,1,0],[0,1,0],[0,0,0]],[[1,0,0],[1,1,1],[1,0,0],[1,0,0],[0,0,0]],[[1,1,0],[1,0,0],[1,1,0],[0,1,0],[0,0,0]],[[0,0,0],[1,1,1],[0,1,0],[0,1,1],[0,0,0]],
          [[0,1,0],[1,1,0],[1,1,0],[1,0,0],[0,0,0]],[[0,0,0],[1,1,1],[1,1,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,0],[1,1,0],[1,0,0],[0,0,0]],[[0,0,0],[1,1,0],[1,1,0],[0,0,0],[0,0,0]],\
             [[0,0,0],[1,1,0],[0,1,1],[0,0,0],[0,0,0]],[[0,0,0],[0,1,1],[0,1,0],[0,1,0],[0,0,0]],[[0,0,0],[0,1,0],[0,1,1],[0,1,0],[0,0,0]],[[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,0,0]] ]

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
SCREEN_HEIGHT = 900

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fill the screen with white
screen.fill((255, 255, 255))

def truncId(piece):
    
    if len(piece.id)==4:
        return piece.id[0:-2]
    elif piece.size <=4:
        return piece.id[0:-1]
    else:
        return piece.id


def render(p1_board,p2_board,p1_pieces,p2_pieces, game_pieces):
    
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
    
    x,y = 0,0
    pad = 3
    pads = 0
    size = 50
    psize = 25
    
    bsize = 10
    bpad = (size-bsize)/2
    
    pad2 = 13
    
    xoffset = 20
    
    # pygame.draw.rect(screen,(255, 255, 255), (0, 0, 100, 660), 0)
    # pygame.draw.rect(screen,(255, 255, 255), (860, 0, 960, 660), 0)

    x_adj = 20

    temp_counter = 0

    for boards in [p1_board,p2_board]:
        
        
        y_adj = 170
        if temp_counter >0:
            y_adj = 170
            x_adj = 700
        
        board = boards[0]
        pieces = boards[1]
        rooms = boards[2]
        items = boards[3]
        
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
        color_map = [(11, 185, 35),(0, 100, 0),(140, 140, 140),(0, 191, 255),(238, 188, 29)]
        color_map2 = [(0,0,0),(255,255,255),(255,132,0)]
        black = (0,0,0)
        white = (255,255,255)
        
        y = y_adj
        for i in range(len(board)):   
            x = x_adj
            for j in range(len(board[i])):
                this_loc = board[i][j]
                this_item = items[i][j]
                #print("The current element is " + str(board[i][j]))
                rc_map = [0,1,1,1,2,3,1]
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
                    pygame.draw.rect(screen,this_color, (x+bpad+2, y+pad2, size-2*bpad-4, size-2*pad2), 0)
                    pygame.draw.rect(screen,this_color, (x+pad2, y+bpad+2, size-2*pad2, size-2*bpad-4), 0)
                else:
                    # pygame.draw.rect(screen, (255,255,255), (x+pad, y+pad, size-2*pad, size-2*pad), 0)   
                    useless = 0
                x += size
            y += size
        
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
            
    pygame.draw.rect(screen,(255, 255, 255), (0, y_adj + 9*size + 20, 1140, 5*psize), 0)     

    x = 20
    # print(len(p1_pieces))                    
    for a in range(len(game_pieces)):
        this_piece = truncId(game_pieces[a])
        this_color = game_pieces[a].color
        if this_piece in Names:
            # print(this_piece)
            # print(this_piece)
            x+=4*psize
            y= 20
            # print(this_piece)
            this_shape = Shapes[Names.index(this_piece)]
            # print(this_shape)
            for i in range(len(this_shape)):
                x-=3*psize
                for j in range(len(this_shape[i])):
                    #print("The current element is " + str(board[i][j]))
                    if(this_shape[i][j] == 1):
                        pygame.draw.rect(screen,color_map[this_color-1], (x, y, psize, psize), 0)     
                    else:
                        pygame.draw.rect(screen,(255, 255, 255), (x, y, psize, psize), 0) 
                        
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
            x+=4*psize
            y=y_adj + 9*size + 20
            # print(this_piece)
            this_shape = Shapes[Names.index(this_piece)]
            # print(this_shape)
            for i in range(len(this_shape)):
                x-=3*psize
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
            x+=4*psize
            y=y_adj + 9*size + 20
            # print(this_piece)
            this_shape = Shapes[Names.index(this_piece)]
            # print(this_shape)
            for i in range(len(this_shape)):
                x-=3*psize
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

