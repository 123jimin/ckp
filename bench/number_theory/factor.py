from bench.util import bench
from ckp.number_theory.factor import *

def bench_factor():
    x = sum(max(factor(r)) for r in range(1_000_000_000, 1_000_010_000))
    assert x == 823444990958
    return x

if __name__ == '__main__':
    bench([
        "bench_factor()",
    ], num_trials=5, global_vars=globals())