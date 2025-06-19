from ..abc import AbstractSegmentTree

# TODO: Optimize `_apply`, `_build`, and `_push`!
class NumberSegmentTree(AbstractSegmentTree):
    """ A segment tree on integers/floats supporting range add/sum operations. """

    __slots__ = ('_tree', '_lazy', '_h')

    _tree: list
    """ A flat representation of this segment tree. """

    _lazy: list
    """ A flat representation of lazy-updates in this segment tree. """

    _h: int

    def __init__(self, init_values: list|int):
        is_init_list = not isinstance(init_values, int)
        L = self._len = len(init_values) if is_init_list else init_values
        self._h = L.bit_length()
        if not L: self._tree = []; self._lazy = []; return

        tree = self._tree = [0] * L + init_values if is_init_list else [0] * (L+L)
        for i in range(L-1, 0, -1):
            i2 = i+i; tree[i] = tree[i2] + tree[i2+1]
        
        self._lazy = [0] * L
    
    def _apply(self, ind: int, value, size: int):
        self._tree[ind] += value * size
        if ind < self._len: self._lazy[ind] += value
    
    def _build(self, start: int, end: int):
        L, tree, lazy = self._len, self._tree, self._lazy
        k = 2
        start, end = start + L, end + L-1
        while start > 1:
            start //= 2; end //= 2
            for i in range(end, start-1, -1):
                i2 = i+i
                tree[i] = tree[i2] + tree[i2+1] + lazy[i] * k
            k += k
    
    # TODO: remove this (after improving `add_to_range`).
    def _calc(self, ind: int, size: int):
        self._tree[ind] = self._tree[ind+ind] + self._tree[ind+ind+1] + self._lazy[ind] * size

    def _push(self, start: int, end: int):
        L = self._len
        k = 1 << (self._h - 1)
        start, end = start + L, end + L-1
        for s in range(self._h, 0, -1):
            for i in range(start>>s, (end>>s)+1):
                value = self._lazy[i]
                i2 = i+i
                self._apply(i2, value, k)
                self._apply(i2+1, value, k)
                self._lazy[i] = 0
            k //= 2

    def __getitem__(self, ind: int): return self.sum_range(ind, ind+1)
    def sum_range(self, start: int, end: int):
        L = self._len
        start, end = max(0, start), min(L, end)
        if start >= end: return 0
        self._push(start, start+1)
        self._push(end-1, end)
        res = 0
        start, end = start+L, end+L
        while start < end:
            if start&1: res += self._tree[start]; start += 1
            if end&1: res += self._tree[end-1]
            start //= 2; end //= 2
        return res
    def sum_all(self): return self.sum_range(0, len(self))

    def __setitem__(self, ind: int, value):
        prev_val = self.sum_range(ind, ind+1)
        self.add_to_range(ind, ind+1, value - prev_val)

    def add_to(self, ind: int, value): self.add_to_range(ind, ind+1, value)
    def add_to_range(self, start: int, end: int, value):
        if not value: return
        if start >= end: return

        L = self._len
        self._push(start, start+1)
        self._push(end-1, end)
        l0, r0, k = start, end, 1
        start, end = start+L, end+L
        while start < end:
            if start&1: self._apply(start, value, k); start += 1
            if end&1: self._apply(end-1, value, k)
            start //= 2
            end //= 2
            k += k
        self._build(l0, l0+1)
        self._build(r0-1, r0)