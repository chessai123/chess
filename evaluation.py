import chess

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

class AI():
    def __init__(self):
        self.depth = 2

    def make_move(self, board):
        legal_move_list = [x for x in board.legal_moves]
        board.push(legal_move_list[0])
        print(legal_move_list[0])
        return board

    def get_row_and_col(self, string):  
        col1 = 0
        for i in letters:
            if i == string[0]:
                break
            col1 += 1

        row1 = int(string[1])

        col2 = 0
        for i in letters:
            if i == string[2]:
                break
            col2 += 1

        row2 = int(string[3])

        return [col1, row1, col2, row2]

    def evalute(self):
        pass

        


    
