from ..abc import AbstractSegmentTree

# TODO
"""
class MonoidAddSegmentTree(AbstractSegmentTree):
    __slots__ = ('_tree', '_zero', '_op')

    def __init__(self, init_values: list, monoid_op, monoid_zero):
        self._op, self._zero = monoid_op, monoid_zero

        L = self._len = len(init_values)
        if not L: self._tree = []; return
        
        tree = self._tree = [monoid_zero] * L + init_values

        for i in range(L-1, 0, -1):
            i2 = i+i; tree[i] = monoid_op(tree[i2], tree[i2+1])
"""
 
class AddSegmentTree(AbstractSegmentTree):
    """ Segment tree for range-add operation on numbers. """

    __slots__ = ('_tree',)

    _tree: list
    """ A flat representation of this segment tree; `len(self._tree) == 2*self._len`. """

    def __init__(self, init_values: list|int):
        is_init_list = not isinstance(init_values, int)
        L = self._len = len(init_values) if is_init_list else init_values
        if not L: self._tree = []; return

        self._tree = [0] * L + init_values if is_init_list else [0] * (L+L)

    def __getitem__(self, ind: int):
        ind += self._len
        tree = self._tree
        ret = tree[ind]
        while ind > 1:
            ind //= 2
            ret += tree[ind]
        return ret
    
    def __setitem__(self, ind: int, value):
        self.add_to(ind, value - self.__getitem__(ind))

    def add_to(self, ind: int, value):
        self._tree[self._len + ind] += value

    def add_to_range(self, start: int, end: int, value):
        tree, L = self._tree, self._len
        if (not self._len) or start >= end: return 0

        start, end = max(0, start)+L, min(end, L)+L

        while start < end:
            sn, sr = divmod(start, 2)
            en, er = divmod(end, 2)
            if sr: tree[start] += value; sn += 1
            if er: tree[end-1] += value

            start, end = sn, en