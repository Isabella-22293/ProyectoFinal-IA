import time
import random

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1)
]

# -------------------------
# Funciones base del juego
# -------------------------

def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def valid_movements(board, player):
    opponent = -player
    valid_moves = []

    for x in range(8):
        for y in range(8):
            if board[x][y] != 0:
                continue
            for dx, dy in DIRECTIONS:
                i, j = x + dx, y + dy
                found_opponent = False
                while in_bounds(i, j) and board[i][j] == opponent:
                    i += dx
                    j += dy
                    found_opponent = True
                if found_opponent and in_bounds(i, j) and board[i][j] == player:
                    valid_moves.append((x, y))
                    break
    return valid_moves

def make_move(board, move, player):
    x, y = move
    new_board = [row[:] for row in board]
    new_board[x][y] = player

    for dx, dy in DIRECTIONS:
        i, j = x + dx, y + dy
        flip = []
        while in_bounds(i, j) and new_board[i][j] == -player:
            flip.append((i, j))
            i += dx
            j += dy
        if in_bounds(i, j) and new_board[i][j] == player:
            for fx, fy in flip:
                new_board[fx][fy] = player
    return new_board

# -------------------------
# Heurística simple mejorada
# -------------------------

def heuristic(board, player):
    # Ponderación de esquinas y movilidad
    corners = [(0,0), (0,7), (7,0), (7,7)]
    score = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == player:
                score += 1
                if (x, y) in corners:
                    score += 10
            elif board[x][y] == -player:
                score -= 1
                if (x, y) in corners:
                    score -= 10

    # Movilidad (cantidad de jugadas válidas)
    score += len(valid_movements(board, player)) - len(valid_movements(board, -player))
    return score

# -------------------------
# Minimax + Alfa-Beta + Tiempo
# -------------------------

def minimax(board, player, depth, alpha, beta, maximizing, start_time, time_limit):
    if time.time() - start_time > time_limit:
        raise TimeoutError()

    if depth == 0:
        return heuristic(board, player), None

    moves = valid_movements(board, player if maximizing else -player)
    if not moves:
        return heuristic(board, player), None

    best_move = None

    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            new_board = make_move(board, move, player)
            eval, _ = minimax(new_board, player, depth - 1, alpha, beta, False, start_time, time_limit)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = make_move(board, move, -player)
            eval, _ = minimax(new_board, player, depth - 1, alpha, beta, True, start_time, time_limit)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

# -------------------------
# AI con Iterative Deepening
# -------------------------

def ai_move(board, player):
    start_time = time.time()
    time_limit = 2.8  # pequeño margen antes del límite
    best_move = None
    depth = 1

    while True:
        elapsed = time.time() - start_time
        if elapsed >= time_limit:
            break
        try:
            eval_score, move = minimax(board, player, depth, float('-inf'), float('inf'),
                                       True, start_time, time_limit)
            if move is not None:
                best_move = move
            depth += 1
        except TimeoutError:
            break

    return best_move
