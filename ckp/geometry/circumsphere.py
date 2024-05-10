from .vector import vec3_add, vec3_sub, vec3_scalar_mul, vec3_dot, vec3_cross, vec3_dist_sq
from math import sqrt

def is_in_circumsphere(C: tuple[float, tuple[float, float, float], float], p: tuple[float, float, float]) -> bool:
    """
        Given a sphere (closed ball) `C` returned by `circumcircle_of_tetrahedron` or `min_enclosing_sphere`, and a point p = (x, y, z), returns whether `C` contains `p`.
    """
    Ca, Cp, Cr2 = C
    dx, dy, dz = p[0]*Ca-Cp[0], p[1]*Ca-Cp[1], p[2]*Ca-Cp[2]
    return dx*dx + dy*dy + dz*dz <= Cr2

def _determinant_4(a: tuple[float, float, float, float], b: tuple[float, float, float, float], c: tuple[float, float, float, float], d: tuple[float, float, float, float]) -> float:
    a1, a2, a3, a4 = a; b1, b2, b3, b4 = b; c1, c2, c3, c4 = c; d1, d2, d3, d4 = d

    return (
        a1 * (b2 * (c3 * d4 - c4 * d3) - b3 * (c2 * d4 - c4 * d2) + b4 * (c2 * d3 - c3 * d2))
        - a2 * (b1 * (c3 * d4 - c4 * d3) - b3 * (c1 * d4 - c4 * d1) + b4 * (c1 * d3 - c3 * d1))
        + a3 * (b1 * (c2 * d4 - c4 * d2) - b2 * (c1 * d4 - c4 * d1) + b4 * (c1 * d2 - c2 * d1))
        - a4 * (b1 * (c2 * d3 - c3 * d2) - b2 * (c1 * d3 - c3 * d1) + b3 * (c1 * d2 - c2 * d1))
    )

def circumsphere_of_segment(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, tuple[float, float, float], float]:
    return (2, (a[0]+b[0], a[1]+b[1], a[2]+b[2]), vec3_dist_sq(a, b))

def min_enclosing_sphere_of_triangle(a: tuple[float, float, float], b: tuple[float, float, float], c: tuple[float, float, float]) -> tuple[float, tuple[float, float, float], float]:
    al = vec3_dist_sq(b, c); bl = vec3_dist_sq(c, a); cl = vec3_dist_sq(a, b)
    if al >= bl:
        if al >= cl: pass
        else: al, cl, a, c = cl, al, c, a
    elif bl >= cl: al, bl, a, b = bl, al, b, a
    else: al, cl, a, c = cl, al, c, a
    
    if al >= bl+cl: return circumsphere_of_segment(b, c)
    
    cos_a = (bl+cl-al) / (2*sqrt(bl*cl))
    r2 = al / (4*(1-cos_a*cos_a))
    
    alpha = (a[0]-c[0], a[1]-c[1], a[2]-c[2])
    beta = (b[0]-c[0], b[1]-c[1], b[2]-c[2])
    gamma = vec3_cross(alpha, beta)
    p = vec3_add(vec3_scalar_mul(vec3_cross(
        vec3_sub(vec3_scalar_mul(beta, vec3_dot(alpha, alpha)), vec3_scalar_mul(alpha, vec3_dot(beta, beta))),
        gamma
    ), 1/(2*vec3_dot(gamma, gamma))), c)
    
    return (1, p, r2)
        
def circumsphere_of_tetrahedron(a: tuple[float, float,  float], b: tuple[float, float,  float], c: tuple[float, float,  float], d: tuple[float, float,  float]) -> tuple[float, tuple[float, float, float], float]:
    ax, ay, az = a; al = ax*ax + ay*ay + az*az
    bx, by, bz = b; bl = bx*bx + by*by + bz*bz
    cx, cy, cz = c; cl = cx*cx + cy*cy + cz*cz
    dx, dy, dz = d; dl = dx*dx + dy*dy + dz*dz
    xs = (ax, bx, cx, dx)
    ys = (ay, by, cy, dy)
    zs = (az, bz, cz, dz)
    ls = (al, bl, cl, dl)
    us = (1, 1, 1, 1)

    Ca = _determinant_4(xs, ys, zs, us)
    Cb = _determinant_4(xs, ys, zs, ls)

    Cx = _determinant_4(ls, ys, zs, us)
    Cy = _determinant_4(xs, ls, zs, us)
    Cz = _determinant_4(xs, ys, ls, us)

    if Ca < 0: Ca, Cb, Cx, Cy, Cz = -Ca, -Cb, -Cx, -Cy, -Cz
    return (2*Ca, (Cx, Cy, Cz), Cx*Cx + Cy*Cy + Cz*Cz + 4*Ca*Cb)