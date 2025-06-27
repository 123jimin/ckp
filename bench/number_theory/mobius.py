from bench.util import bench

from ckp.number_theory.mobius import *

A = list(range(1_000_000, 1_100_000))

def bench_mobius_naive():
    for x in A: mobius_naive(x)

if __name__ == '__main__':
    bench([
        bench_mobius_naive
    ], num_trials=5)