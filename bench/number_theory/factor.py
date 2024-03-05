from bench.util import bench
from ckp.number_theory.factor import *

def bench_find_divisor():
    # A random prime number, chosen by a fair dice roll.
    p = 1854622803871
    x = pollard_rho_find_divisor(p ** 2)
    assert x == p
    return x

def bench_factor():
    x = sum(max(factor_pollard_rho(r)) for r in range(1_000_000_000, 1_000_010_000))
    assert x == 823444990958
    return x

if __name__ == '__main__':
    bench([
        "bench_find_divisor()",
    ], num_trials=5, global_vars=globals())