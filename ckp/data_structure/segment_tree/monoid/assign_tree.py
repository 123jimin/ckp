from ..abc import AbstractSegmentTree

# TODO
class MonoidAssignSegmentTree(AbstractSegmentTree):
    __slots__ = ('_tree', '_lazy', '_h', '_op', '_zero')

    def __init__(self, init_values: list|int, monoid_op, monoid_zero):
        self._op, self._zero = monoid_op, monoid_zero
        is_init_list = not isinstance(init_values, int)
        
        L = self._len = len(init_values) if is_init_list else init_values
        self._h = L.bit_length()
        if not L: self._tree = []; self._lazy = []; return

        tree = self._tree = [monoid_zero]*L + init_values if is_init_list else [monoid_zero]*(L+L)
        self._lazy = [None]*L

        for i in range(L-1, 0, -1):
            i2 = i+i; tree[i] = monoid_op(tree[i2]+tree[i2+1])