from ckp.data_structure import GCDSegmentTree, AddSegmentTree

import random, math
N, Q = 30_000, 50_000

random.seed(42)

init_values = [random.randint(1, 1000) for _ in range(N)]
ops = []

for _ in range(Q):
    a, b = random.randrange(0, N), random.randrange(0, N)
    if a > b: a, b = b, a
    match random.randrange(0, 10):
        case 0:
            ops.append((0, a, b))
        case 1:
            ops.append((0, a, min(a+random.randint(1, 10), b)))
        case _:
            ops.append((random.randint(0, 1000), a, b))

init_diffs = [0] * (N-1)
for i in range(N-1): init_diffs[i] = init_values[i+1] - init_values[i]

def bench():
    sum_tree = AddSegmentTree(init_values)
    diff_tree = GCDSegmentTree(init_diffs)

    ans = 0
    for (t, a ,b) in ops:
        if t == 0:
            g = diff_tree.sum_range(a, b)
            ans += math.gcd(g, sum_tree[a])
        else:
            sum_tree.add_to_range(a, b+1, t)
            if a: diff_tree[a-1] = diff_tree[a-1] + t
            if b < N-1: diff_tree[b] = diff_tree[b] - t
    
    assert ans == 11301
    return ans

tags = {'segment_tree', 'lazy_segment_tree'}