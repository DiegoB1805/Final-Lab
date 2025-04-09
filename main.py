
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE
from checkers.game import Game
from minimax.algorithm import minimax


FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(position):
    x, y = position
    row = y // SQUARE_SIZE # Calcula fila basada en posición Y
    col = x // SQUARE_SIZE # Calcula columna basada en posición X
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW) # Crea una instancia del juego 

    while run:
        clock.tick(FPS)
          # Verifica si hay un ganador
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, WHITE, game)
            game.ai_move(new_board)
        if game.winner() != None:
            print(game.winner())
            run = False
          # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(position)
                game.select(row, col)

        game.update()
    
    pygame.quit()

main()