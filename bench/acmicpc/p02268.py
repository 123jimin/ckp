from ckp.data_structure import SumSegmentTree

import random
N, M = 150_000, 150_000

random.seed(42)
ops = [(random.choice([0, 1]), *sorted((random.randrange(0, N), random.randrange(0, N)))) for _ in range(M)]

def bench():
    tree = SumSegmentTree([0] * N)
    ans = 0
    for (op, x, y) in ops:
        if op == 0:
            ans += tree.sum_range(x, y)
        else:
            tree[x] += y
    assert ans == 98309415998492
    return ans

tags = {'segment_tree'}