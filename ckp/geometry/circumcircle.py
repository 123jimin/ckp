def is_in_circumcircle(C: tuple[float, tuple[float, float], float], p: tuple[float, float]) -> bool:
    """
        Given a circle (closed disc) `C` returned by `circumcircle_of_triangle` or `min_enclosing_circle`, and a point p = (x, y), returns whether `C` contains `p`.
    """
    Ca, Cp, Cr2 = C
    dx = p[0]*Ca-Cp[0]
    dy = p[1]*Ca-Cp[1]
    return dx*dx + dy*dy <= Cr2

def circumcircle_of_triangle(a: tuple[float, float], b:tuple[float, float], c:tuple[float, float]) -> tuple[float, tuple[float, float], float]:
    """
        Given a triangle abc, compute the circumcircle C of it.
        C will be given as a format (Ca, Cp, Cr2), where, given that the circumcircle is centered at (x, y) with radius r:

        - Ca > 0
        - Cp = Ca * (x, y)
        - Cr2 = (Ca * r) ** 2

        When all of `a`, `b`, `c` are integers, then all Ca, Cp, Cr2 will be integers.

        When three points are colinear, Ca will be zero.
    """

    ax, ay = a; al = ax*ax + ay*ay
    bx, by = b; bl = bx*bx + by*by
    cx, cy = c; cl = cx*cx + cy*cy

    # Det([(ax, bx, cx), (ay, by, cy), (1, 1, 1)])
    Ca = ax*(by-cy) + bx*(cy-ay) + cx*(ay-by)

    # Det([(ax, bx, cx), (ay, by, cy), (al, bl, cl)])
    Cb = ax*(by*cl - bl*cy) + bx*(cy*al - cl*ay) + cx*(ay*bl - al*by)

    # Det([(al, bl, cl), (ay, by, cy), (1, 1, 1)])
    Cx = al*(by-cy) + bl*(cy-ay) + cl*(ay-by)

    # Det([(ax, bx, cx), (al, bl, cl), (1, 1, 1)])
    Cy = ax*(bl-cl) + bx*(cl-al) + cx*(al-bl)

    if Ca < 0: Ca, Cb, Cx, Cy = -Ca, -Cb, -Cx, -Cy

    return (2*Ca, (Cx, Cy), Cx*Cx+Cy*Cy + 4*Ca*Cb)

def min_enclosing_circle(P: list[tuple[float, float]]) -> tuple[float, tuple[float, float], float]:
    """
        Given a list of points P, returns the minimal enclosing circle C.
        C will be given as a format (Ca, Cp, Cr2), where, given that the circumcircle is centered at (x, y) with radius r:

        - Ca > 0
        - Cp = Ca * (x, y)
        - Cr2 = (Ca * r) ** 2

        When all points are integral points, then all Ca, Cp, Cr2 will be integers.

        Calling `random.shuffle(P)` before using this function is strongly recommended.
    """

    lP = len(P)
    assert(lP > 0)

    if lP == 1: return (1, P[0], 0)

    stack = [tuple()] * (lP - 1)
    stack.append(None)
    stack_top = lP - 2

    Ca, Cp, Cr2 = 1, P[-1], 0

    while stack_top >= 0:
        D = stack[i := stack_top]; stack_top -= 1
        if D is None: continue

        Pi = P[i]

        dx, dy = Pi[0]*Ca-Cp[0], Pi[1]*Ca-Cp[1]
        if dx*dx + dy*dy <= Cr2: continue

        if len(D) == 2:
            Ca, Cp, Cr2 = circumcircle_of_triangle(Pi, D[0], D[1])
            continue
        D = D + (Pi,)

        stack[i] = None
        for j in range(i+1, lP): stack[j] = D
        stack_top = lP - 1
        
        if len(D) == 1:
            Ca, Cp, Cr2 = 1, Pi, 0
        else:
            ax, ay = D[0]; bx, by = Pi
            dx, dy = ax-bx, ay-by
            Ca, Cp, Cr2 = 2, (ax+bx, ay+by), dx*dx + dy*dy
    
    return (Ca, Cp, Cr2)