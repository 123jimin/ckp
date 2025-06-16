from .tree import TreeData

# TODO: add tests for DistanceTreeData
class DistanceTreeData(TreeData):
    """ Represents a tree, where each edge has length. """
    __slots__ = ('distances', 'parent_distances', 'root_distances')

    distances: list[list[int]]

    parent_distances: list[int]
    root_distances: list[int]

def _distance_tree_init_dfs(tree: DistanceTreeData, neighbors: list[list[int]], depth: int, root_distance: int, curr: int, parent: int = -1):
    tree.parents[curr] = parent
    tree.depths[curr] = depth
    tree.root_distances[curr] = root_distance
    parent_distances = tree.parent_distances

    for (ch, d) in zip(neighbors[curr], tree.distances[curr]):
        if ch == parent: continue

        tree.children[curr].append(ch)
        parent_distances[ch] = d
        _distance_tree_init_dfs(tree, depth+1, root_distance+d, ch, curr)

def distance_tree_init(neighbors: list[list[int]], distances: list[list[int]], root: int = 0) -> DistanceTreeData:
    tree = DistanceTreeData()
    tree.root = root
    tree.distances = distances
    tree.sizes = None

    N = len(neighbors)
    tree.children = [[] for _ in range(N)]
    tree.parents = [-1] * N
    tree.depths = [0] * N
    tree.parent_distances = [0] * N
    tree.root_distances = [0] * N

    # TODO: Remove DFS
    _distance_tree_init_dfs(tree, neighbors, 0, 0, root)
    return tree

def distance_tree_from_edges(edges: list[tuple[int, int, int]], root: int = 0) -> DistanceTreeData:
    neighbors = [[] for _ in range(len(edges)+1)]
    distances = [[] for _ in range(len(edges)+1)]
    for (x, y, d) in edges:
        assert(x != y)
        neighbors[x].append(y); neighbors[y].append(x)
        distances[x].append(d); distances[y].append(d)

    return distance_tree_init(neighbors, distances, root)