"""
    Functions for dealing with complete binary trees via arrays, handy for implementing segment trees.
"""

def complete_binary_tree_from_list(init_values: list, nil_value = 0) -> list:
    """ Create  """
    return [nil_value] * len(init_values) + init_values

def complete_binary_tree_from_size(size: int, nil_value = 0) -> list:
    return [nil_value] * (size+size)

def complete_binary_tree_build(tree: list[int], reduce_op):
    for i in range(len(tree)//2-1, 0, -1):
        i2 = i+i; tree[i] = reduce_op(tree[i2], tree[i2+1])