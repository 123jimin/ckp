from .tree import TreeData, assert_valid_tree

# TODO: add tests for DistanceTreeData
class DistanceTreeData(TreeData):
    """ Represents a tree, where each edge has length. """
    __slots__ = ('distances', 'parent_distances', 'root_distances')

    distances: list[list[int]]
    """ Distances to each children. """

    parent_distances: list[int]
    """ Distance to the parent node. """

    root_distances: list[int]
    """ Distance to the root node. """

def assert_valid_distance_tree(tree: DistanceTreeData) -> None:
    """ Checks whether a given distance tree is consistent. This function is for debugging CKP only. """

    assert_valid_tree(tree)
    root = tree.root
    assert tree.root_distances[root] == 0, f"{root=} must have 0 root distance"
    assert tree.parent_distances[root] == 0, f"{root=} must have 0 parent distance"

    stack = [tree.root]
    while stack:
        v = stack.pop()
        assert len(tree.children[v]) == len(tree.distances[v]), f"{len(tree.children[v])=} must be equal to {len(tree.distances[v])=} for {v=}"
        for ch, d in zip(tree.children[v], tree.distances[v]):
            assert tree.parent_distances[ch] == d
            assert tree.root_distances[ch] == tree.root_distances[v] + d
            stack.append(ch)

def distance_tree_from_neighbors(neighbors: list[list[int]], distances: list[list[int]], root: int = 0) -> DistanceTreeData:
    tree = DistanceTreeData()
    tree.root = root
    tree.sizes = None

    N = len(neighbors)
    children = tree.children = [[] for _ in neighbors]
    tree_distances = tree.distances = [[] for _ in neighbors]
    parents = tree.parents = [-1] * N
    depths = tree.depths = [0] * N
    parent_distances = tree.parent_distances = [0] * N
    root_distances = tree.root_distances = [0] * N
    
    children[root] = neighbors[root]
    tree_distances[root] = distances[root]

    for ch, d in zip((stack := neighbors[root].copy()), distances[root]):
        parents[ch] = root
        depths[ch] = 1
        parent_distances[ch] = root_distances[ch] = d
    
    stack_pop, stack_push = stack.pop, stack.append
    while stack:
        v = stack_pop()
        
        p, rd, nd = parents[v], root_distances[v], depths[v]+1
        for ch, d in zip(neighbors[v], distances[v]):
            if ch == p: continue

            parents[ch] = v
            depths[ch] = nd
            children[v].append(ch)
            tree_distances[v].append(d)
            parent_distances[ch] = d
            root_distances[ch] = rd + d

            if len(neighbors[ch]) > 1: stack_push(ch)

    return tree

def distance_tree_from_edges(edges: list[tuple[int, int, int]], root: int = 0) -> DistanceTreeData:
    neighbors = [[] for _ in range(len(edges)+1)]
    distances = [[] for _ in range(len(edges)+1)]
    
    for (x, y, d) in edges:
        assert(x != y)
        neighbors[x].append(y); neighbors[y].append(x)
        distances[x].append(d); distances[y].append(d)

    return distance_tree_from_neighbors(neighbors, distances, root)

def distance_tree_max_depths(tree: DistanceTreeData) -> list[int]:
    max_depths = [0] * len(tree)
    stack = [(tree.root, True)]

    stack_extend, stack_push, stack_pop = stack.extend, stack.append, stack.pop
    parent_distances, children = tree.parent_distances, tree.children
    
    while stack:
        v, f = stack_pop()
        if f:
            stack_push((v, False))
            stack_extend((ch, True) for ch in children[v] if len(children[ch]))
        else:
            max_depths[v] = max((parent_distances[ch] + max_depths[ch] for ch in children[v]), default=0)

    return max_depths