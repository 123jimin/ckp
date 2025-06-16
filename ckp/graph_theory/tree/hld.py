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

def tree_hld_init(tree: TreeData):
    tree_children = tree.children
    sizes = tree_sizes(tree)
    get_size = sizes.__getitem__

    path_index = [None] * len(tree)
    paths = [[]]

    stack = [(0, tree.root)]
    while stack:
        curr_ind, curr = stack.pop()
        path_index[curr] = (curr_ind, len(curr_path := paths[curr_ind]))
        curr_path.append(curr)
        children = tree_children[curr]

        if len(children) == 0:
            continue

        if len(children) == 1:
            stack.extend((curr_ind, ch) for ch in children)
            continue
        
        max_ch_size = max(map(get_size, children))
        for ch in children:
            if get_size(ch) == max_ch_size:
                # Heavy Path
                max_ch_size += 1
                stack.append((curr_ind, ch))
            else:
                # Light Path
                new_ind = len(paths)
                paths.append([])
                stack.append((new_ind, ch))
    
    hld = TreeHLDData()
    hld.tree = tree
    hld.path_index = path_index
    hld.paths = paths

    return hld

def tree_hld_decompose_descendant(hld: TreeHLDData, node: int, ancestor: int):
    """
        Given that `ancestor` is an ancestor of `node`, returns a list of intervals in heavy paths (`hld.paths`).
        - Each interval is given as a tuple `(path_index, path_start, path_end)`, which represents an interval `hld.paths[path_index][path_start:path_end]`.
        - Intervals are non-overlapping.
        - The union of all intervals is a continuous path from `node` to `ancestor`, including both ends.
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