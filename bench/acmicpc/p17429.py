from ckp.data_structure.segment_tree.ring import NumberRingSegmentTree
from ckp.graph_theory.tree import tree_from_edges, random_tree_edges, tree_sizes
from ckp.graph_theory.tree.lca import tree_lca_init, tree_lca_query
from ckp.graph_theory.tree.euler_tour import euler_tour_sorted
from ckp.graph_theory.tree.hld import tree_hld_init, tree_hld_decompose_descendant

import random

N, Q = 500_000, 100_000
E = []
lQ = []

def setup():
    global E, lQ

    random.seed(42)
    E = random_tree_edges(N)
    
    lQ = []
    for _ in range(Q):
        q = random.randint(1, 6)
        match q:
            case 1: lQ.append((q, random.randrange(N), random.randrange(1, 1_000_000_000)))
            case 2: lQ.append((q, random.randrange(N), random.randrange(N), random.randrange(1, 1_000_000_000)))
            case 3: lQ.append((q, random.randrange(N), random.randrange(1, 1_000_000_000)))
            case 4: lQ.append((q, random.randrange(N), random.randrange(N), random.randrange(1, 1_000_000_000)))
            case 5: lQ.append((q, random.randrange(N)))
            case 6: lQ.append((q, random.randrange(N), random.randrange(N)))

def bench():
    T = tree_from_edges(E)
    sizes = tree_sizes(T)
    tour = euler_tour_sorted(T)
    hld = tree_hld_init(T)
    lca = tree_lca_init(T)

    V = NumberRingSegmentTree([0] * N)

    ans = 0
    return ans

    for (q, *args) in lQ:
        match q:
            case 1: pass
            case 2: pass
            case 3: pass
            case 4: pass
            case 5: pass
            case 6: pass

tags = {
    'hld', 'segment_tree', 'lazyprop', 'lca', 'euler_tour_technique'
}