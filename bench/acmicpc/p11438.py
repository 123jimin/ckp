from ckp.graph_theory.tree import Tree, TreeLCA

import random, math
N, M = 100_000, 100_000

random.seed(42)

tree_parents = [(random.randrange(i) if i else -1) for i in range(N)]
lca_queries = [(random.randrange(N), random.randrange(N)) for _ in range(M)]

tree = Tree(parents=tree_parents)

def bench():
    tree_lca = TreeLCA(tree)
    v = sum(tree_lca.get(x, y) for x, y in lca_queries)
    assert(v == 997884)

    return v

tags = {'tree', 'lca'}