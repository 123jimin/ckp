from ..abc import AbstractSegmentTree

class NumberSegmentTree(AbstractSegmentTree):
    """
        A segment tree on integers/floats supporting range add/sum operations.

        It can be quite tricky to customize this implementation. Check out `SimpleNumberSegmentTree` for a simpler implementation, but with worse performance.
    """

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
    
    def _push_two(self, x: int, y: int):
        L, H, tree, lazy = self._len, self._h, self._tree, self._lazy
        k = 1 << (H - 1)
        x += L; y += L
        
        for s in range(H, 1, -1):
            if (value := lazy[i := x >> s]):
                lazy[i] = 0
                tree[i2 := i+i] += (vk := value * k)
                lazy[i2] += value
                tree[i2 := i2+1] += vk
                if i2 < L: lazy[i2] += value

            if (value := lazy[i := y >> s]):
                lazy[i] = 0
                tree[i2 := i+i] += (vk := value * k)
                lazy[i2] += value
                tree[i2 := i2+1] += vk
                if i2 < L: lazy[i2] += value

            k //= 2
        
        if (value := lazy[i := x // 2]):
            lazy[i] = 0
            tree[x] += value
            tree[x^1] += value
        
        if (value := lazy[i := y // 2]):
            lazy[i] = 0
            tree[y] += value
            tree[y^1] += value

    def __getitem__(self, ind: int): return self.sum_range(ind, ind+1)

    def sum_range(self, start: int, end: int):
        L, tree = self._len, self._tree
        
        if start < 0: start = 0
        if end > L: end = L

        if start >= end: return 0
        self._push_two(start, end-1)
        res = 0
        start, end = start+L, end+L
        while start < end:
            if start&1: res += tree[start]; start += 1
            if end&1: res += tree[end-1]
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

        L, tree, lazy = self._len, self._tree, self._lazy
        self._push_two(start, end-1)

        cl, cr, k = False, False, 1
        start += L; end += L

        while start < end:
            if cl: s2=start+start; tree[start-1] = tree[s2-2] + tree[s2-1] + lazy[start-1] * k
            if cr: e2=end+end; tree[end] = tree[e2] + tree[e2+1] + lazy[end] * k
            if start&1: self._apply(start, value, k); cl = True; start += 1
            if end&1: self._apply(end-1, value, k); cr = True
            start //= 2; end //= 2; k += k

        start -= 1
        while end:
            if cl: s2=start+start; tree[start] = tree[s2] + tree[s2+1] + lazy[start] * k
            if cr and (not cl or start != end): e2=end+end; tree[end] = tree[e2] + tree[e2+1] + lazy[end] * k
            start //= 2; end //= 2; k += k

class SimpleNumberSegmentTree(AbstractSegmentTree):
    """
        A segment tree on integers/floats supporting range add/sum operations.

        This is a slower, but simpler, implementation of `NumberSegmentTree`, which may be used to customize a lazy segment tree.
    """

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

    # Not used in this tree, but could be useful for modifying this segtree.
    def _build(self, start: int, end: int):
        L, tree, lazy = self._len, self._tree, self._lazy
        k, start, end = 2, start + L, end + (L-1)
        while start > 1:
            start //= 2; end //= 2
            for i in range(end, start-1, -1):
                i2 = i+i
                tree[i] = tree[i2] + tree[i2+1] + lazy[i] * k
            k += k

    def _calc(self, ind: int, size: int):
        tree, lazy = self._tree, self._lazy
        ind2 = ind+ind
        tree[ind] = tree[ind2] + tree[ind2+1] + lazy[ind] * size

    def _push(self, ind: int):
        L, H, lazy = self._len, self._h, self._lazy
        k = 1 << (H - 1)
        ind += L

        for s in range(H, 0, -1):
            if (value := lazy[i := ind >> s]):
                self._apply(i2 := i+i, value, k)
                self._apply(i2+1, value, k)
                lazy[i] = 0
            k //= 2

    def __getitem__(self, ind: int): return self.sum_range(ind, ind+1)

    def sum_range(self, start: int, end: int):
        L, tree = self._len, self._tree
        
        if start < 0: start = 0
        if end > L: end = L

        if start >= end: return 0
        self._push(start); self._push(end-1)

        res = 0
        start += L; end += L
        while start < end:
            if start&1: res += tree[start]; start += 1
            if end&1: res += tree[end-1]
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
        self._push(start); self._push(end-1)
        
        k, cl, cr = 1, False, False
        start += L; end += L

        while start < end:
            if cl: self._calc(start-1, k)
            if cr: self._calc(end, k)
            if start&1: self._apply(start, value, k); cl = True; start += 1
            if end&1: self._apply(end-1, value, k); cr = True
            start //= 2; end //= 2; k += k
        
        start -= 1
        while end:
            if cl: self._calc(start, k)
            if cr and (not cl or start != end): self._calc(end, k)
            start //= 2; end //= 2; k += k