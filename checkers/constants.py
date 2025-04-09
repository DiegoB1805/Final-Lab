import pygame

#Aqui almacenamos las constantes del juego

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
CREAM = (255, 253, 208)
BLACK = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
BROWN = (150, 80, 0)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (60, 50))