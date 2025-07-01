from itertools import repeat

class BipartiteGraphData:
    """
        A bipartite graph where the set of vertices is U+V for non-intersecting U and V, and every edges connect U and V.

        It's possible that `v_neighbors` is not given.
    """

    __slots__ = ('U', 'V', 'u_neighbors', 'v_neighbors')
    U: int
    V: int
    u_neighbors: list[list[int]]
    v_neighbors: list[list[int]]|None

    def __init__(self, U: int, V: int, u_neighbors: list[list[int]], v_neighbors: list[list[int]]|None = None):
        self.U, self.V, self.u_neighbors, self.v_neighbors = U, V, u_neighbors, v_neighbors

def bipartite_graph_from_neighbors(U: int, V: int, u_neighbors: list[list[int]], v_neighbors: list[list[int]]|None = None) -> BipartiteGraphData:
    return BipartiteGraphData(U, V, u_neighbors, v_neighbors)

def bipartite_graph_from_edges(U: int, V: int, edges: list[tuple[int, int]]|None = None):
    u_neighbors: list[list[int]] = [[] for _ in repeat(None, U)]
    v_neighbors: list[list[int]] = [[] for _ in repeat(None, V)]

    for u, v in edges:
        u_neighbors[u].append(v)
        v_neighbors[v].append(u)

    return BipartiteGraphData(U, V, u_neighbors, v_neighbors)