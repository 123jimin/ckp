from ckp.linear_algebra import matrix_mod, matrix_add_mod, matrix_mul_mod, matrix_pow_mod, matrix_id

import random
N = 20
A = [[random.randint(0, 1000) for _ in range(N)] for _ in range(N)]
B = 100_000_000_000

def pow_sum(A, B, M=1000):
    if B == 1: return matrix_mod(A, 1000)
    h, r = divmod(B, 2)
    S = pow_sum(A, h, M)
    S = matrix_mul_mod(S, matrix_add_mod(matrix_id(len(A)), matrix_pow_mod(A, h, M), M), M)
    if r: S = matrix_add_mod(S, matrix_pow_mod(A, B, M), M)
    return S

def bench():
    C = pow_sum(A, B)
    ans = sum(sum(row) for row in C)
    assert(ans == 199671)
    return ans

tags = {'matrix_multiplication'}