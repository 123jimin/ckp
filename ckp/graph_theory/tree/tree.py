class TreeData:
    """ Represents a tree. """
    __slots__ = ('root', 'parents', 'children', 'depths', 'sizes')

    root: int
    """ The root index of this tree. """

    parents: list[int]
    """ Parent node index of each node. `tree.parents[tree.root]` is -1. """

    children: list[list[int]]
    """ Children of each node. """

    depths: list[int]
    """ Depth of each node. `tree.depths[tree.root]` is 0. """

    sizes: list[int]|None
    """ Size of subtree of each node. This is not computed by default, and computed as needed via `tree_sizes`. """
    
    def __len__(self): return len(self.parents)
    def __repr__(self): return f"TreeData(parents={self.parents}, root={self.root})"

def assert_valid_tree(tree: TreeData) -> None:
    """ Checks whether a given tree is consistent. This function is for debugging CKP only. """
    N = len(tree)
    assert N > 0, f"len(tree) must be greater than zero"
    assert N == len(tree.parents), f"len(tree)={N} must be equal to {len(tree.parents)=}"
    assert N == len(tree.children), f"len(tree)={N} must be equal to {len(tree.children)=}"
    assert N == len(tree.depths), f"len(tree)={N} must be equal to {len(tree.depths)=}"

    root = tree.root
    assert 0 <= root < N, f"tree.root={root} must be in [0, len(tree)={N})"
    assert tree.parents[root] == -1, f"{tree.parents[root]=} must be -1"
    assert tree.depths[root] == 0, f"{tree.depths[root]=} must be 0"

    visited = [False] * N
    stack = [root]
    visited[root] = True

    while stack:
        v = stack.pop()
        for ch in tree.children[v]:
            assert 0 <= ch < N, f"tree.children[{v=}] has out-of-bound child {ch=}"
            assert ch != v, f"{v=} has itself as a child"
            assert tree.parents[ch] == v, f"parent inconsistency between {v=} and {ch=}"
            assert tree.depths[ch] == tree.depths[v]+1, f"depth inconsistency between {v=} and {ch=}"
            assert not visited[ch], f"{ch=} appears multiple times"
            visited[ch] = True
            stack.append(ch)

    assert all(visited), f"some nodes are unreachable"

    if tree.sizes is not None:
        assert N == len(tree.sizes), f"len(tree)={N} must be equal to {len(tree.sizes)=}"
        assert N == tree.sizes[root], f"len(tree)={N} must be equal to {tree.sizes[root]=}"

        for v in range(N):
            assert 1 <= tree.sizes[v] <= N, f"{tree.sizes[v]=} out of range"
            assert tree.sizes[v] == 1 + sum(tree.sizes[ch] for ch in tree.children[v]), f"size inconsistency for {v=}"

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
    children = tree.children = [[] for _ in parents]
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
    """ Retrieves the list of subtrees of the tree, which is cached to the provided `tree`. """
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

