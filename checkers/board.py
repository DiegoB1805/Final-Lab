import pygame
from checkers.constants import BLACK, ROWS, BLACK, SQUARE_SIZE, COLS, WHITE, BROWN, CREAM
from checkers.piece import Piece 

#En esta clase se define el tablero y las piezas, como se dibujan y como se mueven.

class Board:
    #En este metodo inicializamos la lista board, creamos el tablero y definimos la cantidad de piezas
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()
    
    #En este metodo dibujamos las casillas del tablero                
    def draw_squares(self, window):
        window.fill(BROWN) #Inicializamos el color del tablero
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                #Dibujamos el cuadrado rojo
                pygame.draw.rect(window, CREAM, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    #Adjuntamos el tablero a la lista board y ponemos las piezas en su lugar
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):  #Verificamos si la casilla es negra y no ponemos piezas en las 2 filas del medio
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    #En este metodo dibujamos todo el tablero y las piezas
    def draw(self, window):
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)
    
    #Aqui movemos la pieza seleccionada a la nueva posicion y verificamos si se convierte en rey
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0: #La verificacion funciona para ambos colores
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1 

    #Aqui obtenemos la pieza en la posicion seleccionada
    def get_piece(self, row, col):
        return self.board[row][col]

    
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

        if piece.color == BLACK or piece.king: #si la pieza es roja o rey, revisamos si puede moverse hacia arriba
            moves.update(self._search_left_diagonal(row -1, max(row-3, -1), -1, piece.color, left)) #Guardamos los movimientos validos en moves
            moves.update(self._search_right_diagonal(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._search_left_diagonal(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._search_right_diagonal(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves #Devolvemos los movimientos validos

    # Método para buscar movimientos válidos en la diagonal izquierda (izquierda-arriba o izquierda-abajo)
    def _search_left_diagonal(self, start, stop, step, color, left, skipped=[]):
        moves = {}      # Diccionario para almacenar los movimientos válidos y las piezas saltadas
        last = []       # Lista para almacenar una posible pieza que se podría saltar

        # Recorremos las filas en el rango especificado
        for r in range(start, stop, step):
            if left < 0:  # Si se sale del tablero por la izquierda, se detiene
                break
            
            current = self.board[r][left]  # Obtenemos la casilla actual en la diagonal

            if current == 0:  # Si la casilla está vacía
                if skipped and not last:
                    break  # No se puede saltar una pieza si no había una justo antes
                elif skipped:
                    # Si ya había piezas saltadas previamente, las agregamos al nuevo movimiento
                    moves[(r, left)] = last + skipped
                else:
                    # Si no se han saltado piezas aún, simplemente se añade el movimiento
                    moves[(r, left)] = last
                
                if last:
                    # Si se saltó una pieza en este paso, se busca recursivamente más movimientos encadenados
                    new_skipped = skipped + last if skipped else last

                    # Determinamos el nuevo límite para la búsqueda recursiva según la dirección del paso
                    if step == -1:
                        row = max(r-3, -1)  # Asegura que no se salga del tablero por arriba
                    else:
                        row = min(r+3, ROWS)  # Asegura que no se salga del tablero por abajo

                    # Búsqueda recursiva en ambas diagonales para explorar múltiples capturas
                    moves.update(self._search_left_diagonal(r+step, row, step, color, left-1, skipped=new_skipped))
                    moves.update(self._search_right_diagonal(r+step, row, step, color, left+1, skipped=new_skipped))
                
                break  # Después de encontrar un movimiento válido, no seguimos en esta dirección

            elif current.color == color:
                break  # Si encuentra una pieza del mismo color, no puede seguir en esa dirección

            else:
                # Se encontró una pieza del color opuesto, posible objetivo para saltar
                last = [current]

            # Avanzamos a la siguiente columna a la izquierda
            left -= 1
        
        return moves  # Retornamos el diccionario con los movimientos válidos encontrados

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
                    new_skipped = skipped + last if skipped else last
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._search_left_diagonal(r+step, row, step, color, right-1,skipped=new_skipped))
                    moves.update(self._search_right_diagonal(r+step, row, step, color, right+1,skipped=new_skipped))
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
