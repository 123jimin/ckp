# TODO: Maybe move this into a different file?
class PerfectTreeData:
    __slots__ = ('_tree', '_D')

    _tree: list
    _D: int
    
    def __init__(self, D: int):
        self._D = D
        L = 1 << D
        self._tree = [0] * (L+L)

def offline_ordered_set_init(N: int) -> PerfectTreeData:
    D = (N-1).bit_length()
    return PerfectTreeData(D)

def offline_ordered_set_add(tree: PerfectTreeData, i: int):
    pass

def offline_ordered_set_discard(tree: PerfectTreeData, i: int):
    pass

def offline_ordered_set_prev(tree: PerfectTreeData, i: int) -> int|None:
    pass

def offline_ordered_set_next(tree: PerfectTreeData, i: int) -> int|None:
    pass

class OfflineOrderedSet(PerfectTreeData):
    def __init__(self, N: int):
        super().__init__((N-1).bit_length())
    
    def add(self, i: int):
        offline_ordered_set_add(self, i)

    def discard(self, i: int):
        offline_ordered_set_discard(self, i)
    
    def prev(self, i: int) -> int|None:
        return offline_ordered_set_prev(self, i)

    def next(self, i: int) -> int|None:
        return offline_ordered_set_next(self, i)