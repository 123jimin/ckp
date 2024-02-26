from bench.util import bench
from ckp.number_theory.primality_test import is_prime_naive

def bench_is_prime_naive():
    x = sum(is_prime_naive(i) for i in range(3_000_001, 6_000_000, 30))
    assert x == 24473
    return x

if __name__ == '__main__':
    bench([
        "bench_is_prime_naive()",
    ], num_trials=8, global_vars=globals())