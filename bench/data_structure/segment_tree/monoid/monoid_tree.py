from bench.util import bench
from ckp.data_structure.segment_tree import LazySumSegmentTree, NumberSegmentTree
from test.data_structure.segment_tree.util.data_generator import TestDataGenerator

import random
random.seed(42)

N, Q = 100_000, 100_000
data_gen = TestDataGenerator(100_000, ['get', 'sum_range', 'sum_range', 'set', 'add_to_range', 'add_to_range'], lambda: random.randint(-100, 100))
init_values = data_gen.list()
ops = [data_gen.op() for _ in range(Q)]

def bench_tree(tree):
    ans = 0
    for op in ops:
        match op:
            case ('get', i): ans += tree[i]
            case ('sum_range', i, j): ans += tree.sum_range(i, j)
            case ('set', i, v): tree[i] = v
            case ('add_to_range', i, j, v): tree.add_to_range(i, j, v)
    assert(ans == 3240201523773)

def bench_lazy():
    bench_tree(LazySumSegmentTree(init_values))

def bench_number():
    bench_tree(NumberSegmentTree(init_values))

if __name__ == "__main__":
    bench([
        bench_lazy, bench_number,
    ], num_trials=10)