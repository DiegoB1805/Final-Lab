
import pygame
from .constants import BROWN, ROWS, CREAM, SQUARE_SIZE, COLS, WHITE, BLACK
from .piece import Piece 

#En esta clase se define el tablero y las piezas, como se dibujan y como se mueven.

class Board:
     #En este metodo inicializamos la lista board, creamos el tablero y definimos la cantidad de piezas
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()
     #En este metodo dibujamos las casillas del tablero       
    def draw_squares(self, win):
        win.fill(BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, CREAM, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
  #Aqui movemos la pieza seleccionada a la nueva posicion y verificamos si se convierte en rey
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1 
  #Aqui obtenemos la pieza en la posicion seleccionada
    def get_piece(self, row, col):
        return self.board[row][col]
    

 #Adjuntamos el tablero a la lista board y ponemos las piezas en su lugar
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    #En este metodo dibujamos todo el tablero y las piezas   
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1
    #Aqui verificamos si hay un ganador, si no hay piezas del color rojo o blanco
    def winner(self):
        if self.black_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            moves.update(self._search_left_diagonal(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._search_right_diagonal(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._search_left_diagonal(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._search_right_diagonal(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _search_left_diagonal(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                                    # Verificar si está en la fila de rey
                    if (color == BLACK and r == 0) or (color == WHITE and r == ROWS - 1):
                        # Explorar hacia arriba y abajo
                        # Dirección hacia arriba (step -1)
                        moves.update(self._search_left_diagonal(r - 1, max(r-3, -1), -1, color, left - 1, skipped=last))
                        moves.update(self._search_right_diagonal(r - 1, max(r-3, -1), -1, color, left + 1, skipped=last))
                        # Dirección hacia abajo (step 1)
                        moves.update(self._search_left_diagonal(r + 1, min(r+3, ROWS), 1, color, left - 1, skipped=last))
                        moves.update(self._search_right_diagonal(r + 1, min(r+3, ROWS), 1, color, left + 1, skipped=last))
                    else:
                        # Continuar en la dirección original
                        new_start = r + step
                        if step == -1:
                            new_stop = max(new_start - 2, -1)
                        else:
                            new_stop = min(new_start + 2, ROWS)
                        moves.update(self._search_left_diagonal(new_start, new_stop, step, color, left - 1, skipped=last))
                        moves.update(self._search_right_diagonal(new_start, new_stop, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _search_right_diagonal(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                     # Verificar si está en la fila de rey
                    if (color == BLACK and r == 0) or (color == WHITE and r == ROWS - 1):
                        # Explorar hacia arriba y abajo
                        # Dirección hacia arriba (step -1)
                        moves.update(self._search_left_diagonal(r - 1, max(r-3, -1), -1, color, right - 1, skipped=last))
                        moves.update(self._search_right_diagonal(r - 1, max(r-3, -1), -1, color, right + 1, skipped=last))
                        # Dirección hacia abajo (step 1)
                        moves.update(self._search_left_diagonal(r + 1, min(r+3, ROWS), 1, color, right - 1, skipped=last))
                        moves.update(self._search_right_diagonal(r + 1, min(r+3, ROWS), 1, color, right + 1, skipped=last))
                    else:
                        # Continuar en la dirección original
                        new_start = r + step
                        if step == -1:
                            new_stop = max(new_start - 2, -1)
                        else:
                            new_stop = min(new_start + 2, ROWS)
                        moves.update(self._search_left_diagonal(new_start, new_stop, step, color, right - 1, skipped=last))
                        moves.update(self._search_right_diagonal(new_start, new_stop, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    #Aqui verificamos el valor del movimiento
    def evaluate(self):
        return self.white_left - self.black_left + ((self.white_kings - self.black_kings ) * 0.5) #Tomando en cuenta el valor de los reyes
    
    #Conseguimos todas las piezas de un mismo color
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
