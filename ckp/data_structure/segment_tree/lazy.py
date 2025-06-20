import operator

# TODO: Merge this with `monoid.add_tree`.

class LazyOpSegmentTree:
    """
        A generic, lazy segment tree on a commutative monoid for supporting `add_to_range`, but not `reduce_range`. 
    """

    __slots__ = ('_len', '_e', '_op', '_tree')

    _len: int
    """ Length of this segment tree. """

    _tree: list
    """ A flat representation of this segment tree; `len(self._tree) == 2*self._len`. """

    def __init__(self, init_values:list, op=operator.add, e=0):
        """
            Creates a segment tree on `init_values`.
            
            `op` is the *commutative* monoid operation and `e` is the identity for the monoid this tree resides.
        """

        self._len = L = len(init_values)
        self._op, self._e = op, e

        if L == 0:
            self._tree = []
            return
    
        self._tree = [e] * L + init_values
        
    def __len__(self): return self._len

    def __str__(self):
        tree, L = self._tree, self._len
        items = ", ".join(str(tree[i]) for i in range(L, L+L))
        return f"[{items}]"
    
    def __iter__(self):
        self.apply_lazy()
        L, tree = self._len, self._tree
        for i in range(L, L+L): yield tree[i]
    
    def apply_lazy(self):
        """ Forces evaluation of lazy operations. """
        tree, op, e = self._tree, self._op, self._e
        for i in range(1, self._len):
            i2, t = i+i, tree[i]
            tree[i2] = op(tree[i2], t)
            tree[i2+1] = op(tree[i2+1], t)
            tree[i] = e
    
    def __getitem__(self, ind:int):
        tree, L, op = self._tree, self._len, self._op
        res = tree[x := L + ind]
        while x > 1:
            x //= 2
            res = op(res, tree[x])
        return res

    def add_to_range(self, start:int, end:int, add_val):
        """ Add `add_val` to every values in the half-open range [start, end). """
        if self._len == 0 or start >= end: return self._e
        
        tree, L, op = self._tree, self._len, self._op
        start, end = max(0, start)+L, min(end, self._len)+L
        
        while start < end:
            sn, sr = divmod(start, 2)
            en, er = divmod(end, 2)
            if sr:
                tree[start] = op(tree[start], add_val)
                sn += 1
            if er:
                e1 = end - 1
                tree[e1] = op(tree[e1], add_val)

            start, end = sn, en
