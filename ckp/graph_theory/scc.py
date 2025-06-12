from ..data_structure.graph.abc import AbstractGraph

def strongly_connected_components(g: AbstractGraph):
    """
        Returns a list of strongly connected components.
        Runtime Complexity: `O(|V| + |E|)`
    """

    v_ind = [None] * len(g)
    v_lowlink = [None] * len(g)
    v_stack = [False] * len(g)
    stack = []
    index = 0

    scc_list = []

    def strong_connect(v, index):
        v_ind[v] = index
        lowlink = index

        index += 1
        stack.append(v)
        v_stack[v] = True

        for w in g.out_neighbors(v):
            if v_ind[w] is None:
                index = strong_connect(w, index)
                lowlink = min(lowlink, v_lowlink[w])
            elif v_stack[w]:
                lowlink = min(lowlink, v_ind[w])

        if lowlink == v_ind[v]:
            scc = []
            while True:
                w = stack.pop()
                v_stack[w] = False
                scc.append(w)
                if w == v: break
            scc_list.append(scc)
        
        v_lowlink[v] = lowlink
        return index

    for v in range(len(g)):
        if v_ind[v] is None:
            index = strong_connect(v, index)
    
    return scc_list