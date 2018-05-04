""" Christians chess ai



"""

__author__ = "Christian Brinch"
__copyright__ = "Copyright 2018"
__credits__ = ["Christian Brinch"]
__license__ = "AFL 3.0"
__version__ = "0.1"
__maintainer__ = "Christian Brinch"
__email__ = "brinch.c@gmail.dk"

import random
import time


class Stack(object):
    ''' A standard stack with push and pop methods
    '''

    def __init__(self):
        self.moves = []

    def is_empty(self):
        ''' Check if stack is empty
        '''
        return len(self.moves) == 0

    def push(self, move):
        ''' Push item onto stack
        '''
        self.moves.append(move)

    def pop(self):
        ''' Pop item from stack
        '''
        return self.moves.pop()


def get_board_value(game):
    ''' Evaluate the board and return numeric value
    '''
    value = 0
    for piece in game.pieces:
        if piece.status == 1:
            value += piece.value()
    return value


def make_evaluated_move(game, player):
    ''' Make a clever move
    '''
    t_0 = time.time()
    i, best_value, best_moves = alpha_beta(
        game, player, 4, -9999, 9999, 0, Stack())
    #i, best_value, best_moves = min_max(game, player, 3,0)
    game.make_move(player, random.choice(best_moves))
    t_1 = time.time()
    print "runtime for ", i, " moves is ", t_1 - \
        t_0, "  Best move value is", best_value


def make_random_move(game, player):
    ''' Make a random move
    '''
    moves = game.get_possible_moves(player)
    game.make_move(random.choice(moves))


def alpha_beta(game, player, depth, alpha, beta, i, move_stack):
    ''' minmax with alpha-beta pruning
    '''
    i = i+1
    if depth == 0:
        return i, get_board_value(game), []

    best_moves = []
    moves = game.get_possible_moves(player)
    current_value = player * -9999
    for move in moves:
        dead_piece_idx = game.make_move(player, move, for_real=False)
        move_stack.push({'move': move, 'kill': dead_piece_idx})
        i, value, dummy = alpha_beta(
            game, player*-1, depth - 1, alpha, beta, i, move_stack)
        game.undo_move(move_stack.pop())
        if (player == 1 and value > current_value) or (player == -1 and value < current_value):
            current_value = value
            best_moves = [move]
        elif value == current_value:
            best_moves.append(move)
        if player == 1:
            alpha = max(alpha, current_value)
        else:
            beta = min(beta, current_value)
        if beta <= alpha:
            break
    return i, current_value, best_moves


def min_max(game, player, depth, i, move_stack):
    ''' simple minmax
    '''
    i = i+1
    if depth == 0:
        return i, get_board_value(game), []

    best_moves = []
    moves = game.get_possible_moves(player)
    current_value = -9999 * player
    for move in moves:
        dead_piece_idx = game.make_move(player, move, for_real=False)
        move_stack.push({'move': move, 'kill': dead_piece_idx})
        i, value, dummy = min_max(game, player*-1, depth - 1, i, move_stack)
        game.undo_move(move_stack.pop())
        if (player == 1 and value > current_value) or (player == -1 and value < current_value):
            current_value = value
            best_moves = [move]
        elif value == current_value:
            best_moves.append(move)

    return i, current_value, best_moves
