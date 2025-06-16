from .tree import TreeData

class TreeLCAData:
    """ Stores information about least common ancestors of a given tree. """
    __slots__ = ('ancestors', 'depths')

    ancestors: list[list[int]]
    depths: list[int]

def tree_lca_init(tree: TreeData) -> TreeLCAData:
    N = len(tree)
    lca = TreeLCAData()
    lca.depths = tree.depths
    ancestors = lca.ancestors = [[] for _ in range(N)]

    get_neighbors = tree.neighbors.__getitem__
    get_parent = tree.parents.__getitem__
    
    # Temporary value for the root node, to simplify visited check.
    ancestors[tree.root].append(-1)
    
    # BFS
    d = 1
    curr_chs = get_neighbors(tree.root).copy()
    next_chs = []
    while curr_chs:
        next_chs.clear()
        li = list(range(d.bit_length() - 1))
        for v in curr_chs:
            if (a := ancestors[v]): continue
            a.append(p := get_parent(v))
            a.extend((p := ancestors[p][i]) for i in li)
            # Intentionally do not check for parent node, to simplify visited check.
            if len(nv := get_neighbors(v)) > 1: next_chs.extend(nv)
        curr_chs, next_chs = next_chs, curr_chs
        d += 1

    # Remove temporary value for the root node.
    ancestors[tree.root].clear()

    return lca

def tree_lca_pth_ancestor(lca: TreeLCAData, v: int, p: int) -> int:
    """ Returns p-th ancestor of v. """
    ancestors = lca.ancestors
    while p:
        if p == 1: return ancestors[v][0]
        p -= 1<<(l := p.bit_length() - 1)
        v = ancestors[v][l]
    return v

def tree_lca_query(lca: TreeLCAData, v: int, w: int) -> int:
    """ Get the common ancestor of `v` and `w`. """

    if v == w: return v
    
    depths, ancestors = lca.depths, lca.ancestors
    d_v, d_w = depths[v], depths[w]
    if d_v < d_w:
        h = d_w - d_v
        while h:
            if h == 1: w = ancestors[w][0]; break
            h -= 1<<(l := h.bit_length() - 1)
            w = ancestors[w][l]
    elif d_w < d_v:
        h = d_v - d_w
        while h:
            if h == 1: v = ancestors[v][0]; break
            h -= 1<<(l := h.bit_length() - 1)
            v = ancestors[v][l]

    while v != w:
        pv, pw = ancestors[v], ancestors[w]

        # Using `zip(pv, pw)` is not faster.
        for i in range(len(pv)):
            nv, nw = pv[i], pw[i]
            if nv != nw: v, w = nv, nw; continue
            if i == 0: return nv
            break

    return v