class BipartiteGraphData:
    """ A bipartite graph where the set of vertices is U+V for non-intersecting U and V, and every edges connect U and V. """

    __slots__ = ('u_neighbors', 'v_neighbors')
    u_neighbors: list[list[int]]
    v_neighbors: list[list[int]]|None

    def __init__(self, u_neighbors: list[list[int]], v_neighbors: list[list[int]]|None = None):
        self.u_neighbors, self.v_neighbors = u_neighbors, v_neighbors

def bipartite_graph_from_neighbors(u_neighbors: list[list[int]], v_neighbors: list[list[int]]|None = None) -> BipartiteGraphData:
    return BipartiteGraphData(u_neighbors, v_neighbors)

def bipartite_graph_from_edges(edges: list[tuple[int, int]]) -> BipartiteGraphData:
    u_neighbors: list[list[int]] = []
    for u, v in edges:
        if len(u_neighbors) <= u: u_neighbors += [[] for _ in range(u+1 - len(u_neighbors))]
        u_neighbors[u].append(v)
    return BipartiteGraphData(u_neighbors)