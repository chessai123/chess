import pygame
import sys
import chess
import math
import fenparser as fp

screenW=400
screenH=400
clock = pygame.time.Clock()

black = (0,0,0)
board_size = 8
column_letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
square_size = 50
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

    def convert_to_screen_coordinates(self, column, row):
        x = row * (screenH/board_size)
        y = column * (screenW/board_size)
        return (x, y)
    
    def draw_board(self):
        # draw the squares on the board 8*8
        self.screen.fill(black)
        current_square = 0
        for i in range(board_size):
            for j in range(board_size):
                (x, y) = self.convert_to_screen_coordinates(i, j)
                if (current_square % 2) == 0:
                    self.screen.blit(self.brown_block, (x,y))
                else:
                    self.screen.blit(self.white_block, (x,y))
                current_square += 1
            current_square += 1
        

    def draw(self):
        self.draw_board()
        
        # parse and filter the piece string
        fen = self.board.fen().split(" ", 1)
        fen = fen[0].split("/", 8)
        
        # find from pos - to pos
        if self.from_position:
            col = 1
            for i in column_letter:
                if i == self.from_position[0]:
                    break
                col += 1
            row = 7 - int(self.from_position[1])
            (x,y) = self.convert_to_screen_coordinates(col, row)
            self.screen.blit(self.highlight_block, (x,y))
        
        # iterate over board squares (rows,columns) and convert coordinates
        current_square = 0
        for i in range(board_size):
            print(fen[i])
            for j in range(board_size):
                (x, y) = self.convert_to_screen_coordinates(i, j)
                print(j)
                if j >= board_size:
                    break

                # stop if board array is out of range
                if fen[i][j] == "8":
                    break
                
                # draw piece according to piece board pos 
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
                
                
                if type(fen[i][j]) == type(4):
                    print("type check")
                    j += int(fen[i][j])
                else:
                    current_square += 1
            current_square += 1
        pygame.display.update()

    def update(self):
        pass

    def convert_to_board_pos(self, x, y):
        row = 8 - math.floor(y/square_size) 
        column = math.floor(x/square_size)
        column = column_letter[column]
        pos = column + str(row)
        return pos

    def is_legal_move(self, move):
        #print(self.board.legal_moves)
        Nf3 = chess.Move.from_uci(move)
        if Nf3 in self.board.legal_moves:
            self.board.push(Nf3) 
            print(self.board.fen())
            self.draw()
        else:
            return False
            

    def game_loop(self):
        self.draw()
        while True:            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.draw()
                    if event.button == 1:
                        #button_states = pygame.mouse.get_pressed()            
                        pos = pygame.mouse.get_pos()
                        # checks from and to pos & checks for legality of said pos/move
                        if self.from_position != None and self.to_position == None:
                            #print("second check")
                            board_pos = self.convert_to_board_pos(pos[0], pos[1])
                            self.to_position = board_pos
                            move = self.from_position + self.to_position
                            print(move)
                            status = self.is_legal_move(move)
                            if status == False:
                                print("not a legal move")
                            
                            self.from_position = None
                            self.to_position = None

                        # maps from pos
                        if self.from_position == None:
                            board_pos = self.convert_to_board_pos(pos[0], pos[1])
                            print(board_pos)
                            self.from_position = board_pos
                            pos = None

                    
            if event.type == pygame.QUIT:
                sys.exit()
        
if __name__ == "__main__":
    board = chessb()
    board.game_loop()