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
        self._add_to_range(ind, ind+1, value - prev_val)

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
        """ Get the whole sum from the half-open range [start, end). """
        if self._len == 0 or start >= end: return 0
        return self._reduce_range(start, end, 1, 0, self._cap)
    
    sum_range = reduce_range