from ckp.geometry import min_enclosing_circle, Vec2
from ckp.geometry.circumcircle import _determinant

import random, sys, math
sys.setrecursionlimit(10_000_000)
N = 100000

random.seed(42)
points = [(random.randint(-30000, 30000), random.randint(-30000, 30000)) for _ in range(N)]

def bench_orig():
    a, (acx, acy), acr = min_enclosing_circle(points)

    assert(abs(acx/a - 163.008313) < 0.001)
    assert(abs(acy/a - 54.380628) < 0.001)
    assert(abs(math.sqrt(acr/a/a) - 42263.568380) < 0.001)
    
    return a, acr

points_vec = [Vec2(x, y) for (x, y) in points]

def is_in_circumcircle_vec(C: tuple[int|float, Vec2, int|float], p: Vec2) -> bool:
    """
        Given a circumcircle (closed disc) `C` returned by `circumcircle_of_*` functions and a point `p`, returns whether `C` contains `p`.
    """
    Ca, Cp, Cr2 = C
    return (Ca*p - Cp).norm_sq() <= Cr2

def circumcircle_of_triangle_vec(D: list[Vec2]) -> tuple[float, Vec2, float]:
    """
        Given that the circumcircle of `D` is centered at (cx, cy) and r, returns (a, (a*cx, a*cy), (a*r)^2).
        When all points of `D` are integer points, then all three values will be integers.

        Note that `a` might be a negative number.
    """

    assert(len(D) <= 3)

    if len(D) == 1: return (1, D[0], 0)
    if len(D) == 2:
        A, B = D
        return (2, A + B, (B-A).norm_sq())
    
    A, B, C = D

    a = _determinant(A.x, A.y, 1, B.x, B.y, 1, C.x, C.y, 1)
    if a == 0: return circumcircle_of_triangle_vec([min(D), max(D)])

    l2A, l2B, l2C = A.norm_sq(), B.norm_sq(), C.norm_sq()
    b = _determinant(A.x, A.y, l2A, B.x, B.y, l2B, C.x, C.y, l2C)
    Sx = _determinant(l2A, A.y, 1, l2B, B.y, 1, l2C, C.y, 1)
    Sy = _determinant(A.x, l2A, 1, B.x, l2B, 1, C.x, l2C, 1)
    return (2*a, Vec2(Sx, Sy), Sx*Sx+Sy*Sy + 4*a*b)

def _min_enclosing_circle_inner_vec(P: list[Vec2], i: int, D: list[Vec2]) -> tuple[float, Vec2, float]:
    if i == len(P) or len(D) == 3: return circumcircle_of_triangle_vec(D)
    if len(D) == 0 and i+1 >= len(P): return circumcircle_of_triangle_vec(P[i:])

    C = _min_enclosing_circle_inner_vec(P, i+1, D)
    if is_in_circumcircle_vec(C, P[i]): return C

    D.append(P[i])
    C = _min_enclosing_circle_inner_vec(P, i+1, D)
    D.pop()

    return C

def min_enclosing_circle_vec(P: list[Vec2]):
    """
        Given that the circumcircle of P is centered at (cx, cy) and r, returns (a, (a*cx, a*cy), (a*r)^2).
        When all points of P are integer points, then all three values will be integers.
        
        Note that `a` might be a negative number.
    """
    return _min_enclosing_circle_inner_vec(P, 0, [])

def bench_vec2():
    a, (acx, acy), acr = min_enclosing_circle_vec(points_vec)

    assert(abs(acx/a - 163.008313) < 0.001)
    assert(abs(acy/a - 54.380628) < 0.001)
    assert(abs(math.sqrt(acr/a/a) - 42263.568380) < 0.001)
    
    return a, acr

bench = bench_orig

tags = ['geometry', 'min_enclosing_circle']