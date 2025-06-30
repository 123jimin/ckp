from ckp.data_structure.graph.bipartite import BipartiteGraphData

class BipartiteMatchingData:
    __slots__ = ('size', 'pair_u', 'pair_v')

    size: int
    pair_u: list[int]
    pair_v: list[int]

    def __init__(self): pass

def bipartite_matching(graph: BipartiteGraphData) -> BipartiteMatchingData:
    raise NotImplementedError("bipartite_matching not yet implemented!")