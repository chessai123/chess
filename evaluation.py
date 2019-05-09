import chess
import config
import fenparser
import math
import sys

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


def make_move(board):
    tree = Node(2, 1, 0, board)
    move = min_max(2, tree, 1)
    print(move)
    # legal_move_list = [x for x in board.legal_moves]
    board.push(move[1])
    return board


def calculate_score_for_piece(piece, lowercase, row, col):
    piece = piece.upper()
    pst_pos = (config.board_length * row) + col
    position_scores = config.pst[piece]
    position_scores = position_scores[::-1]

    if lowercase:
        piece_value = config.piece[piece]
        pst_value = position_scores[pst_pos]
    else:
        piece_value = -config.piece[piece]
        pst_value = -position_scores[pst_pos]
    print("piece value: {} position value: {}, sum: {}".format(piece_value, pst_value, piece_value+pst_value))
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
    # loop through the board and calculate the score
    fen = parse_fen(board)
    score = 0
    for row in range(len(fen)):
        for col in range(len(fen[row])):
            score += calculate_score_for_position(row, col, fen)
            #print("this is the score: {}, row and col: {}{} this is the fen string: \n{}".format(score, row, col, fen))
    return score

def parse_fen(board):
    return fenparser.FenParser(board.fen()).parse()


class Node(object):
    def __init__(self, depth, playernum, move, board):
        self.depth = depth
        self.playernum = playernum
        self.board = board
        self.move = move
        self.children = []
        self.generate_children()

    def generate_children(self):
        legal_moves = [x for x in self.board.legal_moves]
        if self.depth >= 0:
            for x in legal_moves:
                self.board.push(x)
                self.children.append(Node(self.depth-1, -self.playernum, x, self.board))
                self.board.pop()


def min_max(depth, node, player):
    if player > 0:
        max_score = [-sys.maxsize, None]
    else:
        max_score = [sys.maxsize, None]

    if depth == 0:
        score = evaluate_board_score(node.board)
        return [score, node.move]

    for child in node.children:
        evaluation = min_max(depth-1, child, -player)
        print(evaluation, max_score)
        if (player > 0):
            if(evaluation[0] > max_score[0]):
                if(node.move != 0):
                    max_score = [evaluation[0], node.move]
                else:
                    max_score = [evaluation[0], evaluation[1]]
        else:
            if(evaluation[0] < max_score[0]):
                if(node.move != 0):
                    max_score = [evaluation[0], node.move]
                else:
                    max_score = [evaluation[0], evaluation[1]]
    return max_score

def AI_make_move():
    pass

    # initial call minimax(depth, origin, True)
    
