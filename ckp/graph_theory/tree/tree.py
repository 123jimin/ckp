class TreeData:
    """ Represents a tree. """
    __slots__ = ('root', 'neighbors', 'parents', 'depths')

    root: int
    """ The root index of this tree. """

    neighbors: list[list[int]]
    """ Neighbor list of each node. """
    
    parents: list[int]
    """ Parent node index of each node. `tree.parents[tree.root]` is -1. """

    depths: list[int]
    """ Depth of each node. `tree.depths[tree.root]` is 0. """
    
    def __len__(self): return len(self.parents)
    def __repr__(self): return f"TreeData(parents={self.parents}, root={self.root})"

def tree_from_neighbors(neighbors: list[list[int]], root: int = 0) -> TreeData:
    """ Constructs a new tree from lists of neighbors. """
    tree = TreeData()
    tree.root = root
    tree.neighbors = neighbors = neighbors
    tree.parents, tree.depths = tree_parents_and_depths(neighbors, root)
    return tree

def tree_from_parents(parents: list[int], root: int = 0) -> TreeData:
    """ Constructs a new tree from lists of parents. `parents[root]` must be `-1`. """
    assert(parents[root] == -1)
    tree = TreeData()
    tree.root = root
    neighbors = tree.neighbors = [[] for _ in range(len(parents))]
    for i in range(len(parents)):
        if (p := parents[i]) >= 0: neighbors[p].append(i); neighbors[i].append(p)
    tree.parents = parents
    _, tree.depths = tree_parents_and_depths(neighbors, root)
    return tree

def tree_from_edges(edges: list[tuple[int, int]], root: int = 0) -> TreeData:
    """ Constructs a new tree from lists of undirected edges. Each edge must appear once. """
    neighbors = [list[int]() for _ in range(len(edges)+1)]
    for (x, y) in edges: neighbors[x].append(y); neighbors[y].append(x)
    return tree_from_neighbors(neighbors, root)

def _tree_parents_and_depths_dfs(neighbors: list[list[int]], parents: list[int], depths: list[int], depth: int, curr: int, parent: int = -1):
    parents[curr] = parent
    depths[curr] = depth
    for ch in neighbors[curr]:
        if ch != parent: _tree_parents_and_depths_dfs(neighbors, parents,depths, depth+1, ch, curr)

def tree_parents_and_depths(neighbors: list[list[int]], root_ind: int = 0) -> tuple[list[int], list[int]]:
    """ Create a list P, and D where P[i] is the parent of node i, and D[i] is the distance of node i from root. P[root_ind] is -1. """
    N = len(neighbors)

    parents = [-1] * N
    depths = [0] * N

    _tree_parents_and_depths_dfs(neighbors, parents, depths, 0, root_ind)

    return parents, depths

def tree_sizes(neighbors: list[list[int]], root_ind: int = 0) -> list[int]:
    """ Constructs a list S, where S[i] is the size of the subtree rooted at node i. """
    if not neighbors: return []
    if not neighbors[root_ind]:
        assert(len(neighbors) == 1)
        return [1]

    sizes = [0] * len(neighbors)
    get_sizes = sizes.__getitem__
    
    stack = [(root_ind, -1)]
    stack.extend((ch, root_ind) for ch in neighbors[root_ind])

    while stack:
        v, p = stack.pop()
        if p >= 0:
            lch = neighbors[v]
            if len(lch) == 1:
                sizes[v] = 1
                continue

            stack.append((v, -1))
            stack.extend((ch, v) for ch in lch if ch != p)
        else:
            # No need to check for parents.
            sizes[v] = 1+sum(map(get_sizes, neighbors[v]))

    return sizes

def tree_centroids(neighbors: list[list[int]]|TreeData, sizes: list[int]|None = None) -> list[int]:
    """
        Returns a list of centroids of the tree.
        A centroid of a tree is a point where all subtrees' sizes are <= len(neighbors) // 2.
        As long as the tree is not empty, there are either one or two centroids.
    """
    if not neighbors: return []
    if isinstance(neighbors, TreeData): neighbors = neighbors.neighbors
    if not sizes: sizes = tree_sizes(neighbors)

    half, r = divmod(len(neighbors), 2)
    curr, parent = 0, -1
    while True:
        for ch in neighbors[curr]:
            if ch == parent: continue
            ch_size = sizes[ch]
            if (not r) and ch_size == half: return [curr, ch]
            elif ch_size > half:
                curr, parent = ch, curr
                break
        else:
            return [curr]

class DistanceTreeData(TreeData):
    """ Represents a tree, where each edge has length. """
    __slots__ = ('distances', 'parent_distances', 'root_distances')

    distances: list[list[int]]

    parent_distances: list[int]
    root_distances: list[int]

def _distance_tree_init_dfs(tree: DistanceTreeData, depth: int, root_distance: int, curr: int, parent: int = -1):
    tree.parents[curr] = parent
    tree.depths[curr] = depth
    tree.root_distances[curr] = root_distance
    parent_distances = tree.parent_distances

    for (ch, d) in zip(tree.neighbors[curr], tree.distances[curr]):
        if ch == parent: continue

        parent_distances[ch] = d
        _distance_tree_init_dfs(tree, depth+1, root_distance+d, ch, curr)

def distance_tree_init(neighbors: list[list[int]], distances: list[list[int]], root: int = 0) -> DistanceTreeData:
    tree = DistanceTreeData()
    tree.root = root
    tree.neighbors = neighbors
    tree.distances = distances

    N = len(neighbors)
    tree.parents = [-1] * N
    tree.depths = [0] * N
    tree.parent_distances = [0] * N
    tree.root_distances = [0] * N

    _distance_tree_init_dfs(tree, 0, 0, root)
    return tree

def distance_tree_from_edges(edges: list[tuple[int, int, int]], root: int = 0) -> DistanceTreeData:
    neighbors = [[] for _ in range(len(edges)+1)]
    distances = [[] for _ in range(len(edges)+1)]
    for (x, y, d) in edges:
        assert(x != y)
        neighbors[x].append(y); neighbors[y].append(x)
        distances[x].append(d); distances[y].append(d)

    return distance_tree_init(neighbors, distances, root)