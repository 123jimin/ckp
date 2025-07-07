"""
    Functions for dealing with complete binary trees via arrays.
    Essentially, this binary tree serves as an implementation of `MonoidSumSegmentTree`.
"""

def complete_binary_tree_from_list(init_values: list, nil_value = 0) -> list:
    """ Create a complete binary tree based on leaf values. """
    return [nil_value] * len(init_values) + init_values

def complete_binary_tree_from_size(size: int, nil_value = 0) -> list:
    """ Create an empty complete binary tree. """
    return [nil_value] * (size+size)

def complete_binary_tree_build(tree: list):
    for i in range(len(tree)//2-1, 0, -1):
        i2 = i+i; tree[i] = tree[i2] + tree[i2+1]

def complete_binary_tree_sum_range(tree: list, start: int, end: int):
    """ Get the sum of leaf nodes for indices in the half-open range [start, end). """
    L = len(tree)//2

    if start >= 0: start += L
    else: start = L

    if end < L: end += L
    else: end = L+L

    res = 0

    while start < end:
        if start & 1: res += tree[start]; start += 1
        if end & 1: res += tree[end - 1]
        start //= 2; end //= 2
    
    return res

def complete_binary_tree_set(tree: list, ind: int, value):
    L = len(tree) // 2
    if not(0 <= ind < L): raise IndexError(f"Index {ind} out of range (len={L})")

    curr_ind = L + ind
    if not (delta := value - tree[curr_ind]): return

    tree[curr_ind] = value
    while curr_ind > 1: tree[curr_ind := curr_ind//2] += delta

def complete_binary_tree_add_to(tree: list, ind: int, value):
    if not value: return

    L = len(tree) // 2
    if not(0 <= ind < L): raise IndexError(f"Index {ind} out of range (len={L})")
    
    tree[curr_ind := L + ind] += value
    while curr_ind > 1: tree[curr_ind := curr_ind//2] += value

def complete_binary_tree_build_monoid(tree: list, monoid_op):
    """ Build the tree with the given `monoid_op`, which may not be commutative. """
    for i in range(len(tree)//2-1, 0, -1):
        i2 = i+i; tree[i] = monoid_op(tree[i2], tree[i2+1])

def complete_binary_tree_sum_range_monoid(tree: list, start: int, end: int, monoid_op, monoid_zero):
    L = len(tree)//2

    if start >= 0: start += L
    else: start = L

    if end < L: end += L
    else: end = L+L
    
    # `op` might not be commutative, so the left and right parts should be added separately.
    res_l = res_r = monoid_zero
    while start < end:
        if start & 1: res_l = monoid_op(res_l, tree[start]); start += 1
        if end & 1: res_r = monoid_op(tree[end-1], res_r)
        start //= 2; end //= 2
    
    return monoid_op(res_l, res_r)