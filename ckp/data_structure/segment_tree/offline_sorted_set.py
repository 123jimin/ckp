from .binary_tree.complete_binary_tree import *

def offline_sorted_set_init(N: int) -> list:
    """ Initialize an offline ordered set for N elements. """
    return complete_binary_tree_from_size(1<<(N-1).bit_length())

def offline_sorted_set_add(tree: list, i: int) -> bool:
    if tree[len(tree)//2+i]: return False
    complete_binary_tree_set(tree, i, 1)
    return True

def offline_sorted_set_discard(tree: list, i: int) -> bool:
    if not tree[len(tree)//2+i]: return False
    complete_binary_tree_set(tree, i, 0)
    return True

def offline_sorted_set_kth(tree: list, k: int) -> int|None:
    L = len(tree)//2
    if k < 0 or k >= tree[1]: return None
    i = 1
    while i < L:
        if k < (v := tree[i2 := i+i]): i = i2
        else: k -= v; i = i2+1
    return i-L

def offline_sorted_set_prev(tree: list, i: int) -> int|None:
    rank = complete_binary_tree_sum_prefix(tree, i)
    if rank: return offline_sorted_set_kth(tree, rank-1)
    else: return None

def offline_sorted_set_next(tree: list, i: int) -> int|None:
    rank = complete_binary_tree_sum_prefix(tree, i+1)
    if rank >= tree[1]: return None
    else: return offline_sorted_set_kth(tree, rank)

class OfflineSortedSet:
    __slots__ = ('_tree',)
    _tree: list[0|1]

    def __init__(self, N: int):
        self._tree = offline_sorted_set_init(N)
    
    def __len__(self) -> int:
        return self._tree[1]

    def add(self, i: int) -> bool:
        return offline_sorted_set_add(self._tree, i)

    def discard(self, i: int) -> bool:
        return offline_sorted_set_discard(self._tree, i)

    def kth(self, k: int) -> int|None:
        return offline_sorted_set_kth(self._tree, k)
    
    def prev(self, i: int) -> int|None:
        return offline_sorted_set_prev(self._tree, i)

    def next(self, i: int) -> int|None:
        return offline_sorted_set_next(self._tree, i)
    
    def __contains__(self, i: int) -> bool:
        L = len(self._tree)//2
        return 0 <= i < L and (not not self._tree[i + L])