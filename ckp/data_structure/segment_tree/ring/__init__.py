class NumberRingSegmentTree:
    """ Temporary implementation for RingSegmentTree. """

    __slots__ = ('_len', '_cap', '_tree', '_lazy_mul', '_lazy_add')

    _len: int
    _cap: int
    _tree: list[int|float]
    _lazy_mul: list[int|float]
    _lazy_add: list[int|float]

    def __init__(self, init_values: list[int|float]):
        self._len = n = len(init_values)
        if n == 0:
            self._cap = 0
            self._tree = []
            self._lazy_mul = []
            self._lazy_add = []
            return
    
        cap = 1 << (n-1).bit_length()
        self._cap = cap
        self._tree = tree =[0] * (2 * cap)

        tree[cap: cap+n] = init_values
        for i in range(cap-1, 0, -1):
            i2 = i+i
            tree[i] = tree[i2] + tree[i2+1]
        
        self._lazy_mul = [1] * cap
        self._lazy_add = [0] * cap
    
    def __len__(self): return self._len
    def __str__(self): return "[{}]".format(", ".join(map(str, self.__iter__())))
    def __iter__(self):
        for i in range(self._len): yield self.__getitem__(i)
    
    def __getitem__(self, ind: int):
        return self.sum_range(ind, ind + 1)
    
    def _apply(self, node: int, size: int, m, d):
        tree = self._tree
        tree[node] = tree[node] * m + size * d

        if node < self._cap:
            self._lazy_mul[node] *= m
            self._lazy_add[node] = self._lazy_add[node] * m + d
    
    def _push(self, node: int, size: int):
        if node >= self._cap: return

        m, d = self._lazy_mul[node], self._lazy_add[node]
        if m == 1 and d == 0: return

        h = size // 2
        n2 = node + node
        self._apply(n2, h, m, d)
        self._apply(n2+1, h, m, d)

        self._lazy_mul[node] = 1
        self._lazy_add[node] = 0

    def _sum_range(self, start: int, end: int, node: int, l: int, r: int):
        if r <= start or end <= l: return 0
        if start <= l and r <= end: return self._tree[node]

        self._push(node, r-l)
        h = (l + r) // 2
        n2 = node+node
        return self._sum_range(start, end, n2, l, h) + self._sum_range(start, end, n2+1, h, r)

    def sum_range(self, start: int, end: int):
        if self._len == 0 or start >= end: return 0
        start, end = max(start, 0), min(end, self._len)
        if start >= end: return 0
        return self._sum_range(start, end, 1, 0, self._cap)
    
    def sum_all(self):
        return self.sum_range(0, len(self))

    def __setitem__(self, ind: int, value):
        self.mul_add_to_range(ind, ind + 1, 0, value)

    def set_range(self, start: int, end: int, value):
        self.mul_add_to_range(start, end, 0, value)

    def add_to(self, ind: int, value):
        self.mul_add_to_range(ind, ind + 1, 1, value)

    def add_to_range(self, start: int, end: int, value):
        self.mul_add_to_range(start, end, 1, value)
    
    def mul_to(self, ind: int, value):
        self.mul_add_to_range(ind, ind + 1, value, 0)

    def mul_to_range(self, start: int, end: int, value):
        self.mul_add_to_range(start, end, value, 0)

    def mul_add_to(self, ind: int, m, d):
        self.mul_add_to_range(ind, ind + 1, m, d)

    def _mul_add_to_range(self, start: int, end: int, m, d, node: int, l: int, r: int):
        if r <= start or end <= l: return
        if start <= l and r <= end:
            self._apply(node, r-l, m, d)
            return
    
        self._push(node, r-l)
        
        h = (l+r) // 2
        n2 = node+node
        self._mul_add_to_range(start, end, m, d, n2, l, h)
        self._mul_add_to_range(start, end, m, d, n2+1, h, r)
        self._tree[node] = self._tree[n2] + self._tree[n2+1]
    
    def mul_add_to_range(self, start: int, end: int, m, d):
        self._mul_add_to_range(start, end, m, d, 1, 0, self._cap)