from ckp.graph_theory.tree.tree import Tree

class TreeLCA:
    """ Stores information about least common ancestors of a given tree. """

    parents: list[list[int]]
    depths: list[int]

    def __init__(self, tree: Tree):
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
    
    def _ascend(self, v: int, h: int) -> int:
        """ Given that the depth of node v is at least h, Ascend h times towards the root. """
        parents = self.parents
        while h:
            if h == 1: return parents[v][0]
            l = h.bit_length() - 1
            h -= (2**l)
            v = parents[v][l]
        return v

    def get(self, v: int, w: int) -> int:
        if v == w: return v
        
        d_v, d_w = self.depths[v], self.depths[w]
        if d_v < d_w: w, d_w = self._ascend(w, d_w - d_v), d_v
        elif d_w < d_v: v, d_v = self._ascend(v, d_v - d_w), d_w

        parents = self.parents
        while v != w:
            pv, pw = parents[v], parents[w]

            for i in range(len(pv)):
                pvi, pwi = pv[i], pw[i]
                if pvi != pwi: continue
                if i == 0: return pvi
                v, w = pv[i-1], pw[i-1]
                break
            else:
                v, w = pv[-1], pw[-1]

        return v