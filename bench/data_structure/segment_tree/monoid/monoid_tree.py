from bench.util import bench
from ckp.data_structure.segment_tree import LazySumSegmentTree, NumberSegmentTree
from test.data_structure.segment_tree.util.data_generator import TestDataGenerator

import random
random.seed(42)

N, Q = 1000, 10_000
data_gen = TestDataGenerator(N, ['get', 'sum_range', 'sum_range', 'set', 'add_to_range', 'add_to_range'], lambda: random.randint(-100, 100))
init_values = data_gen.list()
ops = [data_gen.op() for _ in range(Q)]

def bench_lazy():
    TestDataGenerator.bench(LazySumSegmentTree(init_values), ops)

def bench_number():
    TestDataGenerator.bench(NumberSegmentTree(init_values), ops)

if __name__ == "__main__":
    bench([
        bench_lazy, bench_number,
    ], num_trials=10)