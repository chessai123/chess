import chess
import chess.variant

def move_brick(board, move):

    Nf3 = chess.Move.from_uci(move)
    if Nf3 not in board.legal_moves:
        print("not a move")
    board.push(Nf3)
    

def parse_arg(board):
    print(board)
    while True:
        choice = input("> ")
        if chess.Move.from_uci(choice) not in board.legal_moves:
            print("not a legal move") 
        else:
            return choice

def run(board):
    while True:
        move = parse_arg(board)
        move_brick(board, move)


if __name__ == "__main__":
    board = chess.variant.GiveawayBoard()
    run(board)
    
    