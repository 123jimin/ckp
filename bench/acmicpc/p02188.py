from ckp.data_structure.graph import bipartite_graph_from_neighbors
from ckp.graph_theory.bipartite_matching import bipartite_matching
import random

N = 3000
p = 0.5
neighbors = []

def setup():
    global neighbors

    random.seed(42)
    neighbors = [[v for v in range(N) if random.random() < p] for u in range(N)]

def bench():
    graph = bipartite_graph_from_neighbors(N, N, neighbors)
    ans = len(bipartite_matching(graph))
    
    assert(ans == N)
    return ans

tags = {'bipartite_matching'}