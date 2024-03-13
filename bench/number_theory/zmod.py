from bench.util import bench
from ckp.number_theory import ZMod

def bench_normal():
    i = 2
    while i != 1:
        i = (i * 2) % 47360503
    return i

def bench_zmod():
    i = ZMod(2, 47360503)
    while i != 1: i *= 2
    return i

if __name__ == '__main__':
    bench([
        "bench_normal()",
        "bench_zmod()",
    ], num_trials=8, global_vars=globals())