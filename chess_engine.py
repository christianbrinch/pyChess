# -*- coding: utf-8 -*-
""" Christians chess engine



"""

__author__ = "Christian Brinch"
__copyright__ = "Copyright 2018"
__credits__ = ["Christian Brinch"]
__license__ = "AFL 3.0"
__version__ = "0.1"
__maintainer__ = "Christian Brinch"
__email__ = "brinch.c@gmail.dk"


import numpy as np
import chess_rules as rules


def draw_piece(value, highlight=False):
    ''' return a string with the appropriate color and piece name
        If highlight is true, the square will be drawn with a yellow
        background.
    '''
    types = {0: " ", 1: "♟", 2: "♜", 3: "♞", 4: "♝", 6: "♚", 5: "♛"}

    if highlight:
        colors = ['\033[95;43m', '\033[0m', '\033[91;43m']
    else:
        colors = ['\033[95m', '\033[0m', '\033[91m']
    if value == 0:
        return colors[0]+types[np.abs(value)]+colors[1]

    return colors[np.sign(value)+1]+types[np.abs(value)]+colors[1]


def convert_position(string_position):
    ''' Convert the position given in chess notation to matrix indices
    '''
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return (8-int(string_position[1]), letters.index(string_position[0]))


def convert_indices(integer_position):
    ''' Convert the position given in matrix indices to chess notation
    '''
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return letters[integer_position[1]]+str(7-integer_position[0]+1)


def initialize_board():
    ''' Add 32 pieces at their initial positions
    '''
    pieces = []
    for color in [-1, 1]:
        row = int(-3.5*color+3.5)
        for i in [0, 7]:
            pieces.append(rules.OneRook(color, (row, i)))
        for i in [1, 6]:
            pieces.append(rules.OneKnight(color, (row, i)))
        for i in [2, 5]:
            pieces.append(rules.OneBischop(color, (row, i)))
        pieces.append(rules.OneQueen(color, (row, 3)))
        pieces.append(rules.OneKing(color, (row, 4)))
        row = int(-2.5*color+3.5)
        for i in range(8):
            pieces.append(rules.OnePawn(color, (row, i)))

    return pieces

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


class ChessGame(object):
    ''' A class that contains a game of chess
    '''

    def __init__(self):
        self.current_player = -1
        self.players = ['WHITE', 'none', 'BLACK']
        self.check = 0
        self.dead_pieces = []
        self.pieces = initialize_board()
        self.state = self.board_state()



    def board_state(self):
        ''' Construct the board and the pieces positions
        '''
        state = np.zeros([8, 8], dtype=int)
        for piece in self.pieces:
            if piece.status:
                state[piece.current_position] = piece.type*piece.color
        return state

    def draw_board(self, highlights=(-1, -1)):
        ''' Draw the chess board in its current state
        '''
        print '\n  +---+---+---+---+---+---+---+---+'
        for j in range(8):
            print 8-j,
            for i in range(8):
                print '| '+draw_piece(self.state[j][i], (j, i) in highlights),
            print '|\n  +---+---+---+---+---+---+---+---+'
        print '    a   b   c   d   e   f   g   h'
        print ''
        print self.players[self.current_player+1]+' turn to move'

    def show_taken_pieces(self):
        ''' Print out the pices that have been taken so far
        '''
        for i in [0, 2]:
            j = i-1
            dead_pieces = [piece for piece in self.dead_pieces if piece*j > 0]
            if dead_pieces:
                print self.players[i]+' has lost the following pieces: ',
                for piece in dead_pieces:
                    print draw_piece(piece),
                print ''

    def draw_valid_moves(self, string_position):
        ''' Draw the board including valid positions for a given piece
        '''
        position = convert_position(string_position)
        piece = [
            piece for piece in self.pieces if piece.current_position == position][0]

        moves = piece.moves(self.state)
        valid_moves = []
        for move in moves:
            valid_moves.append(move)

        self.draw_board(valid_moves)

    def get_all_moves(self, player):
        ''' A method to get a list of all moves for a player
        '''
        moves = []
        pieces = [piece for piece in self.pieces if piece.color ==
                  player and piece.status]
        for piece in pieces:
            for move in piece.moves(self.state):
                moves.append(tuple([piece.current_position, move]))

        return moves

    def get_possible_moves(self, player):
        ''' A method to get a list of all moves that are valid and does not
            cause player to be check
        '''
        moves = self.get_all_moves(player)
        move_stack = Stack()
        for move in moves:
            dead_piece_idx = self.make_move(player, move, for_real=False)
            move_stack.push({'move':move, 'kill':dead_piece_idx})
            if self.is_check(player):
                moves = [
                    entry for entry in moves if entry != move]
            self.undo_move(move_stack.pop())
        return moves

    def is_check(self, player):
        ''' Check if a player is check
        '''
        king_idx = next((idx for idx, piece in enumerate(
            self.pieces) if piece.type == 6 and piece.color == player), False)
        opponent_moves = self.get_all_moves(player*-1)
        if self.pieces[king_idx].current_position in [move[1] for move in opponent_moves]:
            return True

        return False

    def check_move(self, player, move, possible_moves):
        ''' Check if a user move is possible
        '''
        if move in possible_moves:
            return True
        else:
            idx = next((idx for idx, piece in enumerate(self.pieces)
                        if piece.current_position == move[0] and piece.status), False)
            if idx is False:
                print "No piece in position "+convert_indices(move[0])
                return False
            elif self.pieces[idx].color*player < 0:
                print "Piece in position " + \
                    convert_indices(move[0])+" belongs to other player"
                return False

            print "Invalid move"
            return False

    def make_move(self, player, move, for_real=True):
        ''' Perform a move
        '''
        piece_idx = next((idx for idx, piece in enumerate(self.pieces)
                          if piece.current_position == move[0] and piece.status), False)

        dead_piece_idx = next((idx for idx, piece in enumerate(self.pieces)
                               if piece.current_position == move[1] and piece.status), False)

        if dead_piece_idx:
            self.pieces[dead_piece_idx].status = 0
            if for_real:
                self.dead_pieces.append(
                    self.pieces[dead_piece_idx].color*self.pieces[dead_piece_idx].type)

        self.pieces[piece_idx].current_position = move[1]
        self.state = self.board_state()


        if self.is_check(player*-1):
            if for_real:
                print self.players[player*-1+1]+" is check!"
            self.check = player*-1

        if for_real:
            self.current_player = player*-1
            self.show_taken_pieces()
            self.draw_board()

        return dead_piece_idx

    def undo_move(self, node):
        ''' A method to undo a move
        '''
        piece_idx = next((idx for idx, piece in enumerate(self.pieces)
                          if piece.current_position == node['move'][1] and piece.status), False)
        self.pieces[piece_idx].current_position = node['move'][0]
        if node['kill'] is not False:
            self.pieces[node['kill']].status = 1
