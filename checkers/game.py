import pygame
from .constants import BLACK, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board

#En este archivo se encuentra la clase Game, que es la encargada de manejar los turnos y la logica de los movimientos.
class Game:
    def __init__(self, window):
        self._init()
        self.window = window
    
    #Este metodo se encarga de actualizar el display y dibujar el tablero y las piezas
    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    #Metodo para inicializar el juego
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    #Metodo dentro de game para llamar al winner del board
    def winner(self):
        return self.board.winner()
    
    #Este metodo se encarga de reiniciar el juego
    def reset(self):
        self._init()

    #Este metodo se encarga de seleccionar la pieza y verificar si el movimiento es valido
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col) #Intentamos mover la pieza seleccionada a la nueva posicion
            if not result:
                self.selected = None
                self.select(row, col) #Llamamos recursivamente si el movimiento no es valido
        
        piece = self.board.get_piece(row, col)  #Obtenemos la pieza en la posicion seleccionada
        if piece != 0 and piece.color == self.turn: #Verificamos si la pieza es del color del jugador actual
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece) 
            return True
            
        return False

    #Este metodo se encarga de mover la pieza seleccionada a la nueva posicion y verificar si el movimiento es valido
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves: #Revisamos si el lugar seleccionado es 0, para mover la pieza
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    #Dibujamos los movimientos validos en el tablero con un circulo 
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    #Metodo para cambiar el turno del jugador
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK


    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()       