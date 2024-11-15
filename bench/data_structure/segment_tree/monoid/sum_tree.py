from bench.util import bench
from ckp.data_structure.segment_tree import MonoidSumSegmentTree, SumSegmentTree

from random import seed, randrange
seed(42)

N = 100_000
data = [randrange(500) for _ in range(N)]
sum_indices = [(i, j) for (i, j) in ((randrange(N), randrange(N)) for _ in range(N)) if i < j]

sum_tree = SumSegmentTree(data)

def bench_sum(tree):
    ans = sum(tree.sum_range(i, j) for (i, j) in sum_indices)
    assert(ans == 416647779345)
    return ans

if __name__ == "__main__":
    bench([
        "bench_sum(sum_tree)",
    ], num_trials=8, global_vars=globals())