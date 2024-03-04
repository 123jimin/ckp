import operator

class SimpleSegmentTree:
    """
        Simple, generic segment tree supporting arbitrary monoid operation.
        Use `SimpleSumSegmentTree` for a bit better performance.

        `SimpleSegmentTree` supports updating each element and reducing on a range in O(log N).
        However, it doesn't support efficient range item modifications. 
    """

    __slots__ = ('_len', '_e', '_op', '_tree')

    _len: int
    """ Length of this segment tree. """

    _tree: list
    """ A flat representation of this segment tree; `len(self._tree) == 2*self._len`. """

    def __init__(self, init_values:list, op=operator.add, e=0):
        """
            Creates a segment tree on `init_values`.
            
            `op` is the monoid operation and `e` is the identity for the monoid this tree resides.
        """

        self._len = L = len(init_values)
        self._op, self._e = op, e

        if L == 0:
            self._tree = []
            return
    
        self._tree = tree = [e] * L + init_values

        for i in range(L-1, 0, -1):
            i2 = i+i; tree[i] = op(tree[i2], tree[i2+1])
        
    def __len__(self): return self._len
    def __iter__(self):
        L = self._len
        for i in range(L, L+L):
            yield self._tree[i]

    def __str__(self):
        tree, L = self._tree, self._len
        items = ", ".join(str(tree[i]) for i in range(L, L+L))
        return f"[{items}]"
    
    def __getitem__(self, ind:int):
        return self._tree[self._len + ind]
    
    def __setitem__(self, ind:int, value):
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")

        curr_ind = self._len + ind
        op, tree = self._op, self._tree
        changed_value = tree[curr_ind] = value

        while curr_ind > 1:
            next_ind, r = divmod(curr_ind, 2)
            # `op` might not be commutative, so we can't optimize this into `op(changed_value, tree[curr_ind+(-1,1)[r]])`.
            changed_value = tree[next_ind] = op(changed_value, tree[curr_ind+1]) if r == 0 else op(tree[curr_ind-1], changed_value)
            curr_ind = next_ind

    def reduce_range(self, start:int, end:int):
        """ Get the reduced value for indices in the half-open range [start, end). """
        if self._len == 0 or start >= end: return self._e
        
        tree, L, e, op = self._tree, self._len, self._e, self._op
        start, end = max(0, start)+L, min(end, self._len)+L
        
        # `op` might not be commutative, so the left and right parts should be added separately.
        res_l, res_r = e, e
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
    
    def reduce(self):
        """ Get the reduced value for all elements in this tree. """
        if self._len == 0: return self._e
        return self.reduce_range(0, self._len)

class SimpleSumSegmentTree:
    """
        Simple, segment tree for summing numbers in ranges.

        `SimpleSumSegmentTree` supports updating each element and reducing on a range in O(log N).
        However, it doesn't support efficient range item modifications. 
    """

    __slots__ = ('_len', '_tree')

    _len: int
    """ Length of this segment tree. """

    _tree: list 
    """ A flat representation of this segment tree; `len(self._tree) == 2*self._len`. """

    def __init__(self, init_values:list):
        """ Creates a segment tree on `init_values`. """

        self._len = L = len(init_values)

        if L == 0:
            self._tree = []
            return
    
        self._tree = tree = [0] * L + init_values

        for i in range(L-1, 0, -1):
            i2 = i+i; tree[i] = tree[i2] + tree[i2+1]
        
    def __len__(self): return self._len
    def __iter__(self):
        L = self._len
        for i in range(L, L+L):
            yield self._tree[i]

    def __str__(self):
        tree, L = self._tree, self._len
        items = ", ".join(str(tree[i]) for i in range(L, L+L))
        return f"[{items}]"
    
    def __getitem__(self, ind:int):
        return self._tree[self._len + ind]
    
    def __setitem__(self, ind:int, value):
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")

        curr_ind = self._len + ind
        tree = self._tree
        changed_value = tree[curr_ind] = value

        while curr_ind > 1:
            next_ind, r = divmod(curr_ind, 2)
            changed_value = tree[next_ind] = changed_value + tree[curr_ind+(1,-1)[r]]
            curr_ind = next_ind

    def reduce_range(self, start:int, end:int):
        """ Get the sum from the half-open range [start, end). """
        if self._len == 0 or start >= end: return 0

        tree, L = self._tree, self._len
        start, end = max(0, start)+L, min(end, self._len)+L
        
        res = 0
        while start < end:
            sn, sr = divmod(start, 2)
            en, er = divmod(end, 2)
            if sr:
                res += tree[start]
                sn += 1
            if er:
                res += tree[end-1]

            start, end = sn, en
        
        return res
    
    sum_range = reduce_range

    def reduce(self):
        """ Get the sum for all elements in this tree. """
        if self._len == 0: return 0
        return self.reduce_range(0, self._len)