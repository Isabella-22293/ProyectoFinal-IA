import random 
from copy import deepcopy
from bot import ai_move as random_ai_move, valid_movements, in_bounds, DIRECTIONS
from othello_ai import ai_move as smart_ai_move  # Tu bot inteligente

def make_move(board, move, player):
    x, y = move
    new_board = deepcopy(board)
    new_board[x][y] = player

    for dx, dy in DIRECTIONS:
        i, j = x + dx, y + dy
        flips = []
        while in_bounds(i, j) and new_board[i][j] == -player:
            flips.append((i, j))
            i += dx
            j += dy
        if in_bounds(i, j) and new_board[i][j] == player:
            for fx, fy in flips:
                new_board[fx][fy] = player
    return new_board

def initial_board():
    board = [[0 for _ in range(8)] for _ in range(8)]
    board[3][3], board[3][4] = -1, 1
    board[4][3], board[4][4] = 1, -1
    return board

def print_board(board):
    symbols = {1: 'B', -1: 'W', 0: '.'}
    print("  " + " ".join(map(str, range(8))))
    for i, row in enumerate(board):
        print(i, " ".join(symbols[cell] for cell in row))
    print()

def count_pieces(board):
    black = sum(row.count(1) for row in board)
    white = sum(row.count(-1) for row in board)
    return black, white

def simulate_game(smart_player_color, random_player_color, print_final_board=False):
    board = initial_board()
    current_player = 1  # Las negras siempre empiezan primero en Othello
    passes = 0

    while passes < 2:
        if current_player == smart_player_color:
            move = smart_ai_move(board, current_player)
        elif current_player == random_player_color:
            move = random_ai_move(board, current_player)
        else:
            move = None  # No jugador válido (no debería ocurrir)

        if move:
            board = make_move(board, move, current_player)
            passes = 0
        else:
            passes += 1
        current_player *= -1

    black, white = count_pieces(board)

    if print_final_board:
        print_board(board)
        print(f"Resultado — Negras: {black}, Blancas: {white}")
        if black > white:
            ganador = "B"
        elif white > black:
            ganador = "W"
        else:
            ganador = "Empate"
        print(f"Ganador: {ganador}\n")

    # Retornamos el ganador en función del color y el bot
    if black > white:
        return "smart" if smart_player_color == 1 else "random"
    elif white > black:
        return "random" if smart_player_color == 1 else "smart"
    else:
        return "draw"

if __name__ == "__main__":
    wins = {"smart": 0, "random": 0, "draw": 0}
    games_to_play = 5

    for i in range(games_to_play):
        print(f"🎮 Partida {i+1}")
        if i % 2 == 0:
            # Bot inteligente negras, aleatorio blancas
            result = simulate_game(smart_player_color=1, random_player_color=-1, print_final_board=True)
        else:
            # Bot inteligente blancas, aleatorio negras
            result = simulate_game(smart_player_color=-1, random_player_color=1, print_final_board=True)
        wins[result] += 1

    print("🔚 Resultados totales:")
    print(f"🧠 Tu bot inteligente ganó {wins['smart']} partidas")
    print(f"🎲 El bot aleatorio ganó {wins['random']} partidas")
    print(f"🤝 Empates: {wins['draw']}")
