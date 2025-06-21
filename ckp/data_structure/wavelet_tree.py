# TODO: Implement this!

class LinkedWaveletTreeData:
    """ A wavelet tree that stores left and right children via references. """
    __slots__ = ('_arr', '_min', '_max', '_left', '_right')

    _arr: list[int]
    _min: int
    _max: int

    def __init__(self):
        pass

def linked_wavelet_tree_init(arr: list[int]):
    pass

def linked_wavelet_tree_map_left(tree: LinkedWaveletTreeData, index: int) -> int:
    pass

def linked_wavelet_tree_map_right(tree: LinkedWaveletTreeData, index: int) -> int:
    pass