# TODO: Maybe move this into a different file?
class PerfectTreeData:
    __slots__ = ('_tree', '_L')

    _tree: list
    _L: int
    
    def __init__(self, D: int):
        self._L = L = 1 << D
        self._tree = [0] * (L+L)

def perfect_tree_sum_prefix(tree: PerfectTreeData, end: int) -> int:
    L, A = tree._L, tree._tree
    if end <= 0: return 0
    if end > L: end = L
    if end == L: return A[1]
    end += L
    res = 0
    while end > 1:
        if end & 1: res += A[end-1]
        end //= 2
    return res

def perfect_tree_sum_range(tree: PerfectTreeData, start: int, end: int) -> int:
    L, A = tree._L, tree._tree
    if start >= 0: start += L
    else: start = L
    if end < L: end += L
    else: end = L+L

    res = 0
    while start < end:
        if start & 1: res += A[start]; start += 1
        if end & 1: res += A[end-1]
        start //= 2; end //= 2
    
    return res

def offline_sorted_set_init(N: int) -> PerfectTreeData:
    """ Initialize an offline ordered set for N elements. """
    D = (N-1).bit_length()
    return PerfectTreeData(D)

def offline_sorted_set_len(tree: PerfectTreeData) -> int:
    """ Return the number of elements in the offline ordered set. """
    return tree._tree[1]

def offline_sorted_set_add(tree: PerfectTreeData, i: int) -> bool:
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

def offline_sorted_set_discard(tree: PerfectTreeData, i: int) -> bool:
    L, A = tree._L, tree._tree
    if i < 0 or i >= L: return
    i += L
    if not A[i]: return False
    A[i] = 0
    i //= 2
    while i:
        i2 = i+i
        A[i] = A[i2] + A[i2+1]
        i //= 2
    return True

def offline_sorted_set_kth(tree: PerfectTreeData, k: int) -> int|None:
    L, A = tree._L, tree._tree
    if k < 0 or k >= A[1]: return None
    i = 1
    while i < L:
        if k < (v := A[i2 := i+i]): i = i2
        else: k -= v; i = i2+1
    return i-L

def offline_sorted_set_prev(tree: PerfectTreeData, i: int) -> int|None:
    rank = perfect_tree_sum_prefix(tree, i)
    if rank: return offline_sorted_set_kth(tree, rank-1)
    else: return None

def offline_sorted_set_next(tree: PerfectTreeData, i: int) -> int|None:
    rank = perfect_tree_sum_prefix(tree, i+1)
    if rank >= tree._tree[1]: return None
    else: return offline_sorted_set_kth(tree, rank)

class OfflineSortedSet(PerfectTreeData):
    def __init__(self, N: int):
        super().__init__((N-1).bit_length())
    
    def __len__(self) -> int:
        return self._tree[1]

    def add(self, i: int) -> bool:
        return offline_sorted_set_add(self, i)

    def discard(self, i: int) -> bool:
        return offline_sorted_set_discard(self, i)

    def kth(self, k: int) -> int|None:
        return offline_sorted_set_kth(self, k)
    
    def prev(self, i: int) -> int|None:
        return offline_sorted_set_prev(self, i)

    def next(self, i: int) -> int|None:
        return offline_sorted_set_next(self, i)
    
    def __contains__(self, i: int) -> bool:
        L = self._L
        return 0 <= i < L and (not not self._tree[i + L])