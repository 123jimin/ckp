"""
    Contains codes for repreenting and maintaining edges states of a Rubik's cube.

    Each edge piece is represented by an integer:
    - Bits 0-3: edge position (0-11)
        - UF, UR, UB, UL, FR, RB, BL, LF, DF, DR, DB, DL
    - Bits 4: edge orientation

    An edge state is a tuple of 12 edge pieces, where to 0th element is the edge piece at UF position, etc...
"""

def edge_init():
    """ Returns the initial edge state. """
    return (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)

def edge_turn(state: tuple[int, int, int, int, int, int, int, int, int, int, int, int], move: int):
    """ Returns a new edge state with the move applied. """
    uf, ur, ub, ul, fr, rb, bl, lf, df, dr, db, dl = state
    match move:
        # U, U2, U'
        case 1: return (ur, ub, ul, uf, fr, rb, bl, lf, df, dr, db, dl)
        case 2: return (ub, ul, uf, ur, fr, rb, bl, lf, df, dr, db, dl)
        case 3: return (ul, uf, ur, ub, fr, rb, bl, lf, df, dr, db, dl)
        # F, F2, F'
        case 5: return (lf^16, ur, ub, ul, uf^16, rb, bl, df^16, fr^16, dr, db, dl)
        case 6: return (df, ur, ub, ul, lf, rb, bl, fr, uf, dr, db, dl)
        case 7: return (fr^16, ur, ub, ul, df^16, rb, bl, uf^16, lf^16, dr, db, dl)
        # R, R2, R'
        case 9: return (uf, fr, ub, ul, dr, ur, bl, lf, df, rb, db, dl)
        case 10: return (uf, dr, ub, ul, rb, fr, bl, lf, df, ur, db, dl)
        case 11: return (uf, rb, ub, ul, ur, dr, bl, lf, df, fr, db, dl)
        # D, D2, D'
        case 17: return (uf, ur, ub, ul, fr, rb, bl, lf, dl, df, dr, db)
        case 18: return (uf, ur, ub, ul, fr, rb, bl, lf, db, dl, df, dr)
        case 19: return (uf, ur, ub, ul, fr, rb, bl, lf, dr, db, dl, df)
        # B, B2, B'
        case 21: return (uf, ur, rb^16, ul, fr, db^16, ub^16, lf, df, dr, bl^16, dl)
        case 22: return (uf, ur, db, ul, fr, bl, rb, lf, df, dr, ub, dl)
        case 23:  return (uf, ur, bl^16, ul, fr, ub^16, db^16, lf, df, dr, rb^16, dl)
        # L, L2, L'
        case 25: return (uf, ur, ub, bl, fr, rb, dl, ul, df, dr, db, lf)
        case 26: return (uf, ur, ub, dl, fr, rb, lf, bl, df, dr, db, ul)
        case 27: return (uf, ur, ub, lf, fr, rb, ul, dl, df, dr, db, bl)
        # Other moves
        case _: return state

def edge_solved_states() -> set[tuple[int]]:
    # TODO
    raise NotImplementedError("Not yet implemented!")

def edge_is_solved(state: tuple[int, int, int, int, int, int, int, int, int, int, int, int]) -> bool:
    return state in edge_solved_states()