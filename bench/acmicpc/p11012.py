from ckp.data_structure import Offline2DFenwickTree

import random
N, M = 10000, 50000

P = []
Q = []

def setup():
    global P, Q

    random.seed(42)
    P = [(random.randint(0, 100_000), random.randint(0, 100_000)) for _ in range(N)]
    
    for _ in range(M):
        x1, x2 = sorted((random.randint(0, 100_000), random.randint(0, 100_000)))
        y1, y2 = sorted((random.randint(0, 100_000), random.randint(0, 100_000)))
        Q.append((x1, x2+1, y1, y2+1))

def bench():
    tree = Offline2DFenwickTree(P)
    ans = sum(tree.sum_rect(*q) for q in Q)
    assert(ans == 55469479)
    return ans

tags = {'segment_tree'}