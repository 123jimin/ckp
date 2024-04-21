from bench.util import bench
from ckp.data_structure.segment_tree.merge_sort import merge_sorted_lists

import random
random.seed(42)

X = [random.randint(0, 1_000_000_000) for _ in range(1_000_000)]
Y = [random.randint(0, 1_000_000_000) for _ in range(1_000_000)]

X.sort()
Y.sort()

def bench_naive():
    v = sorted(X+Y)
    assert(v[0] == 528)
    assert(v[500_000] == 250180108)
    assert(v[-1] == 999999978)
    return v

def bench_ckp():
    v = merge_sorted_lists(X, Y)
    assert(v[0] == 528)
    assert(v[500_000] == 250180108)
    assert(v[-1] == 999999978)
    return v

if __name__ == '__main__':
    bench([
        "bench_naive()",
        "bench_ckp()",
    ], num_trials=8, global_vars=globals())