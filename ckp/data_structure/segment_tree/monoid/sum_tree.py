""" Segment tree supporting range sum operations. """

from math import gcd
from ..abc import AbstractSegmentTree

class AbstractSumSegmentTree(AbstractSegmentTree):
    """ Common methods for all monoid sum segment tree and their derivatives. """

    __slots__ = ('_tree',)

    _tree: list
    """ A flat representation of this segment tree; `len(self._tree) == 2*self._len`. """

    def __iter__(self): yield from map(self._tree.__getitem__, range(self._len, self._len*2))
    def __getitem__(self, ind: int): return self._tree[self._len + ind]

class MonoidSumSegmentTree(AbstractSumSegmentTree):
    """ Monoid segment tree that only supports range sum query. """

    __slots__ = ('_zero', '_op',)

    def __init__(self, init_values: list|int, monoid_op, monoid_zero):
        self._op, self._zero = monoid_op, monoid_zero
        is_init_list = not isinstance(init_values, int)

        L = self._len = len(init_values) if is_init_list else init_values
        if not L: self._tree = []; return
        
        tree = self._tree = [monoid_zero] * L + init_values if is_init_list else [monoid_zero] * (L+L)

        for i in range(L-1, 0, -1):
            i2 = i+i; tree[i] = monoid_op(tree[i2], tree[i2+1])

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
        # `self._tree[1]` can't be used when the monoid is not commutative.
        return self.sum_range(0, self._len)

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

class SumSegmentTree(AbstractSumSegmentTree):
    """ Segment tree for summing numbers in ranges. """

    __slots__ = ()
    
    def __init__(self, init_values: list|int):
        """ Creates a segment tree on `init_values`. """
        is_init_list = not isinstance(init_values, int)

        L = self._len = len(init_values) if is_init_list else init_values
        if not L: self._tree = []; return
    
        tree = self._tree = [0] * L + init_values if is_init_list else [0] * (L+L)

        for i in range(L-1, 0, -1):
            i2 = i+i; tree[i] = tree[i2] + tree[i2+1]
    
    def sum_range(self, start: int, end: int):
        """ Get the sum of elements at indices in the half-open range [start, end). """
        tree, L = self._tree, self._len
        if (not L) or start >= end: return 0
        
        start, end = max(0, start)+L, min(end, L)+L

        res = 0
        while start < end:
            sn, sr = divmod(start, 2)
            en, er = divmod(end, 2)
            if sr: res += tree[start]; sn += 1
            if er: res += tree[end-1]

            start, end = sn, en
        
        return res
    
    def sum_all(self):
        """ Get the sum of all elements in this tree. """
        return self._tree[1] if self._len else 0
    
    def __setitem__(self, ind: int, value):
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")
        
        curr_ind, tree = self._len + ind, self._tree
        changed_value = tree[curr_ind] = value

        while curr_ind > 1:
            next_ind, r = divmod(curr_ind, 2)
            changed_value = tree[next_ind] = changed_value + tree[curr_ind+(1,-1)[r]]
            curr_ind = next_ind

    def add_to(self, ind: int, value):
        """ Add a given value to (the right side of) `self[ind]`. """
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")
        
        curr_ind, tree = self._len + ind, self._tree
        tree[curr_ind] += value

        while curr_ind > 1: curr_ind //= 2; tree[curr_ind] += value

