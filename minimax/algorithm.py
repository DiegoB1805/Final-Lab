from copy import deepcopy 
from checkers.constants import BLACK, WHITE
import pygame


def minimax(position, depth, max_player, game, alpha, beta):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:  # AI
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves_in_board(position, WHITE, game):
            evaluation = minimax(move, depth - 1, False, game, alpha, beta)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break  
        return maxEval, best_move
    
    else:  # Jugador humano
        minEval = float('inf')
        best_move = None
        for move in get_all_moves_in_board(position, BLACK, game):
            evaluation = minimax(move, depth - 1, True, game, alpha, beta)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break  # Poda alpha
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1]) #Movemos a esa row y col
    if skip: #Si hay un salto, removemos la pieza saltada
        board.remove(skip)

    return board

#Obtenemos todos los movimientos
def get_all_moves_in_board(board, color, game):
    moves = [] #lista para almacenar [[tablero, pieza], [nuevoTablero, pieza] ...]

    for piece in board.get_all_pieces(color): #Hacemos un loop por todas las piezas de un mismo color
        valid_moves = board.get_valid_moves(piece)  #diccionario que almacena [{(row, col): [piezasSaltadas]}
        for move, skip in valid_moves.items():
            #draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip) #Simulamos el proximo movimiento y lo guardamos en new_board
            moves.append(new_board)  #Agregamos el nuevo tablero a la lista de movimientos
    
    return moves

#Metodo opcional para ver movimientos cuando se va haciendo el minimax
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.window)
    pygame.draw.circle(game.window, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(100)
   
