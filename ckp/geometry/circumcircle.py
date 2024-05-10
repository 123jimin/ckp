def _determinant(a, b, c, d, e, f, g, h, i): return a*(e*i-f*h) - b*(d*i-f*g) + c*(d*h-e*g)

def is_in_circumcircle(C: tuple[float, tuple[float, float], float], p: tuple[float, float]) -> bool:
    """
        Given a circumcircle (closed disc) returned by `circumcircle_of_*` functions, and a point p = (x, y), returns whether C contains p.
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

    ax, ay = a
    bx, by = b
    cx, cy = c

    Ca = _determinant(ax, ay, 1, bx, by, 1, cx, cy, 1)
    al, bl, cl = ax*ax+ay*ay, bx*bx+by*by, cx*cx+cy*cy

    Cb = _determinant(ax, ay, al, bx, by, bl, cx, cy, cl)
    Cx = _determinant(al, ay, 1, bl, by, 1, cl, cy, 1)
    Cy = _determinant(ax, al, 1, bx, bl, 1, cx, cl, 1)

    if Ca < 0: Ca, Cb, Cx, Cy = -Ca, -Cb, -Cx, -Cy

    return (2*Ca, (Cx, Cy), Cx*Cx+Cy*Cy + 4*Ca*Cb)

def _min_enclosing_circle_inner(P: list[tuple[float, float]], i: int, D: list[tuple[float, float]]) -> tuple[float, tuple[float, float], float]:
    if i == len(P):
        assert(1 <= len(D) <= 2)
        if len(D) == 1: return (1, D[0], 0)
        ax, ay = D[0]; bx, by = D[1]
        dx, dy = ax-bx, ay-by
        return (2, (ax+bx, ay+by), dx*dx + dy*dy)
    if len(D) == 0 and i == len(P)-1: return (1, P[i], 0)

    C = _min_enclosing_circle_inner(P, i+1, D)
    if is_in_circumcircle(C, P[i]): return C

    if len(D) == 2: return circumcircle_of_triangle(P[i], D[0], D[1])

    D.append(P[i])
    C = _min_enclosing_circle_inner(P, i+1, D)
    D.pop()

    return C

def min_enclosing_circle(P: list[tuple[float, float]]) -> tuple[float, tuple[float, float], float]:
    """
        Given a list of points P, returns the minimal enclosing circle C.
        C will be given as a format (Ca, Cp, Cr2), where, given that the circumcircle is centered at (x, y) with radius r:

        - Ca > 0
        - Cp = Ca * (x, y)
        - Cr2 = (Ca * r) ** 2

        When all points are integral points, then all Ca, Cp, Cr2 will be integers.
    """
    assert(len(P) > 0)
    return _min_enclosing_circle_inner(P, 0, [])