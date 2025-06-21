import bisect

class LinkedWaveletTreeData:
    """ A wavelet tree that stores left and right children via references. """
    __slots__ = ('_arr', '_min', '_max', '_left', '_right')

    _arr: list[int]
    _min: int
    _max: int

    def __init__(self, arr: list[int], min_value: int, max_value: list[int]):
        self._arr, self._min, self._max = arr, min_value, max_value
        self._left = self._right = None

        if min_value == max_value: return

        half_value = (min_value + max_value) // 2
        assert(min_value <= half_value < max_value)

        left_arr = list(filter(lambda v: v <= half_value, arr))
        right_arr = list(filter(lambda v: v > half_value, arr))

        assert(left_arr and right_arr)
        self._left = LinkedWaveletTreeData(left_arr, min_value, half_value)
        self._right = LinkedWaveletTreeData(right_arr, half_value+1, max_value)

    def __str__(self): return self._str()

    def _str(self, indent: int = 0):
        lines = [f"{' '*indent}{self._arr}"]
        if self._left: lines.append(self._left._str(indent+2))
        if self._right: lines.append(self._right._str(indent+2))

        return '\n'.join(lines)

    def __repr__(self): return f"LinkedWaveletTreeData(arr={repr(self._arr)}, min={self._min}, max={self._max})"

def linked_wavelet_tree_init(arr: list[int]):
    min_value, max_value = min(arr), max(arr)
    return LinkedWaveletTreeData(arr, min_value, max_value)

def linked_wavelet_tree_map_left(tree: LinkedWaveletTreeData, index: int) -> int:
    pass

def linked_wavelet_tree_map_right(tree: LinkedWaveletTreeData, index: int) -> int:
    pass