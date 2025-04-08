from .constants import BLACK, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame

class Piece:
    #Aqui tenemos las constantes para el tamaño de la pieza y el contorno
    PADDING = 15
    OUTLINE = 4

    #Aqui inicializamos la pieza con su color, posicion y si es rey o no
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

     #Aqui calculamos la posicion de la pieza en el tablero
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    #Definimos la pieza como rey
    def make_king(self):
        self.king = True
    
    #Aqui dibujamos la pieza en el tablero
    def draw(self, window):
        radius = SQUARE_SIZE//2 - self.PADDING  #Calculamos el radio de la pieza
        pygame.draw.circle(window, GREY, (self.x, self.y), radius + self.OUTLINE) #Dibujamos el contorno
        pygame.draw.circle(window, self.color, (self.x, self.y), radius) #Dibujamos la pieza
        if self.king:
            window.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2)) #Dibujamos la corona en la pieza si es rey

    #Cambiamos la columna y fila de la pieza y su nueva posicion
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)