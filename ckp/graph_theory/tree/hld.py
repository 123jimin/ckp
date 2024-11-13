from .tree import TreeData, tree_sizes

class TreeHLDData:
    """ Stores information about heavy-light decomposition of a given tree. """

    __slots__ = ('tree', 'path_index', 'paths')
    tree: TreeData
    path_index: list[tuple[int, int]]
    """ For each node `v`, `path_index[v]` is a tuple for index of v in `paths`."""
    paths: list[list[int]]
    """ A list of heavy paths. """
    
    def __str__(self): return f"<TreeHLD path_index={self.path_index} paths={self.paths}>"

def _tree_hld_init_node(hld: TreeHLDData, sizes: list[int], ind: int, curr: int, parent: int = -1):
    paths = hld.paths
    hld.path_index[curr] = (ind, len(curr_path := paths[ind]))
    curr_path.append(curr)

    neighbors = hld.tree.neighbors[curr]

    if parent == -1:
        if len(neighbors) == 0: return
    else:
        if len(neighbors) == 1: return
        if len(neighbors) == 2:
            for ch in neighbors:
                if ch != parent:
                    _tree_hld_init_node(hld, sizes, ind, ch, curr)
                    return
            assert(False)

    max_ch_size = max(sizes[ch] for ch in neighbors if ch != parent)

    for ch in neighbors:
        if ch == parent: continue
        if sizes[ch] == max_ch_size:
            # Heavy Path
            max_ch_size += 1
            _tree_hld_init_node(hld, sizes, ind, ch, curr)
        else:
            # Light Path
            new_ind = len(paths)
            paths.append([])
            _tree_hld_init_node(hld, sizes, new_ind, ch, curr)

def tree_hld_init(tree: TreeData, sizes: list[int]|None = None):
    if sizes is None: sizes = tree_sizes(tree.neighbors, tree.root)

    hld = TreeHLDData()
    hld.tree = tree
    hld.path_index = [None] * len(tree)
    hld.paths = [[]]

    _tree_hld_init_node(hld, sizes, 0, tree.root)

    return hld

def tree_hld_decompose_descendant(hld: TreeHLDData, node: int, ancestor: int):
    """
        Given that `ancestor` is an ancestor of `node`, returns a list of intervals in heavy paths (`hld.paths`).
        - Each interval is given as a tuple `(path_index, path_start, path_end)`, which represents an interval `hld.paths[path_index][path_start:path_end]`.
        - Intervals are non-overlaping.
        - The union of all intervals is a continous path from `node` to `ancestor`, including both ends.
    """
    
    path_index, paths, tree = hld.path_index, hld.paths, hld.tree
    parents = tree.parents
    p_ancestor, i_ancestor = path_index[ancestor]
    p_node, i_node = path_index[node]

    while p_ancestor != p_node:
        yield (p_node, 0, i_node+1)
        p_node, i_node = path_index[node := parents[paths[p_node][0]]]

    assert(i_ancestor <= i_node)
    yield (p_ancestor, i_ancestor, i_node+1)