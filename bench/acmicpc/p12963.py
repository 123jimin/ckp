from ckp.data_structure import disjoint_set_init, disjoint_set_find, disjoint_set_is_same_set, disjoint_set_union

import random
N, M = 250_000, 500_000
E = []

def setup():
    global E

    random.seed(42)
    E = [(random.randrange(N), random.randrange(N)) for _ in range(M)]

def bench():
    ds = disjoint_set_init(N)
    vx, vy = 0, N-1
    ans = 0

    for i in range(M):
        a, b = E[i]
        a = disjoint_set_find(ds, a)
        b = disjoint_set_find(ds, b)
        if a == b: continue
        if a == vx and b == vy or a == vy and b == vx:
            ans += i
            continue
        disjoint_set_union(ds, a, b)
        if a == vx or b == vx: vx = disjoint_set_find(ds, vx)
        if a == vy or b == vy: vy = disjoint_set_find(ds, vy)
    
    assert(ans == 1029314)
    return ans

tags = {'disjoint_set'}