"""
    Contains codes for representing and manipulating corner states of a Rubik's cube.

    Each corner piece is represented by an integer:
    - Bits 0-2: corner position (0-7)
        - URF UBR ULB UFL DFR DRB DBL DLF
    - Bits 3-4: corner orientation (0-2)
        - 0 when U or B is in the right place. +1 for every clockwise corner turn.

    A corner state is a tuple of 8 corner pieces, where the 0th element is the corner piece at URF position, etc....
"""

CornerState = tuple[int, int, int, int, int, int, int, int]

def corner_init() -> CornerState:
    """ Returns the initial corner state. """
    return (0, 1, 2, 3, 4, 5, 6, 7)

def corner_turn(state: CornerState, action: int) -> CornerState:
    """ Returns a new corner state with the action applied. """
    urf, ubr, ulb, ufl, dfr, drb, dbl, dlf = state
    match action:
        case 1: return ()
        case 2: return ()
        case 3: return ()
        case _: return state