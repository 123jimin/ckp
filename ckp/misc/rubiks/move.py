"""
    Contains code for converting between move list and string, primarily for I/O or debugging purposes.
"""

def move_to_str(move: int) -> str:
    layer, turns = divmod(move, 4)
    return "UFR?DBL?"[layer] + ("0", "", "2", "'")[turns]

def moves_to_str(moves: list[int]) -> str:
    return "".join(move_to_str(move) for move in moves)

def str_to_move(s: str) -> int:
    layer = "UFR?DBL".index(s[0])
    turn = "??2'".index(s[1]) if len(s) > 1 else 1
    return 4*layer + turn

def str_to_moves(s: str) -> list[int]:
    a = []
    prev_move = None
    for c in s:
        if c in "UFRDBL":
            if prev_move is not None: a.append(prev_move)
            prev_move = 4*"UFR?DBL".index(c) + 1
        elif c in "2'":
            a.append(prev_move + "?2'".index(c))
            prev_move = None
    if prev_move is not None: a.append(prev_move)
    return a

def inverse_move(move: int) -> int:
    return move ^ ((move%2) * 2)

def inverse_moves(moves: list[int]) -> list[int]:
    return list(reversed(inverse_move(move) for move in moves))