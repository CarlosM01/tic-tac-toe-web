class GameBoard:
    def __init__(self):
        self.reset()

    def reset(self):
        # Reinicia el tablero a su estado vacío
        self.board = [[None for _ in range(3)] for _ in range(3)]

    def make_move(self, row, col, player):
        # Realiza un movimiento en el tablero si la celda está vacía
        if self.board[row][col] is None:
            self.board[row][col] = player
            return True
        return False

    def check_winner(self):
        # Comprobación de las condiciones de victoria
        win_conditions = [
            [(0, 0), (0, 1), (0, 2)],  # Fila superior
            [(1, 0), (1, 1), (1, 2)],  # Fila central
            [(2, 0), (2, 1), (2, 2)],  # Fila inferior
            [(0, 0), (1, 0), (2, 0)],  # Columna izquierda
            [(0, 1), (1, 1), (2, 1)],  # Columna central
            [(0, 2), (1, 2), (2, 2)],  # Columna derecha
            [(0, 0), (1, 1), (2, 2)],  # Diagonal principal
            [(0, 2), (1, 1), (2, 0)]   # Diagonal secundaria
        ]
        # Verifica si alguna de las condiciones de victoria se cumple
        for condition in win_conditions:
            if self.board[condition[0][0]][condition[0][1]] == \
               self.board[condition[1][0]][condition[1][1]] == \
               self.board[condition[2][0]][condition[2][1]] and \
               self.board[condition[0][0]][condition[0][1]] is not None:
                return self.board[condition[0][0]][condition[0][1]]
        
        # Verifica si el tablero está lleno (empate)
        if all(cell is not None for row in self.board for cell in row):
            return 'Tie'
        return None

class MinimaxAI:
    def __init__(self, game_board):
        self.game_board = game_board

    def minimax(self, board, is_maximizing):
        winner = self.game_board.check_winner()
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif winner == 'Tie':
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] is None:
                        board[row][col] = 'O'
                        eval = self.minimax(board, False)
                        board[row][col] = None
                        max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] is None:
                        board[row][col] = 'X'
                        eval = self.minimax(board, True)
                        board[row][col] = None
                        min_eval = min(min_eval, eval)
            return min_eval

    def best_move(self):
        # Encuentra el mejor movimiento para la IA (jugador 'O')
        best_val = float('-inf')
        move = None
        for row in range(3):
            for col in range(3):
                if self.game_board.board[row][col] is None:
                    self.game_board.board[row][col] = 'O'
                    move_val = self.minimax(self.game_board.board, False)
                    self.game_board.board[row][col] = None
                    if move_val > best_val:
                        best_val = move_val
                        move = (row, col)
        return move
