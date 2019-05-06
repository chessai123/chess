import chess
import config
import fenparser
import math
import sys 

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


def make_move(self, board):
    legal_move_list = [x for x in board.legal_moves]
    self.calculate_pos(legal_move_list[0],board, 0)
    board.push(legal_move_list[0])
    print(legal_move_list[0])
    return board

#the fen string is inverted, so needs to take the length of the board and [x for x in board.legal_moves]
#subtrakt with the row number to get the right pos in the fen
def get_row_and_col(self, string):   
    col1 = 0
    for i in letters:
        if i == string[0]:
            break
        col1 += 1

    row1 = 8-int(string[1]) 

    col2 = 0
    for i in letters:
        if i == string[2]:
            break
        col2 += 1

    row2 = 8-int(string[3])

    return [col1, row1, col2, row2]
    
    def evalute(self, board):
        pass

def evaluate_pos_score(self, move, board, player):
    fen = parse_fen(board)
    moves = self.get_row_and_col(str(move))
    
    from_col    = moves[0]
    from_row    = moves[1]
    to_col      = moves[2]
    to_row      = moves[3]

    #get the value for the given piece
    piece = fen[from_row][from_col].capitalize()
    piece_value = config.piece[piece]
        
    #get score for the position
    pst_pos = (config.board_length * to_row) + to_col
    position_score = config.pst[piece]
    pst_value = position_score[pst_pos]
    
    to_pos = fen[to_row][to_col]
    
    if to_pos != " ":
        to_pos_score = config.piece[to_pos]
        return to_pos_score + pst_value
    else:
        return pst_value


def parse_fen(board):
    return fenparser.FenParser(board.fen()).parse()

class Node(object):
    def __init__(self, depth, playernum, score, board, move):
        self.depth = depth
        self.playernum = playernum
        self.score = score
        self.board = board
        self.children = []
        self.generate_children()

    def generate_children(self):
        legal_moves = [x for x in self.board.legal_moves]
        if self.depth >= 0:
            for x in legal_moves:
                self.board.push(x)
                self.children.append(Node(self.depth-1, -self.playernum, -self.score, self.board, x))
                self.board.pop(x)


def min_max(depth, node, player):   
    if depth == 0 or len(node.children) == 0:
        return evaluate_pos_score()

    max_score = sys.maxsize * -player

    for i in range(len(node)):
        child = node.children[i]
        score = min_max(depth-1, child, -player)
        if( player > 0 ):
            if score > max_score:
                max_score = score
            else:
                max_score = score
    
    return max_score



    #initial call minimax(depth, origin, True)
    
