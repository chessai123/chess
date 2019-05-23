import chess
import config
import fenparser
import math
import sys

TREE_DEPTH = 2
PLAYER_NUM = 1

def make_move(board):
    tree = Node(TREE_DEPTH, PLAYER_NUM, 0, board)
    move = min_max(TREE_DEPTH, tree, PLAYER_NUM, -sys.maxsize, sys.maxsize)
    board.push(move[1])
    return board

""" Calculate the score for a piece depending on the color and position """
def calculate_score_for_piece(piece, lowercase, row, col):
    piece = piece.upper()
    pst_pos = (config.board_length * row) + col
    position_scores = config.pst[piece]
    #reverse the position scores for a right representation for the board
    position_scores = position_scores[::-1]

    if lowercase:
        piece_value = config.piece[piece]
        pst_value = position_scores[pst_pos]
    else:
        piece_value = -config.piece[piece]
        pst_value = -position_scores[pst_pos]
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

""" Calculate the score of the board by parsing the board state """
def evaluate_board_score(board):
    fen = parse_fen(board)
    score = 0
    for row in range(len(fen)):
        for col in range(len(fen[row])):
            score += calculate_score_for_position(row, col, fen)
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

    #create the tree
    def generate_children(self):
        legal_moves = [x for x in self.board.legal_moves]
        if self.depth >= 0:
            for x in legal_moves:
                self.board.push(x)
                self.children.append(Node(self.depth-1, -self.playernum, x, self.board))
                self.board.pop()

""" Recursively calculate max possible score for positions throughout the branches in the decision tree. 
    Using Alpha-Beta pruning to reduce branch calculations.
    The alpha parameter holds the best value that the maximizer can guarantee at the level or above.
    the beta parameter holds the best value that the minimizer can guarantee at the level or above.
    Needs to push before evaluating and pop after so the board always holds the right state. """
def min_max(depth, node, player, alpha, beta):
    if player > 0:
        max_score = [alpha, None]
    else:
        max_score = [beta, None]

    if depth == 0:
        node.board.push(node.move)
        score = evaluate_board_score(node.board)
        node.board.pop()
        return [score, node.move]

    #Maximizer
    if player > 0:
        for child in node.children:
            child.board.push(child.move)
            evaluation = min_max(depth-1, child, -player, alpha, beta)
            child.board.pop()

            if(evaluation[0] > max_score[0]):
                #if there is no move, we are at the top of the tree
                #and needs to return the best move
                if(node.move != 0):
                    max_score = [evaluation[0], node.move]
                else:
                    max_score = [evaluation[0], evaluation[1]]

            alpha = max(max_score[0], alpha)

            #pruning
            if beta <= alpha:
                break
    #minimizer
    else: 
        for child in node.children:
            child.board.push(child.move)
            evaluation = min_max(depth-1, child, -player, alpha, beta)
            child.board.pop()

            if(evaluation[0] < max_score[0]):
                if(node.move != 0):
                    max_score = [evaluation[0], node.move]
                else:
                    max_score = [evaluation[0], evaluation[1]]
            
            beta = min(max_score[0], beta)
            
            #pruning
            if beta <= alpha:
                break
    return max_score
