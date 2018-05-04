""" Christians chess game



"""

__author__ = "Christian Brinch"
__copyright__ = "Copyright 2018"
__credits__ = ["Christian Brinch"]
__license__ = "AFL 3.0"
__version__ = "0.1"
__maintainer__ = "Christian Brinch"
__email__ = "brinch.c@gmail.dk"


#import random
import chess_engine as engine
import chess_ai as ai


def convert_position(string_position):
    ''' Convert the position given in chess notation to matrix indices
    '''
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return (8-int(string_position[1]), letters.index(string_position[0]))

def main():
    ''' Just a main wrapper
    '''
    game = engine.ChessGame()

    game.draw_board()

    done = False
    while not done:
        move = raw_input('Input move (example: a2-a3):').split('-')
        if 'exit' in move:
            break
        move = tuple([convert_position(move[0]), convert_position(move[1])])
        possible_moves = game.get_possible_moves(-1)
        #move = random.choice(possible_moves)
        if not possible_moves:
            if game.check:
                print "Player "+game.players[game.check+1]+" is check mate"
            else:
                print "Game is stale mate"
            break
        if game.check_move(-1, move, possible_moves):
            game.make_move(-1, move)
            possible_moves = game.get_possible_moves(1)
            if not possible_moves:
                if game.check:
                    print "Player "+game.players[game.check+1]+" is check mate"
                else:
                    print "Game is stale mate"
                break
            ai.make_evaluated_move(game, 1)
        #done = True
