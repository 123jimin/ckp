from bench.util import bench
from ckp.linear_algebra.matrix_mod import matrix_pow_mod

def matrix_id_flat(n: int):
    return [int(i == j) for i in range(n) for j in range(n)]

def matrix_mod_flat(x: list[int], m: int) -> list[list[int]]:
    return [e%m for e in x]

def matrix_mul_mod_flat(cx: int, x: list[int], cy: int, y: list[int], m: int) -> list[int]:
    # assert(len(x)%cx == 0)
    # assert(len(y) == cx*cy)
    return [
        sum(x[i+k]*y[k*cy+j] for k in range(cx)) % m
        for i in range(0, len(x), cx)
        for j in range(cy)
    ]

def matrix_pow_mod_flat(cx: int, x: list[int], k: int, m: int) -> list[int]:
    # assert(len(x) == cx**2)
    # assert(k >= 0)

    if k == 0: return matrix_id_flat(len(x))
    if k == 1: return matrix_mod_flat(x, m)

    k, d = divmod(k, 2)
    y = matrix_pow_mod_flat(cx, x, k, m)
    y = matrix_mul_mod_flat(cx, y, cx, y, m)

    if d: y = matrix_mul_mod_flat(cx, y, cx, x, m)
    return y

A = [[i+j for j in range(100)] for i in range(0, 10000, 100)]
B = list(range(10000))

def bench_matrix_pow_mod():
    C = matrix_pow_mod(A, 1_234_567_890, 1_000_000_009)
    x = sum(i*v for (i, v) in enumerate(C[0]))
    assert x == 2494948687891
    return x

def bench_matrix_pow_mod_flat():
    C = matrix_pow_mod_flat(100, B, 1_234_567_890, 1_000_000_009)
    x = sum(i*C[i] for i in range(100))
    assert x == 2494948687891
    return x

if __name__ == '__main__':
    bench([
        "bench_matrix_pow_mod_flat()",
        "bench_matrix_pow_mod()",
    ], num_trials=5, global_vars=globals())