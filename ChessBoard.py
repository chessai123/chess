import pygame
import sys
import chess
import math
import fenparser

screenW=400
screenH=400
clock = pygame.time.Clock()

black = (0,0,0)
board_size = 64
board_length = math.sqrt(board_size)
column_letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
square_size = int(screenH / 8)

brown_square_img    = "images/brown_square.png"
white_square_img    = "images/white_square.png"
cyanid_square_img   = "images/cyan_square.png"

black_pawn_img      = "images/Chess_tile_pd.png"
white_pawn_img      = "images/Chess_tile_pl.png"
black_bishop_img    = "images/Chess_tile_bd.png"
white_bishop_img    = "images/Chess_tile_bl.png"
black_king_img      = "images/Chess_tile_kd.png"
white_king_img      = "images/Chess_tile_kl.png"
black_horse_img     = "images/Chess_tile_nd.png"
white_horse_img     = "images/Chess_tile_nl.png"
black_queen_img     = "images/Chess_tile_qd.png"
white_queen_img     = "images/Chess_tile_ql.png"
black_tower_img     = "images/Chess_tile_rd.png"
white_tower_imp     = "images/Chess_tile_rl.png"

class chessb:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((screenW,screenH))
        pygame.display.set_caption('AlfaGeir')
        self.LoadImages()
        self.board = chess.Board()
        self.from_position = None
        self.to_position = None

    def LoadImages(self):
        self.white_block = pygame.image.load(white_square_img)
        self.brown_block = pygame.image.load(brown_square_img)
        self.highlight_block = pygame.image.load(cyanid_square_img)
        self.highlight_block = pygame.transform.scale(self.highlight_block, (square_size,square_size))

        self.black_pawn = pygame.image.load(black_pawn_img)
        self.black_pawn = pygame.transform.scale(self.black_pawn, (square_size,square_size))
        self.white_pawn = pygame.image.load(white_pawn_img)
        self.white_pawn = pygame.transform.scale(self.white_pawn, (square_size,square_size))     
        self.black_bishop = pygame.image.load(black_bishop_img)
        self.black_bishop = pygame.transform.scale(self.black_bishop, (square_size,square_size))
        self.white_bishop = pygame.image.load(white_bishop_img)
        self.white_bishop = pygame.transform.scale(self.white_bishop, (square_size,square_size)) 
        self.black_king = pygame.image.load(black_king_img)
        self.black_king = pygame.transform.scale(self.black_king, (square_size,square_size))
        self.white_king = pygame.image.load(white_king_img)
        self.white_king = pygame.transform.scale(self.white_king, (square_size,square_size)) 
        self.black_horse = pygame.image.load(black_horse_img)
        self.black_horse = pygame.transform.scale(self.black_horse, (square_size,square_size))
        self.white_horse = pygame.image.load(white_horse_img)
        self.white_horse = pygame.transform.scale(self.white_horse, (square_size,square_size)) 
        self.black_queen = pygame.image.load(black_queen_img)
        self.black_queen = pygame.transform.scale(self.black_queen, (square_size,square_size))
        self.white_queen = pygame.image.load(white_queen_img)
        self.white_queen = pygame.transform.scale(self.white_queen, (square_size,square_size)) 
        self.black_tower = pygame.image.load(black_tower_img)
        self.black_tower = pygame.transform.scale(self.black_tower, (square_size,square_size))
        self.white_tower = pygame.image.load(white_tower_imp)
        self.white_tower = pygame.transform.scale(self.white_tower, (square_size,square_size)) 

    def convert_to_chess_square(self, x, y):
        row = 7 - int(math.floor(y/square_size)) 
        col = int(math.floor(x/square_size) + 1)
        print(row, col)
        return int(((row*board_length) + col)-1)
    
    def convert_to_screen_coordinates(self, row, column):
        x = row * (screenH/board_length)
        y = column * (screenW/board_length)
        return (x, y)

    def draw_board_squares(self):
        self.screen.fill(black)
        for i in range(board_size):
            col = math.floor(i / board_length)
            row = (i % board_length)
            (x, y) = self.convert_to_screen_coordinates(row, col)   
            if ((x+y)/square_size)%2 == 0: 
                self.screen.blit(self.brown_block, (x, y))
            else:
                self.screen.blit(self.white_block, (x, y))
        
    def draw_pieces(self, fen):
        for i in range(board_size):
            col = int(math.floor(i / board_length))
            row = int(i % board_length)
            (x, y) = self.convert_to_screen_coordinates(row, col)
            if fen[col][row] == "p":
                self.screen.blit(self.black_pawn, (x,y))
            if fen[col][row] == "P":
                self.screen.blit(self.white_pawn, (x,y))
            if fen[col][row] == "q":
                self.screen.blit(self.black_queen, (x,y))
            if fen[col][row] == "Q":
                self.screen.blit(self.white_queen, (x,y))
            if fen[col][row] == "k":
                self.screen.blit(self.black_king, (x,y))
            if fen[col][row] == "K":
                self.screen.blit(self.white_king, (x,y))
            if fen[col][row] == "r":
                self.screen.blit(self.black_tower, (x,y))
            if fen[col][row] == "R":
                self.screen.blit(self.white_tower, (x,y))
            if fen[col][row] == "n":
                self.screen.blit(self.black_horse, (x,y))
            if fen[col][row] == "N":
                self.screen.blit(self.white_horse, (x,y))
            if fen[col][row] == "b":
                self.screen.blit(self.black_bishop, (x,y))
            if fen[col][row] == "B":
                self.screen.blit(self.white_bishop, (x,y))

    def draw(self):
        self.draw_board_squares()
        fen = self.parse_fen()
        self.draw_pieces(fen)
        pygame.display.update()

