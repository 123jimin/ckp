class DisjointSetData:
    """ A simple implementation of disjoint set structure. """

    __slots__ = ('parents', 'sizes', 'ranks')

    parents: list[int]
    sizes: list[int]
    ranks: list[int]

    def __len__(self): return len(self.parents)

def disjoint_set_init(size: int) -> DisjointSetData:
    """ Create a disjoint set structure on `size` elements. """
    ds = DisjointSetData()
    ds.parents, ds.sizes, ds.ranks = list(range(size)), [1] * size, [0] * size

    return ds

def disjoint_set_size(ds: DisjointSetData, ind: int) -> int:
    """ Returns the size of the set `ind` is in. """
    return ds.sizes[disjoint_set_find(ds, ind)]

def disjoint_set_find(ds: DisjointSetData, ind: int) -> int:
    """ Returns the representative element for `ind`. """
    parents = ds.parents

    # Compress the path by half.
    while (parent := parents[ind]) != ind:
        parents[ind] = gparent = parents[parent]; ind = gparent
    
    return ind

def disjoint_set_is_same_set(ds: DisjointSetData, x: int, y: int) -> bool:
    """ Returns whether `x` and `y` reside in the same set. """
    parents = ds.parents

    # x = disjoint_set_find(ds, x)
    while (px := parents[x]) != x:
        parents[x] = gx = parents[px]; x = gx
    
    # y = disjoint_set_find(ds, y)
    while (py := parents[y]) != y:
        parents[y] = gy = parents[py]; y = gy
    
    return x == y

def disjoint_set_union(ds: DisjointSetData, x: int, y: int) -> bool:
    """ Merge sets containing `x` and `y`, and returns whether two sets were merged. """
    parents = ds.parents

    # x = disjoint_set_find(ds, x)
    while (px := parents[x]) != x:
        parents[x] = gx = parents[px]; x = gx
    
    # y = disjoint_set_find(ds, y)
    while (py := parents[y]) != y:
        parents[y] = gy = parents[py]; y = gy
    
    if x == y: return False

    # Processes union.
    sizes, ranks = ds.sizes, ds.ranks
    if ranks[x] < ranks[y]: x, y = y, x

    parents[y] = x; sizes[x] += sizes[y]
    if ranks[x] == ranks[y]: ranks[x] += 1

    return True

def disjoint_set_union_find(ds: DisjointSetData, x: int, y: int) -> tuple[int, int]|None:
    """ Merge sets containing `x` and `y`, and returns a tuple (rx, ry), where a set with root `rx` has been merged to another set with root `ry`. """
    parents = ds.parents

    # x = disjoint_set_find(ds, x)
    while (px := parents[x]) != x:
        parents[x] = gx = parents[px]; x = gx
    
    # y = disjoint_set_find(ds, y)
    while (py := parents[y]) != y:
        parents[y] = gy = parents[py]; y = gy
    
    if x == y: return None

    # Processes union.
    sizes, ranks = ds.sizes, ds.ranks
    if ranks[x] < ranks[y]: x, y = y, x

    parents[y] = x; sizes[x] += sizes[y]
    if ranks[x] == ranks[y]: ranks[x] += 1

    return (x, y)

class DisjointSet(DisjointSetData):
    """ Objected-oriented interface for manipulating the disjoint set data structure. """
    
    def __init__(self, size: int):
        self.parents, self.sizes, self.ranks = list(range(size)), [1] * size, [0] * size

    size = disjoint_set_size
    find = disjoint_set_find
    is_same_set = disjoint_set_is_same_set
    union = disjoint_set_union
    union_find = disjoint_set_union_find
    
class DisjointSetObject:
    """ Disjoint set that can be used without constructing the universe set. """

    __slots__ = ('key', 'value', '_parent', '_size', '_rank')

    _size: int
    _rank: int

    def __init__(self, key, value=None):
        """ Create a new disjoint set object. `key` and `value` may be set to arbitrary values. """
        self.key, self.value, self._parent, self._size, self._rank = key, value, self, 1, 0
    
    @property
    def size(self): return self.root._size

    @property
    def root(self):
        # Path compression omitted.
        curr = self
        while (parent := curr._parent) != curr: curr = parent
        return curr
    
    def in_same_set(self, other) -> bool:
        return self.root == other.root
    
    def union(self, other) -> tuple|None:
        x, y = self.root, other.root
        if x is y: return None

        if x._rank < y._rank: x, y = y, x
        y._parent = x; x._size += y._size
        if x._rank == y._rank: x._rank += 1

        return (x, y)