class MaxSegmentTree(AbstractSumSegmentTree):
    """ Segment tree for calculating max of a range of numbers. """

    __slots__ = ('_min')
    
    def __init__(self, init_values: list|int, min_value = 0):
        """ Creates a segment tree on `init_values`. """
        is_init_list = not isinstance(init_values, int)

        self._min = min_value

        L = self._len = len(init_values) if is_init_list else init_values
        if not L: self._tree = []; return
    
        tree = self._tree = [min_value] * L + init_values if is_init_list else [min_value] * (L+L)

        for i in range(L-1, 0, -1):
            i2 = i+i; tree[i] = max(tree[i2], tree[i2+1])
    
    def sum_range(self, start: int, end: int):
        """ Get the max value of elements at indices in the half-open range [start, end). """
        if (not self._len) or start >= end: return self._min
        
        tree, L = self._tree, self._len
        start, end = max(0, start)+L, min(end, L)+L

        res = self._min
        while start < end:
            sn, sr = divmod(start, 2)
            en, er = divmod(end, 2)

            if sr and er: res = max(res, tree[start], tree[end-1]); sn += 1
            elif sr: res = max(res, tree[start]); sn += 1
            elif er: res = max(res, tree[end-1])

            start, end = sn, en
        
        return res
    
    def sum_all(self):
        """ Get the max value of all elements in this tree. """
        return self._tree[1] if self._len else self._min
    
    def __setitem__(self, ind: int, value):
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")
        
        curr_ind, tree = self._len + ind, self._tree
        prev_value = tree[curr_ind]
        changed_value = tree[curr_ind] = value

        if prev_value == changed_value: return
        elif prev_value < changed_value:
            while curr_ind > 1:
                curr_ind //= 2
                if changed_value <= tree[curr_ind]: break
                tree[curr_ind] = changed_value
        else:
            while curr_ind > 1:
                next_ind, r = divmod(curr_ind, 2)
                other_value = tree[curr_ind+(1,-1)[r]]
                if prev_value <= other_value: break
                if changed_value < other_value: changed_value = other_value
                tree[curr_ind := next_ind] = changed_value
    
    def add_to(self, ind: int, value):
        """ Update `self[ind]` to `max(self[ind], value)`. """
        self.__setitem__(ind, max(self[ind], value))

class GCDSegmentTree(AbstractSumSegmentTree):
    """ Segment tree for calculating the GCD of elements in ranges. """

    __slots__ = ()
    
    def __init__(self, init_values: list|int):
        """ Creates a segment tree on `init_values`. """
        is_init_list = not isinstance(init_values, int)

        L = self._len = len(init_values) if is_init_list else init_values
        if not L: self._tree = []; return
    
        tree = self._tree = [0] * L + init_values if is_init_list else [0] * (L+L)

        for i in range(L-1, 0, -1):
            i2 = i+i; tree[i] = gcd(tree[i2], tree[i2+1])
    
    def sum_range(self, start: int, end: int):
        """ Get the GCD of elements at indices in the half-open range [start, end). """
        if (not self._len) or start >= end: return 0
        
        tree, L = self._tree, self._len
        start, end = max(0, start)+L, min(end, L)+L

        res = 0
        while start < end:
            sn, sr = divmod(start, 2)
            en, er = divmod(end, 2)
            if sr and er: res = gcd(res, tree[start], tree[end-1]); sn += 1
            elif sr: res = gcd(res, tree[start]); sn += 1
            elif er: res = gcd(res, tree[end-1])

            start, end = sn, en
        
        return res
    
    def sum_all(self):
        """ Get the GCD of all elements in this tree. """
        return self._tree[1] if self._len else 0
    
    def __setitem__(self, ind: int, value):
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")
        
        curr_ind, tree = self._len + ind, self._tree
        changed_value = tree[curr_ind] = value

        while curr_ind > 1:
            next_ind, r = divmod(curr_ind, 2)
            changed_value = tree[next_ind] = gcd(changed_value, tree[curr_ind+(1,-1)[r]])
            curr_ind = next_ind

    def add_to(self, ind: int, value):
        """ Update `self[ind]` to `gcd(self[ind], value)`. """
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")
        
        curr_ind, tree = self._len + ind, self._tree
        tree[curr_ind] = gcd(tree[curr_ind], value)

        while curr_ind > 1:
            orig_value = tree[curr_ind := curr_ind // 2]
            changed_value = gcd(orig_value, value)
            if orig_value == changed_value: return
            tree[curr_ind] = changed_value