<<<<<<< HEAD
    def parse_fen(self):
        return fenparser.FenParser(self.board.fen()).parse()

    def check_if_legal(self):
        Nf3 = chess.Move(from_square=self.from_position, to_square=self.to_position)
        print(Nf3)
=======
    def convert_to_board_pos(self, x, y):
        row = board_size - math.floor(y/square_size) 
        column = math.floor(x/square_size)
        column = column_letter[column]
        pos = column + str(row)
        return pos

    def convert_to_chess_board_pos(self, x, y):
        col = 0
        for i in column_letter:
            if i == x:
                break
            col += 1
        row = board_size - int(y)
        return (col, row)

    def convert_to_chess_squares(self, x, y):
        counter = 0
        for i in range(board_size):
            for j in range(board_size):
                if (i, j) == (y, x):
                    #print("counter:")
                    print("counter" ,counter, ((x+1)*(y+1))-1)
                    return counter
                counter += 1
        return counter        

    def is_pawn_promotion(self, move):
        print(move)
        first_pos = move[:2]
        second_pos = move[2:]
        fen = self.parse_fen()

        first = self.convert_to_chess_board_pos(first_pos[0], first_pos[1]) 
        first_col = first[0]
        first_row = first[1]

        second = self.convert_to_chess_board_pos(second_pos[0], second_pos[1])
        second_col = second[0]
        second_row = second[1]

        # check for white pawn
        if fen[first_row][first_col] == "P" and second_row == 0:
            from_pos = self.convert_to_chess_squares(first_row, first_col)
            to_pos = self.convert_to_chess_squares(second_row, second_col)
            print(first_pos, first_col, first_row)
            print("\n")
            print("hello", from_pos, to_pos)
            Nf3 = chess.Move(from_square=from_pos, to_square=to_pos, promotion=chess.QUEEN)
            self.board.push(Nf3) 
            self.draw()

        # check for black pawn
        if fen[first_row][first_col] == "p" and second_row == 7:
            from_pos = self.convert_to_chess_squares(first_col, first_row)
            to_pos = self.convert_to_chess_squares(second_col, second_row)
            Nf3 = chess.Move(from_square=from_pos, to_square=to_pos, promotion=chess.QUEEN)
            self.board.push(Nf3) 
            self.draw()

        """
        fen = self.parse_fen()
        pos = move[0]
        first_col = 0
        for i in column_letter:
            if i == pos:
                break
            first_col += 1
        first_row = int(move[1]) -1

        pos = move[2]
        to_col = 0
        for i in column_letter:
            if i == pos:
                break
            to_col += 1
        to_row = int(move[3]) -1

        print(move)

        if fen[first_row][first_col] == "P" and move[3] == "8":
            board_pos_from = self.convert_to_chess(first_col, first_row)
            board_pos_to = self.convert_to_chess(to_col, to_row)
            Nf3 = chess.Move(to_square=board_pos_from, from_square=board_pos_to, promotion=chess.QUEEN)
            print(Nf3)
            self.board.push(Nf3)
            self.draw()
        elif fen[first_row][first_col] and move[3] == "1":
            board_pos_from = self.convert_to_chess(first_col, first_row)
            board_pos_to = self.convert_to_chess(to_col, to_row)
            Nf3 = chess.Move(from_square=board_pos_from, to_square=board_pos_to, promotion=chess.QUEEN)
            self.board.push(Nf3)
            self.draw()
            """
            

    def is_legal_move(self, move):
        Nf3 = chess.Move.from_uci(move)
        self.is_pawn_promotion(move)
>>>>>>> bd91cde6704ecd71585df832b0361520e584e1b2
        if Nf3 in self.board.legal_moves:
            print("legal")
            self.board.push(Nf3) 
        else:
            print("not a legal")
            return False
<<<<<<< HEAD

    def move_piece(self, square):
        if self.to_position == None and self.from_position != None:
            self.to_position = square
            #do the move
            self.check_if_legal()
            print("to position: {0} from position: {1}".format(self.to_position, self.from_position))
            self.from_position = None
            self.to_position = None
            return
        if self.from_position == None:
            self.from_position = square
            return

    def run_game(self):
=======
            
    def game_loop(self):
>>>>>>> bd91cde6704ecd71585df832b0361520e584e1b2
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.draw()
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:          
                        pos = pygame.mouse.get_pos()
                        square = self.convert_to_chess_square(pos[0], pos[1])
                        print(square)
<<<<<<< HEAD
                        self.move_piece(square)
                        self.draw()
=======
                        if self.to_position == None:
                            pass

                        # checks from and to pos & checks for legality of said pos/move
                        if self.from_position != None and self.to_position == None:
                        
                            board_pos = self.convert_to_board_pos(pos[0], pos[1])
                            self.to_position = board_pos
                            move = self.from_position + self.to_position
                            status = self.is_legal_move(move)
                            if status == False:
                                print("not a legal move")

                            if self.from_position == None:
                                pass
>>>>>>> bd91cde6704ecd71585df832b0361520e584e1b2
                if event.type == pygame.QUIT:
                    sys.exit()

if __name__ == "__main__":
    ChessGame = chessb()
    ChessGame.run_game()
