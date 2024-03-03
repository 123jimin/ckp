from ckp.data_structure import SimpleSumSegmentTree

import random
N, M = 40_000, 40_000

random.seed(42)
ops = [(random.choice([0, 1]), *sorted((random.randrange(0, N), random.randrange(0, N)))) for _ in range(M)]

def bench():
    tree = SimpleSumSegmentTree([0] * N)
    ans = 0
    for (op, x, y) in ops:
        if op == 0:
            ans += tree.reduce_range(x, y)
        else:
            tree[x] += y
    assert ans == 1889273531508
    return ans

tags = {'segment_tree'}