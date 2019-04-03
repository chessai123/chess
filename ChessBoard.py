import pygame
import sys
import chess
import time

screenW=400
screenH=400

black = (0,0,0)
board_size = 8

brown_square_img    = "images/brown_square.png"
white_square_img    = "images/white_square.png"

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

bk = "e8"
wk = "e1"


class chessb:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((screenW,screenH))
        pygame.display.set_caption('AlfaGeir')
        self.LoadImages()
        self.square_size = 50
        #self.screen.fill(black)
        self.board = chess.Board()

    def LoadImages(self):
        self.white_block = pygame.image.load(white_square_img)
        self.brown_block = pygame.image.load(brown_square_img)

        self.black_pawn = pygame.image.load(black_pawn_img)
        self.black_pawn = pygame.transform.scale(self.black_pawn, (50,50))
        self.white_pawn = pygame.image.load(white_pawn_img)
        self.white_pawn = pygame.transform.scale(self.white_pawn, (50,50))     
        self.black_bishop = pygame.image.load(black_bishop_img)
        self.black_bishop = pygame.transform.scale(self.black_bishop, (50,50))
        self.white_bishop = pygame.image.load(white_bishop_img)
        self.white_bishop = pygame.transform.scale(self.white_bishop, (50,50)) 
        self.black_king = pygame.image.load(black_king_img)
        self.black_king = pygame.transform.scale(self.black_king, (50,50))
        self.white_king = pygame.image.load(white_king_img)
        self.white_king = pygame.transform.scale(self.white_king, (50,50)) 
        self.black_horse = pygame.image.load(black_horse_img)
        self.black_horse = pygame.transform.scale(self.black_horse, (50,50))
        self.white_horse = pygame.image.load(white_horse_img)
        self.white_horse = pygame.transform.scale(self.white_horse, (50,50)) 
        self.black_queen = pygame.image.load(black_queen_img)
        self.black_queen = pygame.transform.scale(self.black_queen, (50,50))
        self.white_queen = pygame.image.load(white_queen_img)
        self.white_queen = pygame.transform.scale(self.white_queen, (50,50)) 
        self.black_tower = pygame.image.load(black_tower_img)
        self.black_tower = pygame.transform.scale(self.black_tower, (50,50))
        self.white_tower = pygame.image.load(white_tower_imp)
        self.white_tower = pygame.transform.scale(self.white_tower, (50,50)) 

    def convert_to_screen_coordinates(self, column, row):
        x = row * (screenH/board_size)
        y = column * (screenW/board_size)
        return (x, y)

    def draw(self):
        self.screen.fill(black)
        current_square = 0
        for i in range(board_size):
            for j in range(board_size):
                (x, y) = self.convert_to_screen_coordinates(i, j)
                if (current_square%2) == 0:
                    self.screen.blit(self.brown_block, (x,y))
                else:
                    self.screen.blit(self.white_block, (x,y))
                current_square += 1
            current_square += 1


        """rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"""
        fen = chess.STARTING_BOARD_FEN.split("/", 8)
        
        print(fen)
        current_square = 0
        for i in range(board_size):
            for j in range(board_size):
                (x, y) = self.convert_to_screen_coordinates(i, j)

                if fen[i][j] == "8":
                    break
                
                if fen[i][j] == "p":
                    self.screen.blit(self.black_pawn, (x,y))
                if fen[i][j] == "P":
                    self.screen.blit(self.white_pawn, (x,y))
                if fen[i][j] == "q":
                    self.screen.blit(self.black_queen, (x,y))
                if fen[i][j] == "Q":
                    self.screen.blit(self.white_queen, (x,y))
                if fen[i][j] == "k":
                    self.screen.blit(self.black_king, (x,y))
                if fen[i][j] == "K":
                    self.screen.blit(self.white_king, (x,y))
                if fen[i][j] == "r":
                    self.screen.blit(self.black_tower, (x,y))
                if fen[i][j] == "R":
                    self.screen.blit(self.white_tower, (x,y))
                if fen[i][j] == "n":
                    self.screen.blit(self.black_horse, (x,y))
                if fen[i][j] == "N":
                    self.screen.blit(self.white_horse, (x,y))
                if fen[i][j] == "b":
                    self.screen.blit(self.black_bishop, (x,y))
                if fen[i][j] == "B":
                    self.screen.blit(self.white_bishop, (x,y))
                
            
        pygame.display.update()
                


if __name__ == "__main__":
    board = chessb()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        board.draw()