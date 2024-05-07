def _determinant(a, b, c, d, e, f, g, h, i): return a*(e*i-f*h) - b*(d*i-f*g) + c*(d*h-e*g)

def is_in_circumcircle(C: tuple[int|float, int|float, int|float], p: tuple[int|float, int|float]) -> bool:
    """
        Given a circumcircle (closed disc) returned by `circumcircle_of_*` functions, and a point p = (x, y), returns whether C contains p.
    """
    Ca, Cp, Cr2 = C
    dx = p[0]*Ca-Cp[0]
    dy = p[1]*Ca-Cp[1]
    return dx*dx + dy*dy <= Cr2

def circumcircle_of_triangle(D: list[tuple[int|float, int|float]]):
    """
        Given that the circumcircle of P is centered at (cx, cy) and r, returns (a, (a*cx, a*cy), (a*r)^2).
        When all points of P are integer points, then all three values will be integers.

        Note that `a` might be a negative number.
    """

    assert(len(D) <= 3)

    if len(D) == 1: return (1, D[0], 0)
    if len(D) == 2:
        ax, ay = D[0]
        bx, by = D[1]
        dx, dy = ax-bx, ay-by
        return (2, (ax+bx, ay+by), dx*dx + dy*dy)
    
    A, B, C = D
    ax, ay = A
    bx, by = B
    cx, cy = C
    
    a = _determinant(ax, ay, 1, bx, by, 1, cx, cy, 1)
    if a == 0: return circumcircle_of_triangle([min(D), max(D)])

    l2A, l2B, l2C = ax*ax+ay*ay, bx*bx+by*by, cx*cx+cy*cy
    b = _determinant(ax, ay, l2A, bx, by, l2B, cx, cy, l2C)
    Sx = _determinant(l2A, ay, 1, l2B, by, 1, l2C, cy, 1)
    Sy = _determinant(ax, l2A, 1, bx, l2B, 1, cx, l2C, 1)
    return (2*a, (Sx, Sy), Sx*Sx+Sy*Sy + 4*a*b)

def _min_enclosing_circle_inner(P: list[tuple[int|float, int|float]], i: int, D: list[tuple[int|float, int|float]]) -> tuple[int|float, int|float, int|float]:
    if i == len(P) or len(D) == 3: return circumcircle_of_triangle(D)
    if len(D) == 0 and i+1 >= len(P): return circumcircle_of_triangle(P[i:])

    C = _min_enclosing_circle_inner(P, i+1, D)
    if is_in_circumcircle(C, P[i]): return C

    D.append(P[i])
    C = _min_enclosing_circle_inner(P, i+1, D)
    D.pop()

    return C

def min_enclosing_circle(P: list[tuple[int|float, int|float]]):
    """
        Given that the circumcircle of P is centered at (cx, cy) and r, returns (a, (a*cx, a*cy), (a*r)^2).
        When all points of P are integer points, then all three values will be integers.
        
        Note that `a` might be a negative number.
    """
    return _min_enclosing_circle_inner(P, 0, [])