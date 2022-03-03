"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """Returns starting state of the board.
            0       1       2
    0   [EMPTY, EMPTY, EMPTY]
    1   [EMPTY, EMPTY, EMPTY]
    2   [EMPTY, EMPTY, EMPTY]
    """
    return [[EMPTY]*3 for _ in range(3)]


def player(board) -> str:
    """Returns player who has the next turn on a board."""
    all_keys = ''.join(f"{col}" for row in board for col in row if col is not None)
    x_count = all_keys.count(X)
    o_count = all_keys.count(O)

    if x_count > o_count:
        return O
    else:
        return X


def actions(board) -> list[tuple]:
    """Returns set of all possible actions (i, j) available on the board."""
    return [(row, col) for row in range(3) for col in range(3) if board[row][col] is None]


def result(board, action) -> list[list[str]]:
    """Returns the board that results from making move (i, j) on the board."""
    board_placeholder = copy.deepcopy(board)
    try:
        if board_placeholder[action[0]][action[1]] is None:
            board_placeholder[action[0]][action[1]] = player(board_placeholder)
            return board_placeholder
        raise IndexError
    except IndexError:
        raise NameError('NotValidActionError')


def winner(board):
    """Returns the winner of the game, if there is one."""

    # row
    for row in board:
        if len(set(row)) == 1 and row[0] is not None:
            return row[0]
    # col
    for col in list(map(list, zip(*board))):
        if len(set(col)) == 1 and col[0] is not None:
            return col[0]

    if board[1][1] is not None:
        # top left diag
        if len(set(board[i][i] for i in range(3))) == 1:
            return board[0][0]

        # top right diag
        if len(set(board[i][len(board)-i-1] for i in range(3))) == 1:
            return board[0][len(board)-1]

    return None


def terminal(board) -> bool:
    """Returns True if game is over, False otherwise."""
    return True if all(col is not None for row in board for col in row) or winner(board) else False


def utility(board) -> int:
    """Returns 1 if X has won the game, -1 if O has won, 0 otherwise."""
    key_open = winner(board)
    if key_open == X:
        return 1
    elif key_open == O:
        return -1
    return 0


def minimax(board) -> tuple:
    """Returns the optimal action with Alpha-Beta Pruning for the current player on the board."""

    def x_max(board, alpha, beta) -> int:
        """score as large as possible"""
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            v = max(v, o_min(result(board, action), alpha, beta))
            if v >= beta:
                return v
            if v > alpha:
                alpha = v
        return v

    def o_min(board, alpha, beta) -> int:
        """score as small as possible"""
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, x_max(result(board, action), alpha, beta))
            if v <= alpha:
                return v
            if v < beta:
                beta = v
        return v

    tempscore = -math.inf
    if player(board) == X:
        for act in actions(board):  # gets all possible moves
            score = o_min(result(board, act), -2, 2)
            if score > tempscore:
                tempscore = score
                optmove = act
        return optmove

    tempscore = math.inf
    for act in actions(board):
        score = x_max(result(board, act), -2, 2)
        if score < tempscore:
            tempscore = score
            optmove = act
    return optmove
