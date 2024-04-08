def _tree_parents_and_depths_dfs(neighbors: list[list[int]], parents: list[int], depths: list[int], depth: int, curr: int, parent: int = -1):
    parents[curr] = parent
    depths[curr] = depth
    for ch in neighbors[curr]:
        if ch != parent: _tree_parents_and_depths_dfs(neighbors, parents,depths, depth+1,  ch, curr)

def tree_parents_and_depths(neighbors: list[list[int]], root_ind: int = 0) -> list[int]:
    """ Create a list P, and D where P[i] is the parent of node i, and D[i] is the distance of node i from root. P[root_ind] is -1. """
    N = len(neighbors)

    parents = [-1] * N
    depths = [-1] * N

    _tree_parents_and_depths_dfs(neighbors, parents, depths, 0, root_ind)

    return parents, depths

def _tree_size_dfs(neighbors: list[list[int]], sizes: list[int], curr: int, parent: int = -1) -> int:
    sizes[curr] = s = 1 + sum(_tree_size_dfs(neighbors, sizes, ch, curr) for ch in neighbors[curr] if ch != parent)
    return s

def tree_sizes(neighbors: list[list[int]], root_ind: int = 0) -> list[int]:
    """ Constructs a list S, where S[i] is the size of the subtree rooted at node i. """
    sizes = [0] * len(neighbors)
    _tree_size_dfs(neighbors, sizes, root_ind)
    return sizes

class Tree:
    root: int

    neighbors: list[list[int]]
    parents: list[int]
    depths: list[int]

    def __init__(self, *, root: int = 0, neighbors: list[list[int]]|None = None, parents: list[int]|None = None, depths: list[int]|None = None):
        assert(neighbors or parents)
        self.root = root
        
        if not neighbors:
            neighbors = [[] for _ in range(len(parents))]
            for i in range(len(parents)):
                if (p := parents[i]) >= 0: neighbors[p].append(i); neighbors[i].append(p)
        elif not parents:
            parents, depths = tree_parents_and_depths(neighbors, root)
        
        if not depths:
            _, depths = tree_parents_and_depths(neighbors, root)
        
        self.neighbors = neighbors
        self.parents = parents
    
    def __len__(self): return len(self.parents)
    def __repr__(self): return f"Tree(parents={self.parents}, root={self.root})"

    @staticmethod
    def from_edges(edges: list[tuple[int, int]], root: int = 0):
        neighbors = [list[int]() for _ in range(len(edges)+1)]
        for (x, y) in edges: neighbors[x].append(y); neighbors[y].append(x)
        return Tree(neighbors=neighbors, root=root)