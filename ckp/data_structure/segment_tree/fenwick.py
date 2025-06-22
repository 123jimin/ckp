import bisect

from .abc import AbstractSegmentTree
from ckp.misc.compress_coords import compress_coords

class FenwickTree(AbstractSegmentTree):
    __slots__ = ('_tree',)

    _tree: list

    def __init__(self, init_values: list|int):
        is_init_list = not isinstance(init_values, int)
        n = self._len = len(init_values) if is_init_list else init_values
        self._tree = bit = [0] * (n+1)

        if not is_init_list: return
        for i, v in enumerate(init_values, 1):
            if not v: continue
            j = i
            while j <= n:
                bit[j] += v
                j += j&-j

    def _prefix_sum(self, i: int):
        """ Returns sum(self[j] for j in range(i)) """
        bit, s = self._tree, 0
        while i:
            s += bit[i]
            i -= i&-i
        return s

    def __getitem__(self, ind: int):
        return self.sum_range(ind, ind+1)

    def __setitem__(self, ind: int, value):
        self.add_to(ind, value - self[ind])
    
    def add_to(self, ind: int, value):
        """ Add a given value to `self[ind]`. """
        if not value: return
        bit, n = self._tree, self._len
        i = ind+1
        while i <= n:
            bit[i] += value
            i += i & -i
    
    def sum_range(self, start: int, end: int):
        """ Get the sum of elements at indices in the half-open range [start, end). """
        if not (L := self._len): return 0

        if start < 0: start = 0
        if end > L: end = L

        if start >= end: return 0

        return self._prefix_sum(end) - self._prefix_sum(start)

    def sum_all(self):
        """ Get the sum of all elements in this tree. """
        return self._prefix_sum(self._len)

class OfflineFenwickTree:
    """ A Fenwick Tree with compressed indices. """

    __slots__ = ('_tree', '_ind_values', '_ind_lookup')

    _tree: FenwickTree
    _ind_values: list
    _ind_lookup: dict

    def __init__(self, indices):
        ind_values = self._ind_values = compress_coords(indices)
        self._ind_lookup = {v: i for (i, v) in enumerate(ind_values)}
        self._tree = FenwickTree(len(ind_values))
    
    def __setitem__(self, ind: int, value):
        self._tree[self._ind_lookup[ind]] = value
    
    def _prefix_sum(self, ind: int):
        return self._tree._prefix_sum(bisect.bisect_left(self._ind_values, ind))

    def add_to(self, ind: int, value):
        self._tree.add_to(self._ind_lookup[ind], value)
    
    def sum_range(self, start: int, end: int):
        ind_values = self._ind_values
        return self._tree.sum_range(
            bisect.bisect_left(ind_values, start),
            bisect.bisect_left(ind_values, end),
        )
    
    def sum_all(self):
        return self._tree.sum_all()

class Offline2DFenwickTree:
    """ A 2D Fenwick Tree with compressed indices. """

    __slots__ = ('_trees', '_ind_values', '_ind_lookup')

    _trees: list[OfflineFenwickTree]
    _ind_values: list
    _ind_lookup: dict

    def __init__(self, points: list[tuple[int, int]]):
        x_values = self._ind_values = compress_coords({p[0] for p in points})
        lx = len(x_values)

        x_lookup = self._ind_lookup = {x: i for i, x in enumerate(x_values)}
        y_values_by_x = [[] for _ in x_values]
        y_values_by_x.append([])

        for x, y in points:
            x = x_lookup[x]+1
            while x <= lx:
                y_values_by_x[x].append(y)
                x += x & -x
        
        self._trees = [OfflineFenwickTree(y_values) for y_values in y_values_by_x]
        for x, y in points:
            self.add_to(x, y, 1)
    
    def _prefix_sum_by_x_ind(self, x_ind: int, y: int) -> int:
        L = len(trees := self._trees)
        s = 0
        while x_ind:
            s += trees[x_ind]._prefix_sum(y)
            x_ind -= x_ind & -x_ind
        return s

    def add_to(self, x: int, y: int, value: int):
        """ Adds `value` to the point `(x, y)`. """
        if not value: return
        trees = self._trees
        L1 = len(trees)
        i = self._ind_lookup[x]+1
        while i < L1:
            trees[i].add_to(y, value)
            i += i & -i

    def sum_rect(self, x_start: int, x_end: int, y_start: int, y_end: int) -> int:
        """ Adds all values such that x-coordinate is in [x_start, x_end) and y-coordinate is in [y_start, y_end). """
        ind_values = self._ind_values
        x_start = bisect.bisect_left(ind_values, x_start)
        x_end = bisect.bisect_left(ind_values, x_end)
        return (
            self._prefix_sum_by_x_ind(x_end, y_end) - self._prefix_sum_by_x_ind(x_start, y_end)
            + self._prefix_sum_by_x_ind(x_start, y_start) - self._prefix_sum_by_x_ind(x_end, y_start)
        )