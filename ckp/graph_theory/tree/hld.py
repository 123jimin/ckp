from .tree import tree_sizes

class TreeHLD:
    """ Stores information about heavy-light decomposition of a given tree. """

    __slots__ = ('path_index', 'paths')
    path_index: list[int]
    paths: list[list[int]]

    def __init__(self, tree, sizes: list[int]|None = None):
        if sizes is None: sizes = tree_sizes(tree.neighbors, tree.root)

        self.path_index = [None] * len(tree)
        self.paths = [[]]

        self._init_node(tree, sizes, 0, tree.root)
    
    def _init_node(self, tree, sizes: list[int], ind: int, curr: int, parent: int = -1):
        self.path_index[curr] = ind
        self.paths[ind].append(curr)

        neighbors = tree.neighbors[curr]

        if parent != -1:
            if len(neighbors) == 1: return
            if len(neighbors) == 2:
                for ch in neighbors:
                    if ch != parent:
                        self._init_node(tree, sizes, ind, ch, curr)
                        return
                assert(False)
        
        max_ch_size = max(sizes[ch] for ch in neighbors if ch != parent)
        for ch in neighbors:
            if ch == parent: continue
            if sizes[ch] == max_ch_size:
                max_ch_size += 1
                self._init_node(tree, sizes, ind, ch, curr)
            else:
                new_ind = len(self.paths)
                self.paths.append([])
                self._init_node(tree, sizes, new_ind, ch, curr)

    def __str__(self):
        return f"<TreeHLD path_index={self.path_index} paths={self.paths}>"