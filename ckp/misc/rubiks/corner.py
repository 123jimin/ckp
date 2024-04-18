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

def corner_face_to_corner(face_1:int, face_2:int, face_3:int) -> int:
    """ Given three faces of a corner, clockwise starting from U or D, returns the integer representing the corner piece. """
    if face_1 in {0, 3}: return {(0, 1): 3, (0, 2): 0, (0, 4): 1, (0, 5): 2, (3, 1): 4, (3, 2): 5, (3, 4): 6, (3, 5): 7}[(face_1, face_2)]
    elif face_2 in {0, 3}: return {(0, 1): 11, (0, 2): 8, (0, 4): 9, (0, 5): 10, (3, 1): 12, (3, 2): 13, (3, 4): 14, (3, 5): 15}[(face_2, face_3)]
    else: return {(0, 1): 19, (0, 2): 16, (0, 4): 17, (0, 5): 18, (3, 1): 20, (3, 2): 21, (3, 4): 22, (3, 5): 23}[(face_3, face_1)]

def cube_face_to_corner(faces: list[tuple], face_mapping: dict = {"Y":0, "B":1, "R":2, "W":3, "G":4, "O":5}):
    """
        Constructs the corner state based on faces.
        - `faces`: List of face colors, for each face. For faces other than U and D, the faces' order is (upleft, upright, downleft, downright).
        - `face_mapping`: Maps each face color into face index (UFRDBL corresponds to 012345).
    """
    return tuple(
        corner_face_to_corner(face_mapping[face_1], face_mapping[face_2], face_mapping[face_3])
        for (face_1, face_2, face_3) in (
            (faces[0][3], faces[2][1], faces[1][0]),
            (faces[0][1], faces[4][1], faces[2][0]),
            (faces[0][0], faces[5][1], faces[4][0]),
            (faces[0][2], faces[1][1], faces[5][0]),
            (faces[3][1], faces[1][3], faces[2][2]),
            (faces[3][3], faces[2][3], faces[4][2]),
            (faces[3][2], faces[4][3], faces[5][2]),
            (faces[3][0], faces[5][3], faces[1][2]),
        )
    )

def corner_to_faces(state: tuple[int, int, int, int, int, int, int, int], face_mapping: list = ["Y", "B", "R", "W", "G", "O"]) -> list[list]:
    faces = [[None] * 4 for _ in range(6)]
    for x, inds in zip(state, [((0, 3), (2, 1), (1, 0)), ((0, 1), (4, 1), (2, 0)), ((0, 0), (5, 1), (4, 0)), ((0, 2), (1, 1), (5, 0)), ((3, 1), (1, 3), (2, 2)), ((3, 3), (2, 3), (4, 2)), ((3, 2), (4, 3), (5, 2)), ((3, 0), (5, 3), (1, 2))]):
        pass
    # TODO
    raise NotImplementedError("Not yet implemented!")

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

def corner_solved_states() -> set[tuple[int]]:
    return {
        (0, 1, 2, 3, 4, 5, 6, 7), (1, 2, 3, 0, 5, 6, 7, 4), (2, 3, 0, 1, 6, 7, 4, 5), (3, 0, 1, 2, 7, 4, 5, 6),
        (4, 7, 6, 5, 0, 3, 2, 1), (5, 4, 7, 6, 1, 0, 3, 2), (6, 5, 4, 7, 2, 1, 0, 3), (7, 6, 5, 4, 3, 2, 1, 0),
        (8, 19, 15, 20, 17, 10, 22, 13), (9, 16, 12, 21, 18, 11, 23, 14), (10, 17, 13, 22, 19, 8, 20, 15), (11, 18, 14, 23, 16, 9, 21, 12),
        (12, 21, 9, 16, 23, 14, 18, 11), (13, 22, 10, 17, 20, 15, 19, 8), (14, 23, 11, 18, 21, 12, 16, 9), (15, 20, 8, 19, 22, 13, 17, 10),
        (16, 12, 21, 9, 11, 23, 14, 18), (17, 13, 22, 10, 8, 20, 15, 19), (18, 14, 23, 11, 9, 21, 12, 16), (19, 15, 20, 8, 10, 22, 13, 17),
        (20, 8, 19, 15, 13, 17, 10, 22), (21, 9, 16, 12, 14, 18, 11, 23), (22, 10, 17, 13, 15, 19, 8, 20), (23, 11, 18, 14, 12, 16, 9, 21),
    }

def corner_is_solved(state: tuple[int, int, int, int, int, int, int, int]) -> bool:
    return state in corner_solved_states()