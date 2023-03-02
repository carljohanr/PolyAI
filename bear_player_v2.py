#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 13:45:23 2022

@author: carljohan
"""

import time
import copy
import pygame
import config

# used for alphabeta search
count = 0
testing = 0
BigInitialValue = 1000000

# used for analyzing AI performance
MoveTimes = []
Outcomes = []
Scores1 = []
Scores2 = []

# This function will prompt the user for their piece
def piece_prompt(options,move_type):
    # Create an array with the valid piece names
    
    if move_type == 'expand_board':
        for o in options:
            print(o[1])
            for j in o[2]:
                print(j)
            print('--')
    # print(options)
    
    try:
        option_names = [str(x.id) for x in options];
    except:
        option_names = [str(x) for x in options];

    # Prompt the user for their choice
    print("\nIt's your turn! Select one of the following options:");
    choice = 0;
    # print (option_names)
    
    count = 0
    
    for x in option_names:
        count +=1
        print("     " + str(count) + " - " + str(x));
        
        if count<len(option_names)-1 and option_names[count][0] != x[0]:
            print("     --")
        
        # count += 1;
    
    
    piece = input("Choose a piece: ");
    print("");
    try: 
        if piece in ('p','P'):
            return 'Pass'
        i = int(piece)
        piece = options[i-1]
    except:
        if piece in option_names:  # If the piece name is valid, retrieve the piece object
            i = option_names.index(piece);
            piece = options[i];
        else:
            print("INVALID PIECE. Please try again:");
            choice = 0;
    

    # Once they've chosen a piece...
    return piece;

# This function will prompt the user for their placement
def placement_prompt_old(possibles):
    choice = -1; # An invalid "choice" to start the following loop

    exclude_list=[]

    # While the user hasn't chosen a valid placment...
    while (choice < 1 or choice > len(possibles)):
        # print(exclude_list)
        count = 1; # Used to index each placement; initialized to 1
        # Prompt the user for their placement
        print("Select one of the following placements:")
        for x in possibles:
            if x not in exclude_list:
                printx = x.points
                printx = [(x+1,y+1) for (x,y) in printx]
                printx = set(printx)
                # print(x)
                print("     " + str(count) + " - " + str(printx));
            count += 1;


        # See if the user enters an integer; if they don't, handle the exception
        try:
            this_input = input("Choose a placement: ")
            # print(this_input,'-' in this_input)
            
            
            if '-' in this_input:
                x,y = this_input.split('-')
                this_point = (int(x)-1,int(y)-1)
                # print('P: ', this_point)
                for p in possibles:
                    if this_point not in p.points and p not in exclude_list:
                        exclude_list.append(p)
                if len(possibles)-len(exclude_list) == 1:
                    for z in range(len(possibles)):
                        if possibles[z] not in exclude_list:
                            choice = z+1
                elif len(possibles)-len(exclude_list) == 0:
                    exclude_list = []
                
            else:
                choice = int(this_input);
        except:
            # Do nothing; if the user doesn't enter an integer, they will be prompted again
            pass;
        print("");

    # Once they've made a valid placement...
    placement = possibles[choice - 1];
    return placement;   

# This function will prompt the user for their placement
def placement_prompt(possibles):
    choice = -1; # An invalid "choice" to start the following loop

    exclude_list=[]

    # While the user hasn't chosen a valid placment...
    while (choice < 1 or choice > len(possibles)):
        # print(exclude_list)
        count = 1; # Used to index each placement; initialized to 1
        # Prompt the user for their placement
        # print("Select one of the following placements:")
        for x in possibles:
            if x not in exclude_list:
                printx = x.points
                printx = [(x+1,y+1) for (x,y) in printx]
                printx = set(printx)
                # print(x)
                # print("     " + str(count) + " - " + str(printx));
            count += 1;

        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        ev = pygame.event.get()

        # proceed events
        for event in ev:
          # handle MOUSEBUTTONUP
          if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            # print(pos)
            xpos,ypos = pos[0],pos[1]
            # print(config.params)
            
            p = config.params[0]
            
            this_x = p[3]+int((xpos-p[1])/p[0])
            this_y = p[4]+int((ypos-p[2])/p[0])
            
            # print(this_x,this_y)
            
            this_point = (this_x,this_y)
            # print('P: ', this_point)
            for p in possibles:
                if this_point not in p.points and p not in exclude_list:
                    exclude_list.append(p)
            if len(possibles)-len(exclude_list) == 1:
                for z in range(len(possibles)):
                    if possibles[z] not in exclude_list:
                        choice = z+1
            elif len(possibles)-len(exclude_list) == 0:
                exclude_list = []

    # Once they've made a valid placement...
    placement = possibles[choice - 1];
    return placement;    

# Random Strategy: choose an available piece randomly
def Random_Player(player, game, oval = 1):
    
    if game.move_type in (['add_piece','add_piece_forced']):
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        this_choice = random.choice(possibles)
        # print('Pieces to select from:',possibles, this_choice)
        return this_choice
        
    elif game.move_type == 'play_piece':
        options = [p for p in player.pieces];
        while len(options) > 0: # if there are still possible moves
            piece = random.choice(options);
            # Function returns a piece so does not need to return the color as well (possibles[x].color)
            possibles = player.possible_moves([piece], game);
            if len(possibles) != 0: # if there is possible moves
                m = random.randint(0,len(possibles)-1)
                return possibles[m]
            else: # no possible move for that piece
                options.remove(piece); # remove it from the options
        return None; # no possible move left


def Random_Player_v2(player, game, oval = 1):
    
    if game.move_type in (['add_piece','add_piece_forced']):
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        # this_choice = random.choice(possibles)
        this_choice = max(possibles)
        # print('Pieces to select from:',possibles, this_choice)
        return this_choice

    elif game.move_type == 'expand_board':
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        this_choice = random.choice(possibles)
        return this_choice
        
    elif game.move_type == 'play_piece':
        options = [p for p in player.pieces];
        while len(options) > 0: # if there are still possible moves
            piece = random.choice(options);
            # Function returns a piece so does not need to return the color as well (possibles[x].color)
            possibles = player.possible_moves([piece], game);
            if len(possibles) != 0: # if there is possible moves
                m = random.randint(0,len(possibles)-1)
                return possibles[m]
            else: # no possible move for that piece
                options.remove(piece); # remove it from the options
        return None; # no possible move left

# Greedy Strategy: choose an available piece randomly based on own board only
def Greedy_Player(player, game, oval = 1, single_option = 0):
    
    
    if game.move_type in (['add_piece','add_piece_forced']):
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        
        scores = []
        for p in possibles:
            scores.append(game.all_pieces[p][0].score+game.all_pieces[p][0].size)
          
        max_index,max_score = getMax(possibles,scores)
        
        # print('Scores by piece:',scores,max_index,max_score,possibles[max_index])
        # The heuristic makes sense, but player ends up with holes that cannot be filled. Just picking the top index gets more square pieces
        return possibles[max_index]
        # return max(possibles)

    elif game.move_type == 'expand_board':
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        this_choice = random.choice(possibles)
        return this_choice
        
    elif game.move_type == 'play_piece':
        options = [p for p in player.pieces];
        scores = []
        all_possibles = []
        debug = []
        grid2 = game.players[0].board.state3
        maxval = max([max(s) for s in game.players[0].board.state2])
        temp_counter = 0
        
        # print('Pieces in hand:', options)
        
        # Copying a partial state and evaluating it is unnecessary. Better do it in the update_board class.
        for piece in options:
            # print('Piece:', piece)
            possibles = player.possible_moves([piece], game);
            # print('Options for piece:',piece,len(possibles))
            if len(possibles) != 0: # if there is possible moves
                for m in range(len(possibles)):
                    this_score = 0
                    new_pieces = 0
                    grid = copy.deepcopy(game.players[0].board.state)
                    grid3 = copy.deepcopy(game.players[0].board.state4)
                    # Should make a copy of the state and use the update function instead
                    for (p0,p1) in possibles[m].points:
                        grid[p1][p0]=1
                        if grid3[p1][p0]<10:
                            this_score += 2*grid3[p1][p0]
                            new_pieces +=1
                        elif grid3[p1][p0]==10:
                            this_score += 5
                    if new_pieces + len(player.pieces) < 2:
                        this_score -= 100
                    this_score += possibles[m].score-cpenalty(grid,grid2)
                    # debug.append(fam_dummy)
                    scores.append(this_score)
                    all_possibles.append(possibles[m])            

            else: # no possible move for that piece
                dummy = 0 # Do nothing
                # This statement created issues in the loop since we are looping over options
                # options.remove(piece); # remove it from the options
        
        # print('--')

        temp_counter+=1


        if len(all_possibles)>0:
            max_index,max_score = getMax(all_possibles,scores)
    
            # print(all_possibles[max_index].id)
            return all_possibles[max_index]
        else:
            print('No possible options')
            return None; # no possible move left



# Greedy Strategy: choose an available piece randomly based on own board only
def Winnie(player, game, oval = 1):
    
    # Move selection logic, could also be used for move ranking in search
    # Player prefers pieces that have higher point value, but does not want repeat pieces (mainly relevant for corner and straight pieces)
    
    if game.move_type in (['add_piece','add_piece_forced']):
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        
        scores = []
        mcounts = []
        
        in_stock = 0
        for p in possibles:
            for i in range(len(player.pieces)):
                pid1 = game.all_pieces[p][0].id
                pid2 = player.pieces[i].id
                # Some issues if there are more than 10 pieces (truncId should solve, but need a better solution)
                if pid1 == pid2 or pid1[:-1] == pid2[:-1]:
                    in_stock += 1
            
            mcount =len(player.possible_moves([game.all_pieces[p][0]],game,1))
            if mcount ==0:
                adj = 0
            else:
                adj = 1
            mcounts.append(mcount)
            # if in_stock > 0:
            #     print(in_stock,'already in stock!')
            scores.append(adj*game.all_pieces[p][0].score+adj*game.all_pieces[p][0].size-0.5*in_stock)
         
        # print('Move counts:', mcounts)
        max_index,max_score = getMax(possibles,scores)
        
        # print('Scores by piece:',scores,max_index,max_score,possibles[max_index])
        # The heuristic makes sense, but player ends up with holes that cannot be filled. Just picking the top index gets more square pieces
        return possibles[max_index]
        # return max(possibles)

    elif game.move_type == 'add_grizzly':
        
        dummy = 0
        
        possibles = player.possible_moves_ranked(dummy, game);
        
        # print('Selected grizzly move:',possibles[0])
        # input('Press enter...')
        
        return possibles[0]

    elif game.move_type == 'expand_board':
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        
        scores = []
        all_possibles = []
        
        for m in possibles:
            player_copy = copy.deepcopy(game.players[0])
            player_copy.board.update(player.id,game.move_type,m)   
            player_copy.update_player()
            this_score = player_copy.potential
            # Pieces that are more valuable for the opponent more likely to be considered
            # But the player does not need to worry about where they are placed since board are indpendent
            scores.append(this_score)
            all_possibles.append(m)  
        
        if len(all_possibles)>0:
            max_index,max_score = getMax(all_possibles,scores)
            
        return all_possibles[max_index]
        
        # this_choice = random.choice(possibles)
        # return this_choice
        
    elif game.move_type == 'play_piece':
        options = [p[0] for p in game.all_pieces if len(p)>0];
        # print('Piece ids:', [p.id for p in options])
        scores = []
        all_possibles = []
        debug = []
        
        # print('Pieces in hand:', options)
        
        for piece in options:
            # print('Piece:', piece)
            possibles = player.possible_moves([piece], game);
            # print(len(possibles))
            if len(possibles) != 0: # if there is possible moves
                for m in possibles:
                    player_copy = copy.deepcopy(game.players[0])
                    player_copy.board.update(player.id,game.move_type,m)   
                    player_copy.update_player()
                    this_score = player_copy.potential
                    # Pieces that are more valuable for the opponent more likely to be considered
                    # But the player does not need to worry about where they are placed since board are indpendent
                    scores.append(this_score)
                    all_possibles.append(m)            
    
            # else: # no possible move for that piece
            #     options.remove(piece); # remove it from the options
                
            
        if len(all_possibles)>0:
            max_index,max_score = getMax(all_possibles,scores)
        
            # print(all_possibles[max_index].id)
            return all_possibles[max_index]
        else:
            print('No possible options')
            return None; # no possible move left


def Paddington(player, game, oval = 1):
    # track start time for use in post-game move time analysis     
    
    
    Depth = 35
    if player.board.moves_played>13:
        Depth = 65
    elif player.board.moves_played>8:
        Depth = 45
        

    t0 = time.time()
    start_time = t0
    
    turn_number = 1

    

    game_copy = copy.deepcopy(game)
    state = BoardState(game_copy)
    # Test resetting one player
    # state.game.players[1]=0
    this_move = alphabeta_search(state, Depth,1, None, None, start_time, state.to_move.board.piece_count)
    
    # print(this_move.id,this_move.points)
   
    t1 = time.time()
    print('Paddington time taken s:',round((t1-t0),2))
    
    return this_move
    
    #time.sleep(100)

def PaddingtonBasic(player, game, oval = 1):
    # track start time for use in post-game move time analysis     
    
    
    Depth = 5
    if player.board.moves_played>13:
        Depth = 25
    elif player.board.moves_played>8:
        Depth = 15
        

    t0 = time.time()
    start_time = t0
    
    turn_number = 1

    game_copy = copy.deepcopy(game)
    state = BoardState(game_copy)
    this_move = alphabeta_search(state, Depth, 1, None, None, start_time, state.to_move.board.piece_count)
    
    # print(this_move.id,this_move.points)
   
    t1 = time.time()
    print('Paddington time taken s:',round((t1-t0),2))
    
    return this_move
    
    #time.sleep(100)


# AI implementation, taken from mancala.py
def alphabeta_search(state, d=1, utility_param = 0, cutoff_test=None, eval_fn=None, start_time=None, turn_number=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    global count
    global testing
    global BigInitialValue
    global MoveTimes
    
    testing = False

    print('Starting search',d)

    player = state.to_move
    flip = 1
    # if state.to_move.id == 1:
    #     flip = 1
    # else:
    #     flip = -1
    count = 0

    def max_value(state, alpha, beta, depth):
        global count, testing
        if testing:
            print("  "* depth, "Max  alpha: ", alpha, " beta: ", beta, " depth: ", depth)
        if cutoff_test(state, depth):
            if testing:
                print("  "* depth, "Max cutoff returning ", eval_fn(state))
            return eval_fn(state)
        v = -BigInitialValue
        
        if cutoff_test(state, depth+10) and state.game.move_type == 'play_piece':
            succ = state.game.successors(state,utility_param,0)
        else:
            succ = state.game.successors(state,utility_param,1)
        count = count + len(succ)
        if testing:
            print("  "*depth, "maxDepth: ", depth, "Total:", count, "Successors: ", len(succ))
        for (a, s) in succ:
            # Decide whether to call max_value or min_value, depending on whose move it is next.
            # A player can move repeatedly if opponent is completely blocked
            if state.to_move.id == s.to_move.id:
                if s.game.move_type in ('play_piece','add_piece_forced'):
                    v = max(v, max_value(s, alpha, beta, depth+10))
                else:
                    v = max(v, max_value(s, alpha, beta, depth+1))
            else:
                
                v = max(v, min_value(s, alpha, beta, depth+1))
                print('?')
            if testing:
                print("  "* depth, "max best value:", v)
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        # print('Computing min value')
        global count
        if testing:
            print("  "*depth, "Min  alpha: ", alpha, " beta: ", beta, " depth: ", depth)
        if cutoff_test(state, depth):
            if testing:
                print("  "*depth, "Min cutoff returning ", eval_fn(state))
            return eval_fn(state)
        v = BigInitialValue
        succ = state.game.successors(state)
        count = count + len(succ)
        if testing:
            print("  "*depth, "minDepth: ", depth, "Total:", count, "Successors: ", len(succ))
        for (a, s) in succ:
            # Decide whether to call max_value or min_value, depending on whose move it is next.
            # A player can move repeatedly if opponent is completely blocked
            if state.to_move.id == s.to_move.id:
                v = min(v, min_value(s, alpha, beta, depth+1))
            else:
                v = min(v, max_value(s, alpha, beta, depth+1))
            if testing:
                print("  "*depth, "min best value:", v)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def right_value(s, alpha, beta, depth):
        if s.to_move.id == state.to_move.id:
            return max_value(s, -BigInitialValue, BigInitialValue, 0)
        else:
            return min_value(s, -BigInitialValue, BigInitialValue, 0)

    def argmin(seq, fn):
        """Return an element with lowest fn(seq[i]) score; tie goes to first one.
        >>> argmin(['one', 'to', 'three'], len)
        'to'
        """
        # print(seq)        
        
        best = seq[0]; best_score = fn(best)
        # print(best,best_score)
        for x in seq:
            x_score = fn(x)
            if x_score < best_score:
                best, best_score = x, x_score
        return best

    def argmax(seq, fn):
        """Return an element with highest fn(seq[i]) score; tie goes to first one.
        >>> argmax(['one', 'to', 'three'], len)
        'three'
        """
        return argmin(seq, lambda x: -fn(x))

    # Body of alphabeta_search starts here:
        
    # Allow the function to pass parameters to the utility - could be used in move ranking as well.
        
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or state.game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: flip*state.game.utility(state, turn_number,utility_param))
    action, state = argmax(state.game.successors(state,utility_param),
                            lambda a_s: right_value(a_s[1], -BigInitialValue, BigInitialValue, 0))

    print('Total nodes evaluated:', count)

    # calculate move time, round to 2 decimal places, store for analysis
    MoveTimes.append(round(time.time() - start_time, 2))
    return action



def getMax(candidates,scores):  
    max_score = -1000000
    max_index = 0
    for a in range(len(candidates)):
         if scores[a]>max_score:
             max_index = a
             max_score = scores[a]
    return max_index,max_score

# Human Strategy: choose an available piece and placement based on user input
def Human_Player(player, game, oval = 1):
    
    if game.move_type in (['add_piece','add_piece_forced','add_grizzly']):
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        return piece_prompt(possibles,game.move_type);
        
    elif game.move_type == 'expand_board':  
        dummy = 0
        possibles = player.possible_moves(dummy, game);
        return piece_prompt(possibles,game.move_type);
        
    elif game.move_type == 'play_piece':
    
        initial_options = [p[0] for p in game.all_pieces if len(p)>0];    
    
        options = []
        
        for p in initial_options:
            possibles = player.possible_moves([p], game);
            if len(possibles) != 0:
                options.append(p)
   
        while len(options) > 0: # if there are still possible moves
            piece = piece_prompt(options,game.move_type);
            if piece=='Pass':
                return None
            possibles = player.possible_moves([piece], game);
            if len(possibles) != 0: # if there is possible moves
                return placement_prompt(possibles);
            else: # no possible move for that piece
                options.remove(piece); # remove it from the options
    return None; # no possible move left


# Human Strategy: choose an available piece and placement based on user input
def Human_Player_Fast(player, game, oval = 1):
    # turn_number = (TotalStartingPieces - len(player.pieces) + 1)
    if game.rounds<2:
        move = Greedy_Player(player,game,oval)
        return move

    else:

        move = Human_Player(player,game,oval)
        return move

# Board state is no longer used
class BoardState:
    """Holds one state of the Blokus board, used to generate successors."""
    def __init__(self, game=None):
        self.game = game
        # self.p1 = [p for p in game.players if p.id == 1][0]
        # self.p2 = [p for p in game.players if p.id == 2][0]
        
        self.p1 = game.players[0]
        self.p2 = game.players[1]
        
        # to_move keeps track of the player whose turn it is to move
        self.to_move = game.players[0]
        # self._board = game.board