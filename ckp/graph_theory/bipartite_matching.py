from ckp.data_structure.graph.bipartite import BipartiteGraphData

class BipartiteMatchingData:
    __slots__ = ('size', 'u_pair', 'v_pair')

    size: int
    """ \\# of matched edges. """

    u_pair: list[int]
    """ Index of V-vertex matched by `u`, or `-1` if there's no match. """

    v_pair: list[int]
    """ Index of U-vertex matched by `v`, or `-1` if there's no match. """

    def __init__(self, size: int, u_pair: list[int], v_pair: list[int]):
        self.size, self.u_pair, self.v_pair = size, u_pair, v_pair

    def __len__(self) -> int: return self.size
    
    def __str__(self) -> str:
        return str([(u, v) for (u, v) in enumerate(self.u_pair) if v >= 0])

def assert_valid_bipartite_matching(graph: BipartiteGraphData, matching: BipartiteMatchingData) -> None:
    """ Checks whether a given matching is consistent. This function is for debugging CKP only. """
    assert len(matching.u_pair) == graph.U, f"{len(matching.u_pair)=} must be equal to {graph.U=}"
    assert len(matching.v_pair) == graph.V, f"{len(matching.v_pair)=} must be equal to {graph.V=}"
    assert matching.size <= min(graph.U, graph.V), f"{matching.size=} must not be greater than {min(graph.U, graph.V)=}"
    assert matching.size == sum(v >= 0 for v in matching.u_pair)
    assert matching.size == sum(u >= 0 for u in matching.v_pair)
    assert all(v < 0 or matching.v_pair[v] == u for (u, v) in enumerate(matching.u_pair))
    assert all(u < 0 or matching.u_pair[u] == v for (v, u) in enumerate(matching.v_pair))
    assert all(v < 0 or v in graph.u_neighbors[u] for (u, v) in enumerate(matching.u_pair))
    assert len(set(v for v in matching.u_pair if v >= 0)) == matching.size
    assert len(set(u for u in matching.v_pair if u >= 0)) == matching.size

def bipartite_matching(graph: BipartiteGraphData) -> BipartiteMatchingData:
    """
        Create a bipartite matching of the given graph, using the Hopkroft-Karp algorithm.
    """
    size = 0
    u_pair = [-1] * graph.U
    v_pair = [-1] * graph.V

    u_neighbors = graph.u_neighbors
    dist = [-1] * len(u_pair)
    while (dist_nil := _bipartite_matching_bfs(u_neighbors, u_pair, v_pair, dist)) >= 0:
        for u in range(len(u_pair)):
            if u_pair[u] < 0 and _bipartite_matching_dfs(u_neighbors, u_pair, v_pair, dist, dist_nil, u):
                size += 1
    
    return BipartiteMatchingData(size, u_pair, v_pair)

def _bipartite_matching_bfs(u_neighbors: list[list[int]], u_pair: list[int], v_pair: list[int], dist: list[int]) -> int:
    q = []
    for u in range(len(u_pair)):
        if u_pair[u] < 0:
            dist[u] = 0
            q.append(u)
        else:
            dist[u] = -1
    dist_nil = -1

    for u in q:
        if (du := dist[u]) < 0: continue
        if dist_nil >= 0 and du >= dist_nil: continue

        for v in u_neighbors[u]:
            if (vp := v_pair[v]) < 0:
                if dist_nil < 0: dist_nil = du+1
            elif dist[vp] < 0:
                dist[vp] = du+1
                q.append(vp)

    return dist_nil

def _bipartite_matching_dfs(u_neighbors: list[list[int]], u_pair: list[int], v_pair: list[int], dist: list[int], dist_nil: int, u: int) -> bool:
    if u < 0: return True
    
    for v in u_neighbors[u]:
        vp = v_pair[v]
        if dist[u]+1 == (dist_nil if vp < 0 else dist[vp]) and _bipartite_matching_dfs(u_neighbors, u_pair, v_pair, dist, dist_nil, vp):
            u_pair[u], v_pair[v] = v, u
            return True
    
    dist[u] = -1
    return False