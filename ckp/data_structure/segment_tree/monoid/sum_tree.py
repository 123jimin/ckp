""" Segment tree supporting range sum operations. """

class MonoidSumSegmentTree:
    """ Monoid segment tree that only supports range sum query. """

    __slots__ = ('_len', '_zero', '_op', '_tree')

    _len: int
    """ Amount of elements in this segment tree. """

    _tree: list
    """ A flat representation of this segment tree; `len(self._tree) == 2*self._len`. """

    def __init__(self, init_values: list, monoid_op, monoid_zero):
        L = self._len = len(init_values)
        self._op, self._zero = monoid_op, monoid_zero

        if not L:
            self._tree = []
            return
        
        tree = self._tree = [monoid_zero] * L + init_values

        for i in range(L-1, 0, -1):
            i2 = i+i; tree[i] = monoid_op(tree[i2], tree[i2+1])
    
    def __len__(self): return self._len
    def __str__(self): return "[%s]".format(", ".join(str(self._tree[i]) for i in range(self._len, self._len*2)))
    def __iter__(self):
        tree = self._tree
        for i in range(self._len, self._len*2):
            yield tree[i]

    def __getitem__(self, ind: int): return self._tree[self._len + ind]
    def sum_range(self, start: int, end: int):
        """ Get the sum of elements at indices in the half-open range [start, end). """
        if (not self._len) or start >= end: return self._zero
        
        tree, L, zero, op = self._tree, self._len, self._zero, self._op
        start, end = max(0, start)+L, min(end, L)+L

        # `op` might not be commutative, so the left and right parts should be added separately.
        res_l, res_r = zero, zero
        while start < end:
            sn, sr = divmod(start, 2)
            en, er = divmod(end, 2)
            if sr:
                res_l = op(res_l, tree[start])
                sn += 1
            if er:
                res_r = op(tree[end-1], res_r)

            start, end = sn, en
        
        return op(res_l, res_r)
    
    def sum_all(self):
        """ Get the sum of all elements in this tree. """
        return self._zero if self._len == 0 else self._tree[1]

    def __setitem__(self, ind: int, value):
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")
        
        curr_ind = self._len + ind
        op, tree = self._op, self._tree
        changed_value = tree[curr_ind] = value

        while curr_ind > 1:
            next_ind, r = divmod(curr_ind, 2)
            changed_value = tree[next_ind] = op(tree[curr_ind-1], changed_value) if r else op(changed_value, tree[curr_ind+1])
            curr_ind = next_ind

    def add_to(self, ind: int, value):
        """ Add a given value to (the right side of) `self[ind]`. """
        self.__setitem__(ind, self._op(self._tree[self._len + ind], value))
