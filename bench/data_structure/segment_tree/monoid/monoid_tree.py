from bench.util import bench
from ckp.data_structure.segment_tree import NumberSegmentTree, FastNumberSegmentTree
from test.data_structure.segment_tree.util.data_generator import TestDataGenerator

import random, cProfile
random.seed(42)

N, Q = 10_000, 10_000
data_gen = TestDataGenerator(N, ['get', 'sum_range', 'sum_range', 'set', 'add_to_range', 'add_to_range'], lambda: random.randint(-100, 100))
init_values = data_gen.list()
ops = [data_gen.op() for _ in range(Q)]

def bench_default():
    res = TestDataGenerator.bench(NumberSegmentTree(init_values), ops)
    assert(sum(res) == 10793641679)

def bench_fast():
    res = TestDataGenerator.bench(FastNumberSegmentTree(init_values), ops)
    assert(sum(res) == 10793641679)

if __name__ == "__main__":
    bench([
        bench_default,
        bench_fast,
    ], num_trials=10)
    
    cProfile.runctx("for _ in range(10): f()", {'f': bench_fast}, {}, sort='tottime')