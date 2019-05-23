import pygame
import sys
import chess
import math
import fenparser
import config as cfg
import evaluation

""" Change parameters to set resolution """
boardW = 800
boardH = 800
screenW = 800
screenH = 800

black = (0,0,0)
board_size = 64
board_length = math.sqrt(board_size)
square_size = int(screenH / 8)

class chessBoard:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption("AlfaGeir")
        self.screen = pygame.display.set_mode((screenW,screenH))
        self.LoadImages()
        self.board = chess.Board()
        self.from_position = None
        self.to_position = None
        self.turn = 0

    def LoadImages(self):
        self.white_block = pygame.image.load(cfg.white_square_img)
        self.white_block = pygame.transform.scale(self.white_block, (square_size,square_size))

        self.brown_block = pygame.image.load(cfg.brown_square_img)
        self.brown_block = pygame.transform.scale(self.brown_block, (square_size,square_size))

        self.highlight_block = pygame.image.load(cfg.cyanid_square_img)
        self.highlight_block = pygame.transform.scale(self.highlight_block, (square_size,square_size))
        
        self.black_pawn = pygame.image.load(cfg.black_pawn_img)
        self.black_pawn = pygame.transform.scale(self.black_pawn, (square_size,square_size))
        self.white_pawn = pygame.image.load(cfg.white_pawn_img)
        self.white_pawn = pygame.transform.scale(self.white_pawn, (square_size,square_size))     
        self.black_bishop = pygame.image.load(cfg.black_bishop_img)
        self.black_bishop = pygame.transform.scale(self.black_bishop, (square_size,square_size))
        self.white_bishop = pygame.image.load(cfg.white_bishop_img)
        self.white_bishop = pygame.transform.scale(self.white_bishop, (square_size,square_size)) 
        self.black_king = pygame.image.load(cfg.black_king_img)
        self.black_king = pygame.transform.scale(self.black_king, (square_size,square_size))
        self.white_king = pygame.image.load(cfg.white_king_img)
        self.white_king = pygame.transform.scale(self.white_king, (square_size,square_size)) 
        self.black_horse = pygame.image.load(cfg.black_horse_img)
        self.black_horse = pygame.transform.scale(self.black_horse, (square_size,square_size))
        self.white_horse = pygame.image.load(cfg.white_horse_img)
        self.white_horse = pygame.transform.scale(self.white_horse, (square_size,square_size)) 
        self.black_queen = pygame.image.load(cfg.black_queen_img)
        self.black_queen = pygame.transform.scale(self.black_queen, (square_size,square_size))
        self.white_queen = pygame.image.load(cfg.white_queen_img)
        self.white_queen = pygame.transform.scale(self.white_queen, (square_size,square_size)) 
        self.black_tower = pygame.image.load(cfg.black_tower_img)
        self.black_tower = pygame.transform.scale(self.black_tower, (square_size,square_size))
        self.white_tower = pygame.image.load(cfg.white_tower_imp)
        self.white_tower = pygame.transform.scale(self.white_tower, (square_size,square_size)) 

    """" Maps mouseclick to chessboard """
    def convert_to_chess_square(self, x, y):
        #since the board is represented different from how it is drawn
        #we need to flip the row to get the right row number. 
        row = 7 - int(math.floor(y/square_size)) 
        col = int(math.floor(x/square_size))
        return chess.square(col, row) 

    def convert_to_board_coordinates(self, row, column):
        x = row * (boardH/board_length)
        y = column * (boardW/board_length)
        return (x, y)

    

    def draw_board_squares(self):
        self.screen.fill(black)

        for i in range(board_size):
            col = math.floor(i / board_length)
            row = (i % board_length)
            (x, y) = self.convert_to_board_coordinates(row, col)  

            if ((x+y)/square_size) % 2 == 1: 
                self.screen.blit(self.brown_block, (x, y))
            else:
                self.screen.blit(self.white_block, (x, y))
           
        if self.from_position:
            row = self.find_row(self.from_position)
            col = self.find_column(self.from_position)

            (x, y) = self.convert_to_board_coordinates(col, row)
            #need to flip the y to get the right coordinate since the boards first square
            #is in the lower left corner, while the coordinates start in the upper left corner
            y = screenH - y - square_size 
            self.screen.blit(self.highlight_block, (x, y))
                
    
    """" Draws pieces to the screen/squares(columns and rows) according to the passed fen-string """
    def draw_pieces(self, fen):
        for i in range(board_size):
            col = int(math.floor(i / board_length))
            row = int(i % board_length)
            (x, y) = self.convert_to_board_coordinates(row, col)
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

    def parse_fen(self):
        return fenparser.FenParser(self.board.fen()).parse()

    def find_column(self, pos):
        return chess.square_file(self.from_position)

    def find_row(self, pos):
        return chess.square_rank(self.from_position)
    
    """" Check for game status, ends game if either player wins or draws """
    def status(self):
        if self.board.is_game_over() == True:
            print("Game Over")
            print(self.board.result())
            if self.board.result() == "1-0":
                print("White Won")
            elif self.board.result() == "0-1":
                print("Black Won")
            else:
                print("Game is drawn")

            sys.exit()

    
    def check_if_promotion(self):
        # flip the row to get the right row according to the chess board
        row = 7 - self.find_row(self.from_position)
        col = self.find_column(self.from_position)
        fen = self.parse_fen()
        
        #if it is a pawn moving to the last row it is a promotion
        if row == 1 and fen[row][col] == "P":
            return True
        elif row == 6 and fen[row][col] == "p":
            return True
        else: 
            return False

    def check_if_legal(self):
        if self.check_if_promotion():
            #promote to a queen
            Nf3 = chess.Move(from_square=self.from_position, to_square=self.to_position, promotion=chess.QUEEN)
        else:    
            Nf3 = chess.Move(from_square=self.from_position, to_square=self.to_position)
        
        if Nf3 in self.board.legal_moves:
            print("legal")
            self.board.push(Nf3)
            self.turn += 1
            self.status()
        else:
            print("not legal")
            return False
    
    def move_piece(self, square):
        if self.to_position == None and self.from_position != None:
            self.to_position = square
            self.check_if_legal()
            
            self.from_position = None
            self.to_position = None
            return

        if self.from_position == None:
            self.from_position = square
            return

    """" Player events """
    def player_move(self):
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        square = self.convert_to_chess_square(pos[0], pos[1])
                        self.move_piece(square)
                        self.draw()
                    
                if event.type == pygame.QUIT:
                        sys.exit()

    """" AI vs AI game loop """
    def run_game_AIvAI(self):
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.draw()
        pygame.display.set_caption("AlfaGeir vs AlfaGeir")
        self.screen = pygame.display.set_mode((screenW,screenH))
        while True:
            if self.turn % 2 == 0:
                self.screen = pygame.display.set_mode((screenW,screenH))
                self.board = evaluation.make_move(self.board)
                self.turn += 1
                self.draw()
            else: 
                self.screen = pygame.display.set_mode((screenW,screenH))
                self.board = evaluation.make_move(self.board) 
                self.turn += 1
                self.draw()

    """" Player vs AI game loop """
    def run_game_playerVsAI(self):
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.draw()
        
        while True:
            if self.turn % 2 == 0:
                pygame.display.set_caption("AlfaGeir - White to move")
                self.screen = pygame.display.set_mode((screenW,screenH))
                self.player_move()
                
            else:
                pygame.display.set_caption("AlfaGeir - AI thinking...")
                self.screen = pygame.display.set_mode((screenW,screenH))
                self.board = evaluation.make_move(self.board) 
                self.turn += 1
                self.draw()
    
    def run_game_playerVsPlayer(self):
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.draw()

        while True:
            if self.turn % 2 == 0:
                self.player_move()
                self.turn += 1
            else:
                self.player_move()
                self.turn += 1

    def cmd_choices(self):
        while(1):
            print('Welcome to AlfaGeir!')
            print('To play vs the AI type "1"')
            print('To see AI vs AI type "2"')
            print('To play player vs player type "3"')
            print('To exit type "exit" or "quit"')
            user_input = input("> ")
            command = user_input.split(' ', 1)
            command[0].lower()

            if (command[0] == "1"):
                ChessGame.run_game_playerVsAI()
            elif (command[0] == "2"):
                ChessGame.run_game_AIvAI()
            elif (command[0] == "3"):
                ChessGame.run_game_playerVsPlayer()
            elif (command[0] == "quit" or command[0] == "exit"):
                break

                
if __name__ == "__main__":
    ChessGame = chessBoard()
    ChessGame.cmd_choices()
