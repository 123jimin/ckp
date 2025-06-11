class FenwickTree:
    __slots__ = ('_len', '_bit')

    _len: int
    _bit: list

    def __init__(self, init_values: list):
        n = self._len = len(init_values)
        self._bit = bit = [0] * (n+1)

        for i, v in enumerate(init_values, 1):
            if not v: continue
            j = i
            while j <= n:
                bit[j] += v
                j += j&-j

    def _add_bit(self, i: int, delta):
        bit, n = self._bit, self._len
        while i <= n:
            bit[i] += delta
            i += i & -i

    def _prefix_sum(self, i: int):
        """ Returns sum(self[j] for j in range(i)) """
        bit, s = self._bit, 0
        while i:
            s += bit[i]
            i -= i&-i
        return s

    def __len__(self): return self._len
    def __iter__(self):
        for i in range(self._len): yield self[i]
    
    def __str__(self): return "[{}]".format(", ".join(map(str, self.__iter__())))

    def __getitem__(self, ind: int):
        return self.sum_range(ind, ind+1)

    def __setitem__(self, ind: int, value):
        self.add_to(ind, value - self[ind])
    
    def add_to(self, ind: int, value):
        """ Add a given value to `self[ind]`. """
        if not value: return
        bit, n = self._bit, self._len
        i = ind+1
        while i <= n:
            bit[i] += value
            i += i & -i
    
    def sum_range(self, start: int, end: int):
        """ Get the sum of elements at indices in the half-open range [start, end). """
        if not self._len: return 0

        start, end = max(0, start), min(end, self._len)
        if start >= end: return 0

        return self._prefix_sum(end) - self._prefix_sum(start)

    def sum_all(self):
        """ Get the sum of all elements in this tree. """
        return self._prefix_sum(self._len)