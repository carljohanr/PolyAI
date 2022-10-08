#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 22:24:48 2022

@author: carljohan
"""

From possible_moves_pruned

            # if game.move_type == 'play_piece':
                # print (candidate_moves[0].points)
                # time.sleep(2)
            # time.sleep(100)
        
        # if game.move_type == 'add_piece':
        #     if max(candidate_moves)<=3:
        #         if candidate_moves == [2,3]:
        #             #print('Common')
        #             piece_counts = game.players[0].piece_counts
        #             if piece_counts[3] > piece_counts[2]:
        #                 candidate_moves = [2]
        #             else:
        #                 candidate_moves = [3]
        #         #print(candidate_moves,game.players[0].piece_counts)
        #     elif 4<=max(candidate_moves)<=7:
        #         if game.players[0].board.addon_value>=2:
        #             # print(candidate_moves)
        #             rank_list=[game.all_pieces[i][0].score for i in candidate_moves]
        #             candidate_moves = self.getAllMax(candidate_moves,rank_list)
        #             # print(candidate_moves)
        #     else:
        #         # print('Candidates',candidate_moves)
        #         rank_list = [8,9,10,19,11,14,17,12,16,15,13,18]
        #         new_candidates = []
        #         for i in range(len(rank_list)):
        #             if rank_list[i] in candidate_moves and len(new_candidates)<4:
        #                 new_candidates.append(rank_list[i])
        #             elif len(new_candidates)>=4:
        #                 break
        #         # print('New candidates',new_candidates)
        #         candidate_moves = new_candidates