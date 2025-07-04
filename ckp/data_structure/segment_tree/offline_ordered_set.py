# TODO: Maybe move this into a different file?
class PerfectTreeData:
    __slots__ = ('_tree', '_L')

    _tree: list
    _L: int
    
    def __init__(self, D: int):
        self._L = L = 1 << D
        self._tree = [0] * (L+L)

def offline_ordered_set_init(N: int) -> PerfectTreeData:
    D = (N-1).bit_length()
    return PerfectTreeData(D)

def offline_ordered_set_len(tree: PerfectTreeData) -> int:
    return tree._tree[1]

def offline_ordered_set_add(tree: PerfectTreeData, i: int) -> bool:
    L, A = tree._L, tree._tree
    if i < 0 or i >= L: return
    i += L
    if A[i]: return False
    A[i] = 1
    i //= 2
    while i:
        i2 = i+i
        A[i] = A[i2] + A[i2+1]
        i //= 2
    return True

def offline_ordered_set_discard(tree: PerfectTreeData, i: int) -> bool:
    L, A = tree._L, tree._tree
    if i < 0 or i >= L: return
    i += L
    if not A[i]: return False
    A[i] = 0
    i //= 2
    while i:
        i2 = i+i
        A[i] = A[i2] + A[i2+1]
    return True

def offline_ordered_set_kth(tree: PerfectTreeData, k: int) -> int|None:
    pass

def offline_ordered_set_prev(tree: PerfectTreeData, i: int) -> int|None:
    pass

def offline_ordered_set_next(tree: PerfectTreeData, i: int) -> int|None:
    pass

class OfflineOrderedSet(PerfectTreeData):
    def __init__(self, N: int):
        super().__init__((N-1).bit_length())
    
    def __len__(self) -> int:
        return self._tree[1]

    def add(self, i: int) -> bool:
        return offline_ordered_set_add(self, i)

    def discard(self, i: int) -> bool:
        return offline_ordered_set_discard(self, i)

    def kth(self, k: int) -> int|None:
        return offline_ordered_set_kth(self, k)
    
    def prev(self, i: int) -> int|None:
        return offline_ordered_set_prev(self, i)

    def next(self, i: int) -> int|None:
        return offline_ordered_set_next(self, i)
    
    def __contains__(self, i: int) -> bool:
        L = self._L
        return 0 <= i < L and (not not self._tree[i + L])