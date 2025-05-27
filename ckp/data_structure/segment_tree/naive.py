import operator

class NaiveMonoidSegmentTree:
    """ A naive implementation of a segment tree, that supports all common segment tree operations on an arbitrary monoid. """
    __slots__ = ('_values', '_zero', '_op')

    def __init__(self, init_values: list, monoid_op, monoid_zero):
        self._values = init_values
        self._op = monoid_op
        self._zero = monoid_zero

    def __len__(self): return len(self._values)
    def __str__(self): return "[{}]".format(", ".join(map(str, self._values)))
    def __iter__(self): return iter(self._values)

    def __getitem__(self, ind: int): return self._values[ind]
    def sum_range(self, start: int, end: int):
        if start >= end: return self._zero
        v = self._values[start]
        for i in range(start+1, end): v = self._op(v, self._values[i])
        return v
    def sum_all(self): return self.sum_range(0, len(self._values))

    def __setitem__(self, ind: int, value): self._values[ind] = value
    def set_range(self, start: int, end: int, value):
        for i in range(start, end): self._values[i] = value

    def add_to(self, ind: int, value): self._values[ind] = self._op(self._values[ind], value)
    def add_to_range(self, start: int, end: int, value):
        for i in range(start, end): self._values[i] = self._op(self._values[i], value)

class NaiveRingSegmentTree(NaiveMonoidSegmentTree):
    """ A naive implementation of a segment tree, that supports all common segment tree operations on an arbitrary ring. """
    __slots__ = ('_one', '_op_mul')

    def __init__(self, init_values: list, ring_add, ring_mul, ring_zero, ring_one):
        super().__init__(init_values, ring_add, ring_zero)
        self._one = ring_one
        self._op_mul = ring_mul
    
    def mul_to(self, ind: int, value): self._values[ind] = self._op_mul(self._values[ind], value)
    def mul_to_range(self, start: int, end: int, value):
        for i in range(start, end): self._values[i] = self._op_mul(self._values[i], value)
    
    def mul_add_to(self, ind: int, m, d):
        v = self._op_mul(self._values[ind], m)
        self._values[ind] = self._op(v, d)
    def mul_add_to_range(self, start: int, end: int, m, d):
        for i in range(start, end): self.mul_add_to(i, m, d)

class NaiveSegmentTree(NaiveRingSegmentTree):
    def __init__(self, init_values: list[int]):
        super().__init__(init_values, operator.add, operator.mul, 0, 1)