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

class LazySumSegmentTree:
    """
        A lazy segment tree supporting range sum and update operations.
    """

    __slots__ = ('_len', '_cap', '_tree', '_lazy')

    _len: int
    """ Length of this segment tree. """

    _cap: int
    """ Max capacity of this segment tree. """

    _tree: list
    """ A flat representation of this segment tree. """

    _lazy: list
    """ A flat representation of lazy-updates in this segment tree. """

    def __init__(self, init_values:list):
        self._len = L = len(init_values)

        if L == 0:
            self._cap = 0
            # These are only used as placeholders, so sharing references is fine.
            self._tree = self._lazy = []
            return
        
        self._cap = cap = 1 << (L-1).bit_length()
        self._tree = tree = [0] * cap + init_values + [0] * (cap - L)

        for i in range(cap-1, 0, -1):
            i2 = i+i; tree[i] = tree[i2] + tree[i2+1]
        
        self._lazy = [0] * cap
        
    def __len__(self): return self._len
    def __bool__(self): return self._len > 0

    def __str__(self):
        items = ", ".join(str(self[i]) for i in range(self._len))
        return f"[{items}]"
    
    def __getitem__(self, ind:int): return self.reduce_range(ind, ind+1)
    def __setitem__(self, ind:int, value):
        prev_val = self[ind]
        self._add_to_range(ind, ind+1, value - prev_val, 1, 0, self._cap)

    def _add_to_range(self, start:int, end:int, add_val, curr_tree:int, curr_offset:int, curr_size:int):
        curr_tree_end = curr_offset + curr_size
        start, end = max(start, curr_offset), min(end, curr_tree_end)
        if start >= end: return
        if curr_size == 1:
            self._tree[curr_tree] += add_val
            return
        if start == curr_offset and end == curr_tree_end:
            self._lazy[curr_tree] += add_val
            return
        self._tree[curr_tree] += add_val * (end-start)
        left_child = curr_tree * 2
        right_child = left_child + 1
        child_size = curr_size // 2
        self._add_to_range(start, end, add_val, left_child, curr_offset, child_size)
        self._add_to_range(start, end, add_val, right_child, curr_offset + child_size, child_size)

    def add_to_range(self, start:int, end:int, add_val):
        """ Add `add_val` to every values in the half-open range [start, end). """
        if self._len == 0 or start >= end: return
        self._add_to_range(start, end, add_val, 1, 0, self._cap)

    def _reduce_range(self, start:int, end:int, curr_tree:int, curr_offset:int, curr_size:int):
        lazy, tree, curr_tree_end = self._lazy, self._tree, curr_offset + curr_size
        start, end = max(start, curr_offset), min(end, curr_tree_end)
        if start >= end: return 0
        if curr_size == 1: return tree[curr_tree]
        
        lazy_val = lazy[curr_tree]
        left_child = curr_tree * 2
        right_child = left_child + 1
        child_size = curr_size // 2

        if lazy_val:
            if curr_size == 2:
                tree[left_child] += lazy_val
                tree[right_child] += lazy_val
            else:
                lazy[left_child] += lazy_val
                lazy[right_child] += lazy_val
            tree[curr_tree] += lazy_val * curr_size
            lazy[curr_tree] = 0

        if start == curr_offset and end == curr_tree_end: return tree[curr_tree]
        return self._reduce_range(start, end, left_child, curr_offset, child_size) + self._reduce_range(start, end, right_child, curr_offset + child_size, child_size)

    def reduce_range(self, start:int, end:int):
        """ Get the sum from the half-open range [start, end). """
        if self._len == 0 or start >= end: return 0
        return self._reduce_range(start, end, 1, 0, self._cap)
    
    sum_range = reduce_range