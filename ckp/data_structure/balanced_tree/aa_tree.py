"""
    An implementation of AA tree.

    A node is represented as a list of `[0:key, 1:value, 2:level, 3:size, 4:left, 5:right]`.
"""

def aa_tree_init(key, value):
    return [key, value, 1, 1, None, None]

def aa_tree_size(node):
    return node and node[3] or 0

def aa_tree_inspect(node, indent: str = "") -> str:
    """ Returns a tree view of the given AA tree. This function is for debugging CKP only. """
    if not node: return f"{indent}- <None>"
    curr = f"{indent}- {node[0]} => {node[1]} // level={node[2]}, size={node[3]}"
    if (not node[4]) and (not node[5]): return curr
    left = aa_tree_inspect(node[4], indent + "  ")
    right = aa_tree_inspect(node[5], indent + "  ")
    return f"{curr}\n{left}\n{right}"

def assert_valid_aa_tree(node) -> None:
    """ Checks whether a given AA tree is consistent. This function is for debugging CKP only. """
    if not node: return

    assert_valid_aa_tree(left := node[4])
    assert_valid_aa_tree(right := node[5])

    if (not left) and (not right):
        assert node[2] == 1, f"level {node[2]} must be 1"
        assert node[3] == 1, f"size {node[3]} must be 1"
        return

    if node[2] > 1:
        assert left, f"node with level {node[2]} must have left children"
        assert right, f"node with level {node[2]} must have right children"

    children_size = (left and left[3] or 0) + (right and right[3] or 0)
    assert node[3] == children_size + 1, f"size {node[3]} must be equal to {children_size=} + 1"

    left_level = (left and left[2] or 0)
    assert node[2] == left_level + 1, f"level {node[2]} must be equal to {left_level=} + 1"

    right_level = (right and right[2] or 0)
    assert node[2] >= right_level, f"level {node[2]} must be greater than or equal to {right_level=}"

    right_right_level = (right and right[5] and right[5][2] or 0)
    assert node[2] > right_right_level, f"level {node[2]} must be greater than {right_right_level=}"

def aa_tree_query(node, key):
    if node is None: return None
    if node[0] == key: return node[1]
    if key < node[0]: return aa_tree_query(node[4], key)
    return aa_tree_query(node[5], key)

def aa_tree_skew(node):
    if not node: return None
    if not (left := node[4]): return node
    if left[2] != node[2]: return node

    left_right = left[5]
    node_size = node[3]
    left[3], node[3] = node_size, node_size - (left[3] - (left_right and left_right[3] or 0))
    node[4] = left[5]
    left[5] = node
    return left

def aa_tree_split(node):
    if not node: return None
    if not (right := node[5]) or not (right_right := right[5]): return node
    if node[2] != right_right[2]: return node

    right_left = right[4]
    node_size = node[3]
    right[3], node[3] = node_size, node_size - (right[3] - (right_left and right_left[3] or 0))

    node[5] = right[4]
    right[4] = node
    right[2] += 1

    return right

def aa_tree_insert(node, key, value):
    if not node: return [key, value, 1, 1, None, None]
    
    if key < node[0]: node[4] = aa_tree_insert(node[4], key, value)
    elif key > node[0]: node[5] = aa_tree_insert(node[5], key, value)
    else: node[1] = value; return node

    node[3] += 1

    return aa_tree_split(aa_tree_skew(node))

def aa_tree_predecessor(node):
    if not (left := node[4]): return None
    while (next_node := left[5]): left = next_node
    return left

def aa_tree_successor(node):
    if not (right := node[5]): return None
    while (next_node := right[4]): right = next_node
    return right

def aa_tree_delete(node, key):
    if not node: return None

    if key < node[0]: node[4] = aa_tree_delete(node[4], key)
    elif key > node[0]: node[5] = aa_tree_delete(node[5], key)
    else:
        if not node[4]:
            if not node[5]: return None
            l = aa_tree_successor(node)
            # TODO