import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
CREAM = CREAM = (255, 253, 208)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19) 
BLACK = (0,0,0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))