from .tree import tree_sizes
from typing import Generator

class TreeHLD:
    """ Stores information about heavy-light decomposition of a given tree. """

    __slots__ = ('tree', 'path_index', 'paths')
    path_index: list[tuple[int, int]]
    paths: list[list[int]]

    def __init__(self, tree, sizes: list[int]|None = None):
        if sizes is None: sizes = tree_sizes(tree.neighbors, tree.root)

        self.tree = tree
        self.path_index = [None] * len(tree)
        self.paths = [[]]

        self._init_node(sizes, 0, tree.root)

    def __str__(self): return f"<TreeHLD path_index={self.path_index} paths={self.paths}>"
    
    def _init_node(self, sizes: list[int], ind: int, curr: int, parent: int = -1):
        self.path_index[curr] = (ind, len(curr_path := self.paths[ind]))
        curr_path.append(curr)

        neighbors = self.tree.neighbors[curr]

        if parent != -1:
            if len(neighbors) == 1: return
            if len(neighbors) == 2:
                for ch in neighbors:
                    if ch != parent:
                        self._init_node(sizes, ind, ch, curr)
                        return
                assert(False)
        
        max_ch_size = max(sizes[ch] for ch in neighbors if ch != parent)
        for ch in neighbors:
            if ch == parent: continue
            if sizes[ch] == max_ch_size:
                max_ch_size += 1
                self._init_node(sizes, ind, ch, curr)
            else:
                new_ind = len(self.paths)
                self.paths.append([])
                self._init_node(sizes, new_ind, ch, curr)
    
    def decompose_descendant(self, ancestor: int, node: int) -> Generator[tuple[int, int, int], None, None]:
        """
            Given that `ancestor` is an ancestor of `node`, returns a list of intervals in heavy paths, where each interval is given as (path_index, path_start, path_end). The interval is half-open.
        """
        path_index, paths, tree = self.path_index, self.paths, self.tree
        p_ancestor, i_ancestor = path_index[ancestor]
        p_node, i_node = path_index[node]

        while p_ancestor != p_node:
            yield (p_node, 0, i_node+1)
            p_node, i_node = path_index[node := tree.parents[paths[p_node][0]]]

        assert(i_ancestor <= i_node)
        yield (p_ancestor, i_ancestor, i_node+1)