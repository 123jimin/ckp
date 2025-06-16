from .tree import TreeData, tree_with_root, tree_centroids

def _tree_isomorphism_signature_dfs(tree: TreeData, curr: int) -> int:
    if not (children := tree.children[curr]): return 0b10
    ch_sigs: list[int] = [_tree_isomorphism_signature_dfs(tree, ch) for ch in children]
    ch_sigs.sort()
    sig = 1
    for ch_sig in ch_sigs:
        sig = (sig << ch_sig.bit_length()) | ch_sig
    return sig << 1

def rooted_tree_isomorphism_signature(tree: TreeData) -> int:
    """
        Returns an *isomorphism signature* of a *rooted* tree.
        Two rooted trees have identical isomorphism signature iff two are isomorphic.
    """
    return _tree_isomorphism_signature_dfs(tree, tree.root)

def rooted_tree_is_isomorphic_to(a: TreeData, b: TreeData) -> bool:
    return rooted_tree_isomorphism_signature(a) == rooted_tree_isomorphism_signature(b)

def tree_isomorphism_signature(tree: TreeData) -> int:
    """
        Returns an *isomorphism signature* of a tree.
        Two trees have identical isomorphism signature iff two are isomorphic.
    """
    centroids = tree_centroids(tree)
    assert(len(centroids) in (1, 2))

    tree_0 = tree if tree.root == centroids[0] else tree_with_root(tree, centroids[0])
    sig_0 = _tree_isomorphism_signature_dfs(tree_0, tree_0.root)

    if len(centroids) == 1: return sig_0
    
    tree_1 = tree if tree.root == centroids[1] else tree_with_root(tree, centroids[1])
    sig_1 = _tree_isomorphism_signature_dfs(tree_1, tree_1.root)

    if sig_0 > sig_1: sig_0, sig_1 = sig_1, sig_0
    return (sig_0 << sig_1.bit_length()) | sig_1

def tree_is_isomorphic_to(a: TreeData, b: TreeData) -> bool:
    if len(a) != len(b): return False
    return tree_isomorphism_signature(a) == tree_isomorphism_signature(b)

def _tree_child_isomorphism_signatures_dfs(tree: TreeData, tree_sigs: list[int], tree_child_sigs: list[dict[int, list[int]]], curr: int, parent: int = -1) -> int:
    ch_sigs: list[int] = []
    tree_child_sigs[curr] = sig_dict = dict[int, list[int]]()
    neighbors = tree.neighbors[curr]
    if not neighbors:
        tree_sigs[curr] = 0b10
        return 0b10
    for ch in tree.neighbors[curr]:
        if ch == parent: continue
        ch_sigs.append(ch_sig := _tree_child_isomorphism_signatures_dfs(tree, tree_sigs, tree_child_sigs, ch, curr))
        if (sig_list := sig_dict.get(ch_sig)) is None:
            sig_list = sig_dict[ch_sig] = []
        sig_list.append(ch)
    ch_sigs.sort()
    sig = 1
    for ch_sig in ch_sigs:
        sig = (sig << ch_sig.bit_length()) | ch_sig
    tree_sigs[curr] = sig = sig << 1
    return sig

def rooted_tree_child_isomorphism_signatures(tree: TreeData) -> tuple[list[int], list[dict[int, list[int]]]]:
    """
        Returns a tuple of *subtree isomorphism signatures* `tree_sigs` and *children isomorphism signatures* `tree_child_sigs`.

        - `tree_sigs[x]` is the isomorphism signature of a subtree rooted at `x`.
        - `tree_child_sigs[x]` is a dictionary, where child indices are grouped by their subtree isomorphism signatures.
    """
    tree_sigs = [0b10] * len(tree)
    tree_child_sigs = [None] * len(tree)
    _tree_child_isomorphism_signatures_dfs(tree, tree_sigs, tree_child_sigs, tree.root)

    return (tree_sigs, tree_child_sigs)