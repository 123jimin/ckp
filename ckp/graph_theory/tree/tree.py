class TreeData:
    """ Represents a tree. """
    __slots__ = ('root', 'children', 'parents', 'depths', 'sizes')

    root: int
    """ The root index of this tree. """

    children: list[list[int]]
    """ Children of each node. """

    parents: list[int]
    """ Parent node index of each node. `tree.parents[tree.root]` is -1. """

    depths: list[int]
    """ Depth of each node. `tree.depths[tree.root]` is 0. """

    sizes: list[int]|None
    """ Size of subtree of each node. This is not computed by default, and computed as needed via `tree_sizes`. """
    
    def __len__(self): return len(self.parents)
    def __repr__(self): return f"TreeData(parents={self.parents}, root={self.root})"

def tree_with_root(tree: TreeData, new_root: int) -> TreeData:
    """ Create a copy of the given tree with the specified root. """
    return tree_from_neighbors([
        (chs if p < 0 else chs + [p])
        for chs, p in zip(tree.children, tree.parents)
    ], new_root)

def tree_from_neighbors(neighbors: list[list[int]], root: int = 0) -> TreeData:
    """ Constructs a new tree from lists of neighbors. """
    tree = TreeData()
    tree.root = root
    tree.parents, tree.depths = tree_parents_and_depths_from_neighbors(neighbors, root)
    tree.children = [[ch for ch in n if ch != p] for (p, n) in zip(tree.parents, neighbors)]
    tree.sizes = None
    return tree

def tree_from_parents(parents: list[int], root: int = 0) -> TreeData:
    """ Constructs a new tree from lists of parents. `parents[root]` must be `-1`. """
    assert(parents[root] == -1)
    tree = TreeData()
    tree.root = root
    children = tree.children = [[] for _ in range(len(parents))]
    for i in range(len(parents)):
        if (p := parents[i]) >= 0: children[p].append(i)
    tree.parents = parents
    tree.depths = tree_depths_from_children(children, root)
    tree.sizes = None
    return tree

def tree_from_edges(edges: list[tuple[int, int]], root: int = 0) -> TreeData:
    """ Constructs a new tree from lists of undirected edges. Each edge must appear once. """
    neighbors = [[] for _ in range(len(edges)+1)]
    for (x, y) in edges: neighbors[x].append(y); neighbors[y].append(x)
    return tree_from_neighbors(neighbors, root)

def tree_depths_from_children(children: list[list[int]], root: int = 0) -> list[int]:
    """ Create a list D where D[i] is the distance of node i from the root. """
    depths = [0] * len(children)

    for ch in (stack := children[root].copy()):
        depths[ch] = 1
    
    stack_pop, stack_push = stack.pop, stack.append
    while stack:
        v = stack_pop()
        nd = depths[v] + 1
        for ch in children[v]:
            depths[ch] = nd
            if children[ch]: stack_push(ch)
        
    return depths


def tree_parents_and_depths_from_neighbors(neighbors: list[list[int]], root: int = 0) -> tuple[list[int], list[int]]:
    """ Create a list P, and D where P[i] is the parent of node i, and D[i] is the distance of node i from the root. P[root] is -1. """
    N = len(neighbors)

    parents = [-1] * N
    depths = [0] * N

    for ch in (stack := neighbors[root].copy()):
        parents[ch] = root
        depths[ch] = 1
    
    stack_pop, stack_push = stack.pop, stack.append
    while stack:
        v = stack_pop()
        p, nd = parents[v], depths[v]+1
        for ch in neighbors[v]:
            if ch == p: continue
            parents[ch] = v
            depths[ch] = nd
            if len(neighbors[ch]) > 1: stack_push(ch)
    
    return parents, depths

def tree_sizes_from_children(children: list[list[int]], root: int = 0) -> list[int]:
    """ Constructs a list S, where S[i] is the size of the subtree rooted at node i. """
    if not children: return []
    if not children[root]:
        assert(len(children) == 1)
        return [1]

    sizes = [0] * len(children)
    get_sizes = sizes.__getitem__

    stack = [(root, False)]
    stack.extend((ch, True) for ch in children[root])

    stack_pop, stack_push, stack_extend = stack.pop, stack.append, stack.extend
    while stack:
        v, p = stack_pop()
        if p:
            if (lch := children[v]):
                stack_push((v, False))
                stack_extend((ch, True) for ch in lch)
            else:
                sizes[v] = 1
        else:
            sizes[v] = 1+sum(map(get_sizes, children[v]))

    return sizes

def tree_sizes(tree: TreeData) -> list[int]:
    if tree.sizes: return tree.sizes
    sizes = tree.sizes = tree_sizes_from_children(tree.children, tree.root)
    return sizes

def tree_centroids_from_children(children: list[list[int]], root: int = 0, sizes: list[int]|None = None) -> list[int]:
    """
        Returns a list of centroids of the tree.
        A centroid of a tree is a point where all subtrees' sizes are <= len(neighbors) // 2.
        As long as the tree is not empty, there are either one or two centroids.
    """
    if not children: return []
    if not sizes: sizes = tree_sizes_from_children(children, root)

    half, r = divmod(len(children), 2)
    curr = 0
    while True:
        for ch in children[curr]:
            ch_size = sizes[ch]
            if (not r) and ch_size == half: return [curr, ch]
            elif ch_size > half:
                curr = ch
                break
        else:
            return [curr]

def tree_centroids(tree: TreeData) -> list[int]:
    """
        Returns a list of centroids of the tree.
        A centroid of a tree is a point where all subtrees' sizes are <= len(neighbors) // 2.
        As long as the tree is not empty, there are either one or two centroids.
    """
    return tree_centroids_from_children(tree.children, tree.root, tree_sizes(tree))

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
    tree.sizes = None

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