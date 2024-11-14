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

def disjoint_set_size(ds: DisjointSetData, ind:int):
    """ Returns the size of the set `ind` is in. """
    return ds.sizes[disjoint_set_find(ds, ind)]

def disjoint_set_find(ds: DisjointSetData, ind:int):
    """ Returns the representative element for `ind`. """
    # TODO: implement path compression without much overhead.
    parents = ds.parents
    while (root_ind := parents[ind]) != ind: ind = root_ind
    return ind

def disjoint_set_is_same_set(ds: DisjointSetData, x:int, y:int) -> bool:
    """ Returns whether `x` and `y` reside in the same set. """
    return disjoint_set_find(ds, x) == disjoint_set_find(ds, y)

def disjoint_set_union(ds: DisjointSetData, x:int, y:int) -> tuple[int, int]|None:
    """
        Take the union of `x` and `y`.
        
        Returns a tuple (x, y), when a set with root `y` is merged to `x`.
    """
    if (x := disjoint_set_find(ds, x)) == (y := disjoint_set_find(ds, y)): return None

    sizes, ranks = ds.sizes, ds.ranks
    if ranks[x] < ranks[y]: x, y = y, x

    ds.parents[y] = x; sizes[x] += sizes[y]

    if ranks[x] == ranks[y]: ranks[x] += 1

    return (x, y)
    
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
        # TODO: implement path compression without much overhead.
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