import pygame
import sys
import chess
import math
import fenparser
import config as cfg
import evaluation

screenW=400
screenH=400
clock = pygame.time.Clock()

black = (0,0,0)
board_size = 64
board_length = math.sqrt(board_size)
square_size = int(screenH / 8)


class chessb:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((screenW,screenH))
        pygame.display.set_caption('AlfaGeir')
        self.LoadImages()
        self.board = chess.Board()
        self.button = pygame.Rect(100, 100, 50, 50)
        self.from_position = None
        self.to_position = None
        self.turn = 0

    def LoadImages(self):
        self.white_block = pygame.image.load(cfg.white_square_img)
        self.brown_block = pygame.image.load(cfg.brown_square_img)
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

    def convert_to_chess_square(self, x, y):
        row = 7 - int(math.floor(y/square_size)) 
        col = int(math.floor(x/square_size))
        return chess.square(col, row) 
    
    def convert_to_screen_coordinates(self, row, column):
        x = row * (screenH/board_length)
        y = column * (screenW/board_length)
        return (x, y)

    def draw_button(self):
        pygame.draw.rect(self.screen, [255, 0, 0], self.button)
    
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
        #self.draw_button()
        pygame.display.update()

    def parse_fen(self):
        return fenparser.FenParser(self.board.fen()).parse()

    def find_column(self, pos):
        return chess.square_file(self.from_position)

    def find_row(self, pos):
        return chess.square_rank(self.from_position)
    
    def status(self):
        # check for game conditions and return the result
        if self.board.is_game_over() == True:
            print("Game Over")
            print(self.board.result())
            sys.exit()
            
    # def restart_game(self):
    #     self.board.clear()
    #     self.board = chess.Board()
    #     self.draw()

    def check_if_promotion(self):
        row = 7 - self.find_row(self.from_position)
        col = self.find_column(self.from_position)
        fen = self.parse_fen()
        if row == 1 and fen[row][col] == "P":
            return True
        elif row == 6 and fen[row][col] == "p":
            return True
        else: 
            return False

    def check_if_legal(self):
        if self.check_if_promotion():
            Nf3 = chess.Move(from_square=self.from_position, to_square=self.to_position, promotion=chess.QUEEN)
        else:    
            Nf3 = chess.Move(from_square=self.from_position, to_square=self.to_position)
        
        if Nf3 in self.board.legal_moves:
            print("legal")
            self.board.push(Nf3)
            self.turn += 1
            self.status()
        else:
            print("not a legal")
            return False

    def move_piece(self, square):
        if self.to_position == None and self.from_position != None:
            self.to_position = square
            #do the move
            self.check_if_legal()
            self.from_position = None
            self.to_position = None
            return
        if self.from_position == None:
            self.from_position = square
            return

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

    def run_game(self):
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.draw()
        
        while True:
            if self.turn%2 == 0:
                self.player_move()
            else:
                #AI
                self.board = evaluation.make_move(self.board) 
                self.turn += 1
                self.draw()
                    #if self.button.collidepoint(pos):
                    #    self.restart_game()
                

if __name__ == "__main__":
    ChessGame = chessb()
    ChessGame.run_game()
