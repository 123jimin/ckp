"""
    Contains codes for representing and manipulating corner states of a Rubik's cube.

    Each corner piece is represented by an integer:
    - Bits 0-2: corner position (0-7)
        - URF UBR ULB UFL DFR DRB DBL DLF
    - Bits 3-4: corner orientation (0-2)
        - 0 when U or B is in the right place. +1 for every clockwise corner turn.

    A corner state is a tuple of 8 corner pieces, where the 0th element is the corner piece at URF position, etc....
"""

def corner_init():
    """ Returns the initial corner state. """
    return (0, 1, 2, 3, 4, 5, 6, 7)

def corner_turn(state: tuple[int, int, int, int, int, int, int, int], move: int):
    """ Returns a new corner state with the move applied. """
    urf, ubr, ulb, ufl, dfr, drb, dbl, dlf = state
    match move:
        # U, U2, U'
        case 1: return (ubr, ulb, ufl, urf, dfr, drb, dbl, dlf)
        case 2: return (ulb, ufl, urf, ubr, dfr, drb, dbl, dlf)
        case 3: return (ufl, urf, ubr, ulb, dfr, drb, dbl, dlf)
        # F, F2, F'
        case 5: return ((ufl+8)%24, ubr, ulb, (dlf-8)%24, (urf-8)%24, drb, dbl, (dfr+8)%24)
        case 6: return (dlf, ubr, ulb, dfr, ufl, drb, dbl, urf)
        case 7: return ((dfr+8)%24, ubr, ulb, (urf-8)%24, (dlf-8)%24, drb, dbl, (ufl+8)%24)
        # R, R2, R'
        case 9: return ((dfr-8)%24, (urf+8)%24, ulb, ufl, (drb+8)%24, (ubr-8)%24, dbl, dlf)
        case 10: return (drb, dfr, ulb, ufl, ubr, urf, dbl, dlf)
        case 11: return ((ubr-8)%24, (drb+8)%24, ulb, ufl, (urf+8)%24, (dfr-8)%24, dbl, dlf)
        # D, D2, D'
        case 17: return (urf, ubr, ulb, ufl, dlf, dfr, drb, dbl)
        case 18: return (urf, ubr, ulb, ufl, dbl, dlf, dfr, drb)
        case 19: return (urf, ubr, ulb, ufl, drb, dbl, dlf, dfr)
        # B, B2, B'
        case 21: return (urf, (drb-8)%24, (ubr+8)%24, ufl, dfr, (dbl+8)%24, (ulb-8)%24, dlf)
        case 22: return (urf, dbl, drb, ufl, dfr, ulb, ubr, dlf)
        case 23: return (urf, (ulb-8)%24, (dbl+8)%24, ufl, dfr, (ubr+8)%24, (drb-8)%24, dlf)
        # L, L2, L'
        case 25: return (urf, ubr, (dbl-8)%24, (ulb+8)%24, dfr, drb, (dlf+8)%24, (ufl-8)%24)
        case 26: return (urf, ubr, dlf, dbl, dfr, drb, ufl, ulb)
        case 27: return (urf, ubr, (ufl-8)%24, (dlf+8)%24, dfr, drb, (ulb+8)%24, (dbl-8)%24)
        # Other moves (presumably on inner layers)
        case _: return state