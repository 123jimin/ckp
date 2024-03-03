"""
    Collection of generic segment trees, supporting arbitrary groups / rings.
"""

import operator

class SimpleSegmentTree:
    """
        Simple, generic segment tree supporting arbitrary group operation.
        Use `SimpleSumSegmentTree` for a bit better performance.

        `SimpleSegmentTree` supports updating each element and reducing on a range in O(log N).
        However, it doesn't support efficient range item modifications. 
    """

    __slots__ = ('_len', '_cap', '_e', '_op', '_tree')

    _len: int
    """ Length of this segment tree. """

    _cap: int
    """ Max capacity of this segment tree. """

    _tree: list
    """ A flat representation of this segment tree. """

    def __init__(self, init_values:list, op=operator.add, e=0):
        """
            Creates a segment tree on `init_values`.
            
            `op` is the group operation and `e` is the group identity for the group this tree resides.
        """

        self._len = L = len(init_values)
        self._op, self._e = op, e

        if L == 0:
            self._cap = 0
            self._tree = []
            return
    
        self._cap = cap = 1 << (L-1).bit_length()
        self._tree = tree = [e] * cap + init_values + [e] * (cap - L)

        for i in range(cap-1, 0, -1):
            i2 = i+i; tree[i] = op(tree[i2], tree[i2+1])
        
    def __len__(self): return self._len
    def __bool__(self): return self._len > 0

    def __str__(self):
        tree, cap = self._tree, self._cap
        items = ", ".join(str(tree[cap+i]) for i in range(self._len))
        return f"[{items}]"
    
    def __getitem__(self, ind:int):
        return self._tree[self._cap + ind]
    
    def __setitem__(self, ind:int, value):
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")

        curr_ind = self._cap + ind
        op, tree = self._op, self._tree
        changed_value = tree[curr_ind] = value

        while curr_ind > 1:
            next_ind = curr_ind // 2
            match curr_ind%2:
                case 0: changed_value = tree[next_ind] = op(changed_value, tree[curr_ind+1])
                case 1: changed_value = tree[next_ind] = op(tree[curr_ind-1], changed_value)
            curr_ind = next_ind
    
    def _reduce_range(self, start:int, end:int, curr_tree:int, curr_offset:int, curr_size:int):
        curr_tree_end = curr_offset + curr_size
        start, end = max(start, curr_offset), min(end, curr_tree_end)
        if start >= end: return self._e
        if start == curr_offset and end == curr_tree_end: return self._tree[curr_tree]

        assert curr_size > 1
        if curr_size == 2:
            assert start+1 == end
            return self._tree[self._cap + start]

        left_child = curr_tree * 2
        right_child = left_child + 1
        child_size = curr_size // 2

        return self._op(
            self._reduce_range(start, end, left_child, curr_offset, child_size),
            self._reduce_range(start, end, right_child, curr_offset + child_size, child_size),
        )

    def reduce_range(self, start:int, end:int):
        """ Get the reduced value for indices in the half-open range [start, end). """
        if self._len == 0 or start >= end: return self._e
        return self._reduce_range(start, end, 1, 0, self._cap)
    
    def reduce(self):
        """ Get the reduced value for all elements in this tree. """
        if self._len == 0: return self._e
        return self._reduce_range(0, self._len, 1, 0, self._cap)
    
class SimpleSumSegmentTree:
    """
        Simple, segment tree for summing numbers in ranges.

        `SimpleSumSegmentTree` supports updating each element and reducing on a range in O(log N).
        However, it doesn't support efficient range item modifications. 
    """

    __slots__ = ('_len', '_cap', '_tree')

    _len: int
    """ Length of this segment tree. """

    _cap: int
    """ Max capacity of this segment tree. """

    _tree: list
    """ A flat representation of this segment tree. """

    def __init__(self, init_values:list):
        """ Creates a segment tree on `init_values`. """

        self._len = L = len(init_values)

        if L == 0:
            self._cap = 0
            self._tree = []
            return
    
        self._cap = cap = 1 << (L-1).bit_length()
        self._tree = tree = [0] * cap + init_values + [0] * (cap - L)

        for i in range(cap-1, 0, -1):
            i2 = i+i; tree[i] = tree[i2] + tree[i2+1]
        
    def __len__(self): return self._len
    def __bool__(self): return self._len > 0

    def __str__(self):
        tree, cap = self._tree, self._cap
        items = ", ".join(str(tree[cap+i]) for i in range(self._len))
        return f"[{items}]"
    
    def __getitem__(self, ind:int):
        return self._tree[self._cap + ind]
    
    def __setitem__(self, ind:int, value):
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")

        curr_ind = self._cap + ind
        tree = self._tree
        changed_value = tree[curr_ind] = value

        while curr_ind > 1:
            next_ind = curr_ind // 2
            match curr_ind%2:
                case 0: changed_value = tree[next_ind] = changed_value + tree[curr_ind+1]
                case 1: changed_value = tree[next_ind] = tree[curr_ind-1] + changed_value
            curr_ind = next_ind
    
    def _reduce_range(self, start:int, end:int, curr_tree:int, curr_offset:int, curr_size:int):
        curr_tree_end = curr_offset + curr_size
        start, end = max(start, curr_offset), min(end, curr_tree_end)
        if start >= end: return 0
        if start == curr_offset and end == curr_tree_end: return self._tree[curr_tree]

        assert curr_size > 1
        if curr_size == 2:
            assert start+1 == end
            return self._tree[self._cap + start]

        left_child = curr_tree * 2
        right_child = left_child + 1
        child_size = curr_size // 2

        return self._reduce_range(start, end, left_child, curr_offset, child_size) + self._reduce_range(start, end, right_child, curr_offset + child_size, child_size)

    def reduce_range(self, start:int, end:int):
        """ Get the sum from the half-open range [start, end). """
        if self._len == 0 or start >= end: return 0
        return self._reduce_range(start, end, 1, 0, self._cap)
    
    sum_range = reduce_range

    def reduce(self):
        """ Get the sum for all elements in this tree. """
        if self._len == 0: return 0
        return self._reduce_range(0, self._len, 1, 0, self._cap)