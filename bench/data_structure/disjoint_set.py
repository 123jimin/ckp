from bench.util import bench
from ckp.data_structure.disjoint_set import DisjointSetData, DisjointSet, disjoint_set_size, disjoint_set_find, disjoint_set_is_same_set, disjoint_set_union

def disjoint_set_union_mod(ds: DisjointSetData, x: int, y: int) -> tuple[int, int]|None:
    parents = ds.parents

    # x = disjoint_set_find(ds, x)
    ox, orx = x, parents[x]
    if ox != orx:
        x = orx
        while (rx := parents[x]) != x: x = rx
        if orx != rx: parents[ox] = rx

    # y = disjoint_set_find(ds, y)
    oy, ory = y, parents[y]
    if oy != ory:
        y = ory
        while (ry := parents[y]) != y: y = ry
        if ory != ry: parents[oy] = ry
    
    # Processes union.
    if x == y: return False

    sizes, ranks = ds.sizes, ds.ranks
    if ranks[x] < ranks[y]: x, y = y, x

    parents[y] = x; sizes[x] += sizes[y]
    if ranks[x] == ranks[y]: ranks[x] += 1

    return True

class DisjointSetMod(DisjointSetData):
    def __init__(self, size: int):
        self.parents, self.sizes, self.ranks = list(range(size)), [1] * size, [0] * size

    size = disjoint_set_size
    find = disjoint_set_find
    is_same_set = disjoint_set_is_same_set
    union = disjoint_set_union_mod

import random
random.seed(42)

N = 1000000
E = [(i+1, i) for i in range(N-1)]

def bench_prev():
    ds = DisjointSet(N)

    for (i, j) in E: ds.union(i, j)
    return i + j

def bench_next():
    ds = DisjointSetMod(N)

    for (i, j) in E: ds.union(i, j)
    return i + j

import cProfile

if __name__ == '__main__':
    bench([
        "bench_prev()",
        "bench_next()",
    ], num_trials=8, global_vars=globals())