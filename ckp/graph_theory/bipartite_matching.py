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
    """ Create a bipartite matching of the given graph, using the Hopkroft-Karp algorithm. """
    U, V = graph.U, graph.V
    W = min(U, V)
    
    size = 0
    u_pair = [-1] * U
    v_pair = [-1] * V
    u_neighbors = graph.u_neighbors

    dist = [-1] * U
    q_append = (q := []).append

    ## Step 0: First BFS+DFS step. ##
    for u in range(U):
        for v in u_neighbors[u]:
            if v_pair[v] < 0:
                u_pair[u], v_pair[v] = v, u
                size += 1
                break
        else:
            dist[u] = 0
            q_append(u)

    while size < W:
        ## Step 1: BFS to find shortest augmenting paths. ##        
        aug_not_found = True
        dist_nil = 1

        while aug_not_found:
            q_append = (nq := []).append

            for u in q:
                for v in u_neighbors[u]:
                    if (vp := v_pair[v]) < 0:
                        aug_not_found = False
                    elif dist[vp] == -1:
                        dist[vp] = dist_nil
                        q_append(vp)

            if aug_not_found and nq:
                q = nq; dist_nil += 1
            else:
                break

        if aug_not_found: break

        ## Step 2: DFS to flip augmenting paths, and prepare for next BFS. ##
        u_parent = [-2] * U
        v_parent = [-1] * V
        next_dist = [-1] * U
        q_append = (q := []).append

        for root in range(U):
            if u_pair[root] >= 0: continue

            u_parent[root] = -1
            stack = [root]; stack_pop, stack_push = stack.pop, stack.append

            while stack:
                ndu = dist[u := stack_pop()] + 1
                for v in u_neighbors[u]:
                    if v_parent[v] >= 0: continue

                    if (vp := v_pair[v]) < 0:
                        if ndu != dist_nil: continue
                        v_parent[v] = u
                        while v >= 0:
                            nv = u_pair[u := v_parent[v]]
                            u_pair[u], v_pair[v] = v, u
                            v = nv
                        size += 1
                        stack = []
                        break
                    else:
                        if ndu != dist[vp]: continue
                        v_parent[v] = u
                        if u_parent[vp] == -2:
                            u_parent[vp] = v
                            stack_push(vp)
            
            if u_pair[root] < 0:
                next_dist[root] = 0
                q_append(root)
        
        dist = next_dist

    return BipartiteMatchingData(size, u_pair, v_pair)