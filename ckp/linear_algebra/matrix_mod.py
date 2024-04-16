"""
    Codes for performing matrix operations on Z/nZ for some n.
"""

from .matrix import matrix_id, matrix_equal

def column_vec_mod(x: list[int], m: int) -> list[list[int]]: return [[xe % m] for xe in x]

def matrix_mod(x: list[list[int]], m: int) -> list[list[int]]:
    return [[xe % m for xe in xr] for xr in x]

def matrix_imod(x: list[list[int]], m: int) -> list[list[int]]:
    for xr in x:
        for i in range(len(xr)): xr[i] %= m
    return x

def matrix_add_mod(x: list[list[int]], y: list[list[int]], m: int) -> list[list[int]]:
    return [[(xe+ye)%m for (xe, ye) in zip(xr, yr)] for (xr, yr) in zip(x, y)]

def matrix_iadd_mod(x: list[list[int]], y: list[list[int]], m: int) -> list[list[int]]:
    for (xr, yr) in zip(x, y):
        for i in range(len(xr)): xr[i] = (xr[i] + yr[i]) % m
    return x

def matrix_sub_mod(x: list[list[int]], y: list[list[int]], m: int) -> list[list[int]]:
    return [[(xe-ye)%m for (xe, ye) in zip(xr, yr)] for (xr, yr) in zip(x, y)]

def matrix_isub_mod(x: list[list[int]], y: list[list[int]], m: int) -> list[list[int]]:
    for (xr, yr) in zip(x, y):
        for i in range(len(xr)): xr[i] = (xr[i] - yr[i]) % m
    return x

def matrix_neg_mod(x: list[list[int]], m: int) -> list[list[int]]:
    return [[(-xe)%m for xe in xr] for xr in x]

def matrix_mul_mod(x: list[list[int]], y: list[list[int]], m: int) -> list[list[int]]:
    assert(0 < len(x[0]) == len(y))

    I, J, K = len(x), len(y), len(y[0])

    return [[sum(x[i][j]*y[j][k] for j in range(J))%m for k in range(K)] for i in range(I)]

def matrix_scalar_mul_mod(x: list[list[int]], k: int, m: int) -> list[list[int]]:
    return [[(k*xe)%m for xe in xr] for xr in x]

def matrix_scalar_imul_mod(x: list[list[int]], k: int, m: int) -> list[list[int]]:
    for xr in x:
        for i in range(len(xr)): xr[i] = (xr[i]*k) % m
    return x

def matrix_column_mul_mod(a: list[list[int]], v: list, m: int) -> list[int]:
    """ Computes Av, for a matrix and a column vector. """
    return [sum(aij*vj for (aij, vj) in zip(ai, v))%m for ai in a]

def matrix_pow_mod(x: list[list[int]], k: int, m: int) -> list[list[int]]:
    assert(0 <= len(x) == len(x[0]))
    assert(k >= 0)

    if k == 0: return matrix_id(len(x))
    if k == 1: return matrix_mod(x, m)

    k, d = divmod(k, 2)
    y = matrix_pow_mod(x, k, m)
    y = matrix_mul_mod(y, y, m)

    if d: y = matrix_mul_mod(y, x, m)
    return y