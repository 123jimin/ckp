from .tree import TreeData

class TreeLCAData:
    """ Stores information about least common ancestors of a given tree. """
    __slots__ = ('ancestors', 'depths')

    ancestors: list[list[int]]
    depths: list[int]

def tree_lca_init(tree: TreeData) -> TreeLCAData:
    lca = TreeLCAData()
    depths = lca.depths = tree.depths
    ancestors = lca.ancestors = [([p] if p >= 0 else []) for p in tree.parents]

    N = len(tree)
    D = max(depths)
    if D <= 1: return lca

    for i in range(D.bit_length()-1):
        for j in range(N):
            if len(a := ancestors[j]) <= i: continue
            if len(pa := ancestors[a[i]]) <= i: continue
            a.append(pa[i])
        
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