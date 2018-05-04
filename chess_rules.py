# -*- coding: utf-8 -*-
""" Christians chess rules



"""

from operator import add


class OnePiece(object):
    ''' A class that contains all information about a single piece
    '''

    def __init__(self, piece, color, position):
        self.type = piece
        self.color = color
        self.status = 1
        self.current_position = position
        self.piece_value = None

    def value_matrix(self, idx):
        ''' Dummy method to be overridden
        '''
        pass

    def value(self):
        ''' Return the value of the piece
        '''
        idx = self.current_position
        if self.color < 0:
            idx = (idx[0], 7-idx[1])

        return self.piece_value * self.color + self.value_matrix(idx)


class OnePawn(OnePiece):
    ''' A class to describe a pawn
    '''

    def __init__(self, color, position):
        OnePiece.__init__(self, 1, color, position)
        self.piece_value = 10.

    def value_matrix(self, idx):
        ''' Return the value of the position
        '''
        matrix = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                  [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                  [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                  [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                  [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                  [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                  [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                  [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]]

        return matrix[idx[0]][idx[1]]

    def moves(self, state):
        ''' A method to calculate all moves for a pawn
        '''
        valid_moves = []
        # Let the pawn move one step ahead
        move = tuple(map(add, self.current_position, (self.color*1, 0)))
        if all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move] == 0:
            valid_moves.append(move)
            # Check if pawn is in start position and if so, let it move 2 steps
            if self.current_position[0] == 1 or self.current_position[0] == 6:
                move = tuple(map(add, self.current_position, (self.color*2, 0)))
                if all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move] == 0:
                    valid_moves.append(move)
        # Let the pawn move to the diagonal if there is an opponent piece
        for side in [-1, 1]:
            move = tuple(map(add, self.current_position, (self.color*1, side)))
            if all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move]*self.color < 0:
                valid_moves.append(move)
        return valid_moves


class OneRook(OnePiece):
    ''' A class to describe a rook
    '''

    def __init__(self, color, position):
        OnePiece.__init__(self, 2, color, position)
        self.piece_value = 50.

    def value_matrix(self, idx):
        ''' Return the value of the position
        '''

        matrix = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                  [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                  [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                  [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                  [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                  [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                  [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                  [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]]

        return matrix[idx[0]][idx[1]]

    def moves(self, state):
        ''' A method to calculate all moves for a rook
        '''
        valid_moves = []
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, 8):
                move = tuple(
                    map(add, self.current_position, (i*direction[0], i*direction[1])))
                if all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move] == 0:
                    valid_moves.append(move)
                elif all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move]*self.color < 0:
                    valid_moves.append(move)
                    break
                else:
                    break
        return valid_moves


class OneKnight(OnePiece):
    ''' A class to describe a knight
    '''

    def __init__(self, color, position):
        OnePiece.__init__(self, 3, color, position)
        self.piece_value = 30

    def value_matrix(self, idx):
        ''' Return the value of the position
        '''
        matrix = [[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                  [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                  [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                  [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                  [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                  [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                  [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
                  [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]

        return matrix[idx[0]][idx[1]]

    def moves(self, state):
        ''' A method to calculate all moves for a knight
        '''
        valid_moves = []
        for destination in [(2, -1), (2, 1), (-2, -1), (-2, 1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            move = tuple(map(add, self.current_position, destination))
            if all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move]*self.color <= 0:
                valid_moves.append(move)
        return valid_moves


class OneBischop(OnePiece):
    ''' A class to describe a bischop
    '''

    def __init__(self, color, position):
        OnePiece.__init__(self, 4, color, position)
        self.piece_value = 30.

    def value_matrix(self, idx):
        ''' Return the value of the position
        '''
        matrix = [[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                  [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                  [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                  [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                  [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                  [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                  [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                  [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]

        return matrix[idx[0]][idx[1]]

    def moves(self, state):
        ''' A method to calculate all moves for a bischop
        '''
        valid_moves = []
        for direction in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            for i in range(1, 8):
                move = tuple(
                    map(add, self.current_position, (i*direction[0], i*direction[1])))
                if all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move] == 0:
                    valid_moves.append(move)
                elif all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move]*self.color < 0:
                    valid_moves.append(move)
                    break
                else:
                    break
        return valid_moves


class OneQueen(OnePiece):
    ''' A class to describe a queen
    '''

    def __init__(self, color, position):
        OnePiece.__init__(self, 5, color, position)
        self.piece_value = 90.

    def value_matrix(self, idx):
        ''' Return the value of the position
        '''
        matrix = [[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                  [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                  [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                  [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                  [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                  [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                  [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
                  [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]

        return matrix[idx[0]][idx[1]]

    def moves(self, state):
        ''' A method to calculate all moves for a queen
        '''
        valid_moves = []
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, 8):
                move = tuple(
                    map(add, self.current_position, (i*direction[0], i*direction[1])))
                if all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move] == 0:
                    valid_moves.append(move)
                elif all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move]*self.color < 0:
                    valid_moves.append(move)
                    break
                else:
                    break
        for direction in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            for i in range(1, 8):
                move = tuple(
                    map(add, self.current_position, (i*direction[0], i*direction[1])))
                if all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move] == 0:
                    valid_moves.append(move)
                elif all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move]*self.color < 0:
                    valid_moves.append(move)
                    break
                else:
                    break

        return valid_moves


class OneKing(OnePiece):
    ''' A class to describe a king
    '''

    def __init__(self, color, position):
        OnePiece.__init__(self, 6, color, position)
        self.piece_value = 900.

    def value_matrix(self, idx):
        ''' Return the value of the position
        '''
        matrix = [[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                  [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                  [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                  [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                  [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                  [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                  [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                  [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]]

        return matrix[idx[0]][idx[1]]

    def moves(self, state):
        ''' A method to calculate all moves for a king
        '''
        valid_moves = []
        for destination in [(1, -1), (1, 0), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]:
            move = tuple(map(add, self.current_position, destination))
            if all([0 <= move[i] <= 7 for i in [0, 1]]) and state[move]*self.color <= 0:
                valid_moves.append(move)

        return valid_moves
