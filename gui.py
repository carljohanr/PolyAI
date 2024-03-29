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

Names = ['X','T','Z','W','U','F','P','I','L','N','Y','V','F0','F1','F2','F3','F4','F5','C0','C1','D0','W0','Z0','X0']

Shapes = [[[0,0,0],[0,1,0],[1,1,1],[0,1,0],[0,0,0]],[[0,0,0],[1,1,1],[0,1,0],[0,1,0],[0,0,0]],[[0,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,0]],[[0,0,0],[1,1,0],[0,1,1],[0,0,1],[0,0,0]],\
          [[0,0,0],[0,0,0],[1,1,1],[1,0,1],[0,0,0]],[[0,0,0],[0,1,1],[1,1,0],[0,1,0],[0,0,0]],[[0,0,0],[1,1,1],[1,1,0],[0,0,0],[0,0,0]],[[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],\
          [[0,1,1],[0,1,0],[0,1,0],[0,1,0],[0,0,0]],[[0,1,0],[0,1,0],[0,1,1],[0,0,1],[0,0,0]],[[0,1,0],[0,1,1],[0,1,0],[0,1,0],[0,0,0]],[[0,0,0],[1,1,1],[1,0,0],[1,0,0],[0,0,0]],\
          [[0,1,1],[0,1,0],[0,1,1],[0,1,0],[0,0,0]],[[0,1,1],[1,1,0],[0,1,0],[0,1,0],[0,0,0]],[[0,1,1],[0,1,0],[1,1,0],[0,1,0],[0,0,0]],[[1,0,0],[1,0,0],[1,1,1],[0,1,0],[0,0,0]],\
          [[1,0,0],[1,1,1],[0,1,0],[0,1,0],[0,0,0]],[[1,0,0],[1,1,0],[0,1,1],[0,1,0],[0,0,0]],[[0,1,1],[0,1,0],[0,1,0],[0,1,1],[0,0,0]],[[0,1,1],[0,1,0],[0,1,1],[0,0,1],[0,0,0]],\
          [[0,1,0],[0,1,1],[0,1,1],[0,1,0],[0,0,0]],[[0,1,1],[0,1,0],[1,1,0],[1,0,0],[0,0,0]],[[1,0,0],[1,1,1],[0,0,1],[0,0,1],[0,0,0]],[[0,1,0],[0,1,1],[1,1,0],[0,1,0],[0,0,0]]]

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
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 660

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fill the screen with white
screen.fill((255, 255, 255))

def render(board,pieces,p1_pieces,p2_pieces):
    
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
    pad = 5
    pads = 1
    psize = 16
    
    pygame.draw.rect(screen,(255, 255, 255), (0, 0, 100, 660), 0)
    pygame.draw.rect(screen,(255, 255, 255), (860, 0, 960, 660), 0)

    
    for a in range(len(p1_pieces)):
        this_piece = p1_pieces[a].id
        if this_piece in Names:
            y+=4*psize
            x=10
            # print(this_piece)
            this_shape = Shapes[Names.index(this_piece)]
            # print(this_shape)
            for i in range(len(this_shape)):
                y-=3*psize
                for j in range(len(this_shape[i])):
                    #print("The current element is " + str(board[i][j]))
                    if(this_shape[i][j] == 1):
                        pygame.draw.rect(screen,(0, 0, 255), (x, y, psize, psize), 0)     
                    else:
                        pygame.draw.rect(screen,(255, 255, 255), (x, y, psize, psize), 0) 
                        
                    y += psize
                x += psize

    y=0

    for a in range(len(p2_pieces)):
        this_piece = p2_pieces[a].id
        if this_piece in Names:
            y+=4*psize
            x=870
            # print(this_piece)
            this_shape = Shapes[Names.index(this_piece)]
            # print(this_shape)
            for i in range(len(this_shape)):
                y-=3*psize
                for j in range(len(this_shape[i])):
                    #print("The current element is " + str(board[i][j]))
                    if(this_shape[i][j] == 1):
                        pygame.draw.rect(screen,(0, 255, 0), (x, y, psize, psize), 0)     
                    else:
                        pygame.draw.rect(screen,(255, 255, 255), (x, y, psize, psize), 0) 
                        
                    y += psize
                x += psize

    for i in range(0, 721, 60):
        pygame.draw.line(screen, (125,125,125), (i+120-1, 0-1), (i+120-1, 840-1), 2)
        pygame.draw.line(screen, (125,125,125), (120-1, i-1), (840-1, i-1), 2)
    
    color_map = [(0,0,255),(0,255,0),(255,0,0),(255,255,255)]
    
    y = 0
    for i in range(len(board)):   
        x = 120
        for j in range(len(board[i])):
            this_loc = board[i][j]
            #print("The current element is " + str(board[i][j]))
            pygame.draw.rect(screen,(255,255,255), (x+pads, y+pads, 60-2*pads, 60-2*pads), 0)
            if this_loc in [1,2,3]:
                this_color = color_map[this_loc-1]
                pygame.draw.rect(screen,this_color, (x+pad, y+pad, 60-2*pad, 60-2*pad), 0)
            else:
                pygame.draw.rect(screen, (255,255,255), (x+pad, y+pad, 60-2*pad, 60-2*pad), 0)              
            x += 60
        y += 60    
    
    y = 0
    for i in range(len(board)):   
        x = 120
        for j in range(len(board[i])):
            this_loc = board[i][j]
            #print("The current element is " + str(board[i][j]))
            if this_loc in [1,2,3]:
                this_color = color_map[this_loc-1]
                if j<len(board[i])-1 and pieces[i][j] == pieces[i][j+1]:
                    pygame.draw.rect(screen,(255,255,255), (x+60-pads, y+pads, 2*pads, 60-2*pads), 0)
                    pygame.draw.rect(screen,this_color, (x+60-pad, y+pad, 2*pad, 60-2*pad), 0)
                if i<len(board)-1 and pieces[i+1][j] == pieces[i][j]:
                    pygame.draw.rect(screen,(255,255,255), (x+pads, y+60-pads, 60-2*pads, 2*pads), 0)  
                    pygame.draw.rect(screen,this_color, (x+pad, y+60-pad, 60-2*pad, 2*pad), 0) 
                    
            x += 60
        y += 60    

    y = 0
    for i in range(len(board)):   
        x = 120
        for j in range(len(board[i])):
            this_loc = board[i][j]
            #print("The current element is " + str(board[i][j]))
            if this_loc in [1,2,3]:
                this_color = color_map[this_loc-1]
                if j<len(board[i])-1 and i<len(board)-1 and pieces[i][j] == pieces[i][j+1] == pieces[i+1][j] == pieces [i+1][j+1]:
                    pygame.draw.rect(screen,this_color, (x+60-pad, y+60-pad, 2*pad, 2*pad), 0) 
                    
            x += 60
        y += 60  

    
    # Update the display
    pygame.display.flip()

def clearGUI():
    screen.fill((255, 255, 255))
    pygame.display.flip()
