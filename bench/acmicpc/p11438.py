from ckp.graph_theory.tree import tree_from_parents, tree_lca_init, tree_lca_query

import random
N, M = 100_000, 100_000

tree_parents = []
lca_queries = []
tree = None

def setup():
    global tree_parents, lca_queries, tree

    random.seed(42)
    tree_parents = [(random.randrange(i) if i else -1) for i in range(N)]
    lca_queries = [(random.randrange(N), random.randrange(N)) for _ in range(M)]

    tree = tree_from_parents(tree_parents)

def bench():
    tree_lca = tree_lca_init(tree)
    v = sum(tree_lca_query(tree_lca, x, y) for x, y in lca_queries)
    assert(v == 997884)

    return v

tags = {'tree', 'lca'}