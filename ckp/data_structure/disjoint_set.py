class DisjointSet:
    """ A simple implementation of disjoint set structure. """

    __slots__ = ('parents', 'sizes', 'ranks')

    parents: list[int]
    sizes: list[int]
    ranks: list[int]

    def __init__(self, size:int):
        """ Create a disjoint set structure on `size` elements. """
        self.parents, self.sizes, self.ranks = list(range(size)), [1] * size, [0] * size
    
    def __len__(self): return len(self.parents)

    def size(self, ind:int):
        """ Returns the size of the set `ind` is in. """
        return self.sizes[self.find(ind)]

    def find(self, ind:int):
        """ Returns the representative element for `ind`. """
        parents = self.parents
        while (root_ind := parents[ind]) != ind: ind = root_ind
        return ind
    
    def in_same_set(self, x:int, y:int) -> bool:
        """ Returns whether `x` and `y` reside in the same set. """
        return self.find(x) == self.find(y)

    def union(self, x:int, y:int) -> bool:
        """
            Take the union of `x` and `y`.
            
            Returns whether `x` and `y` were in different sets.
        """
        if (x := self.find(x)) == (y := self.find(y)): return False

        sizes, ranks = self.sizes, self.ranks
        if ranks[x] < ranks[y]: x, y = y, x

        self.parents[y] = x; sizes[x] += sizes[y]

        if ranks[x] == ranks[y]: ranks[x] += 1

        return True
    
class DisjointSetObject:
    """ Independently usable disjoint set. """

    __slots__ = ('key', 'value', '_parent', '_size', '_rank')

    _size: int
    _rank: int

    def __init__(self, key, value=None):
        """ Create a new disjoint set object. `key` and `value` may be set to arbitrary value. """
        self.key, self.value, self._parent, self._size, self._rank = key, value, self, 1, 0
    
    @property
    def size(self): return self.root._size

    @property
    def root(self):
        curr = self
        while (parent := curr._parent) != curr: curr = parent
        return curr
    
    def in_same_set(self, other) -> bool:
        return self.root == other.root
    
    def union(self, other) -> bool:
        x, y = self.root, other.root
        if x is y: return False

        if x._rank < y._rank: x, y = y, x
        y._parent = x; x._size += y._size
        if x._rank == y._rank: x._rank += 1

        return True