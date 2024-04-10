class TreeLCA:
    """ Stores information about least common ancestors of a given tree. """

    parents: list[list[int]]
    depths: list[int]

    def __init__(self, tree):
        """ Given a `Tree` or `DistanceTree`, constructs a data structure that enables querying LCA in a logarithmic time. """
        depths = self.depths = tree.depths
        parents = self.parents = [([p] if p >= 0 else []) for p in tree.parents]

        N = len(tree)
        D = max(depths)
        if D <= 1: return

        for i in range(D.bit_length()-1):
            for j in range(N):
                if len(a := parents[j]) <= i: continue
                if len(pa := parents[a[i]]) <= i: continue
                a.append(pa[i])

    def ancestor(self, v: int, p: int) -> int:
        """ Retrieves p-th ancestor of v. """
        parents = self.parents
        while p:
            if p == 1: return parents[v][0]
            p -= 1<<(l := p.bit_length() - 1)
            v = parents[v][l]
        return v

    def get(self, v: int, w: int) -> int:
        if v == w: return v
        
        depths, parents = self.depths, self.parents
        
        d_v, d_w = depths[v], depths[w]
        if d_v < d_w:
            h = d_w - d_v
            while h:
                if h == 1: w = parents[w][0]; break
                h -= 1<<(l := h.bit_length() - 1)
                w = parents[w][l]
        elif d_w < d_v:
            h = d_v - d_w
            while h:
                if h == 1: v = parents[v][0]; break
                h -= 1<<(l := h.bit_length() - 1)
                v = parents[v][l]

        while v != w:
            pv, pw = parents[v], parents[w]

            # Using `zip(pv, pw)` is not faster.
            for i in range(len(pv)):
                nv, nw = pv[i], pw[i]
                if nv != nw: v, w = nv, nw; continue
                if i == 0: return nv
                break

        return v