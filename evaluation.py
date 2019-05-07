import chess
import config
import fenparser
import math
import sys 

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


def make_move(board):
    #tree = Node(2, 1, 0, board)
    print("Board score: {}".format(evaluate_board_score(board)))
    legal_move_list = [x for x in board.legal_moves]
    board.push(legal_move_list[0])
    return board

def calculate_score_for_piece(piece, lowercase, row, col):
    piece = piece.upper()
    pst_pos = (config.board_length * row) + col
    position_scores = config.pst[piece]
    pst_value = position_scores[pst_pos]

    if lowercase:
        piece_value = -config.piece[piece]
    else:
        piece_value = config.piece[piece]

    return pst_value + piece_value

def calculate_score_for_position(row, col, fen):
    piece = fen[row][col]

    if piece == "P":
        return calculate_score_for_piece(piece, False, row, col)
    elif piece == "N":
        return calculate_score_for_piece(piece, False, row, col)
    elif piece == "B":
        return calculate_score_for_piece(piece, False, row, col)
    elif piece == "R":
        return calculate_score_for_piece(piece, False, row, col)
    elif piece == "Q":
        return calculate_score_for_piece(piece, False, row, col)
    elif piece == "K":
        return calculate_score_for_piece(piece, False, row, col)
    elif piece == "p":
        return calculate_score_for_piece(piece, True, row, col)
    elif piece == "n":
        return calculate_score_for_piece(piece, True, row, col)
    elif piece == "b":
        return calculate_score_for_piece(piece, True, row, col)
    elif piece == "r":
        return calculate_score_for_piece(piece, True, row, col)
    elif piece == "q":
        return calculate_score_for_piece(piece, True, row, col)
    elif piece == "k":
        return calculate_score_for_piece(piece, True, row, col)
    else:
        return 0
    

def evaluate_board_score(board):
    #loop through the board and calculate the score
    fen = parse_fen(board)

    score = 0

    for row in range(len(fen)):
        for col in range(len(fen[row])):
            score += calculate_score_for_position(row, col, fen)

    return score


def parse_fen(board):
    return fenparser.FenParser(board.fen()).parse()

class Node(object):
    def __init__(self, depth, playernum, score, board):
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
                self.children.append(Node(self.depth-1, -self.playernum, -self.score, self.board))
                self.board.pop()

def min_max(depth, node, player):   
    if depth == 0 or len(node.children) == 0:
        return evaluate_board_score()

    max_score = sys.maxsize * -player

    for i in range(len(node)):
        child = node.children[i]
        score = min_max(depth-1, child, -player)
        if( player > 0 ):
            if score > max_score:
                max_score = score
        else:
            if score < max_score:
                max_score = score
    
    return max_score

def AI_make_move():
    pass

    #initial call minimax(depth, origin, True)
    
