from .abc import AbstractGraph, AbstractWeightedGraph, Undirected

class ListGraph(AbstractGraph):
    """ Weightless directed graph, with no supports for duplicated edge checks, nor edge removals. """
    __slots__ = ('neighbors', 'n')
    neighbors: list[list[int]]
    n: int

    def __init__(self, n: int, neighbors: list[list[int]]|None = None):
        if neighbors:
            self.n = len(neighbors)
            self.neighbors = neighbors
        else:
            self.n = n
            self.neighbors = [[] for _ in range(n)]
    
    def __len__(self): return self.n

    def out_neighbors(self, x: int): return self.neighbors[x]

    def add_edge(self, x: int, y: int): self.neighbors[x].append(y)

    def has_edge(self, x: int, y: int): return y in self.neighbors[x]

class UndirectedListGraph(Undirected(ListGraph)): pass

class SetGraph(AbstractGraph):
    """ Weightless directed graph, ignoring duplicated edges and supporting edge removals. """
    __slots__ = ('neighbors', 'n')
    neighbors: list[set[int]]
    n: int

    def __init__(self, n: int, neighbors: list[set[int]]|None = None):
        if neighbors:
            self.n = len(neighbors)
            self.neighbors = neighbors
        else:
            self.n = n
            self.neighbors = [set() for _ in range(n)]
    
    def __len__(self): return self.n

    def out_neighbors(self, x: int): return self.neighbors[x]

    def add_edge(self, x: int, y: int): self.neighbors[x].add(y)

    def has_edge(self, x: int, y: int): return y in self.neighbors[x]

    def del_edge(self, x: int, y: int): self.neighbors[x].remove(y)

class UndirectedSetGraph(Undirected(SetGraph)): pass

class DictGraph(AbstractWeightedGraph):
    """ Weighted, directed graph. """
    __slots__ = ('neighbors', 'n')
    neighbors: list[dict[int]]
    n: int

    def __init__(self, n: int, neighbors: list[dict[int]]|None = None):
        if neighbors:
            self.n = len(neighbors)
            self.neighbors = neighbors
        else:
            self.n = n
            self.neighbors = [dict() for _ in range(n)]
    
    def __len__(self): return self.n

    def __repr__(self): return f"DictGraph({self.n}, {repr(self.neighbors)})"

    def out_neighbors(self, x: int): return self.neighbors[x].keys()

    def add_edge(self, x: int, y: int, w): self.neighbors[x][y] = w

    def has_edge(self, x: int, y: int) -> bool: return y in self.neighbors[x]

    def out_edges(self, x: int): return self.neighbors[x].items()

    def get_weight(self, x: int, y: int): return self.neighbors[x].get(y)

class UndirectedDictGraph(Undirected(DictGraph)): pass

class DictFlowGraph(DictGraph):
    __slots__ = ('_super_add_edge', 'neighbors')

    def __init__(self, n: int, neighbors: list[dict[int]]|None = None):
        s = super()
        s.__init__(n, neighbors)
        self._super_add_edge = s.add_edge

    def add_edge(self, x: int, y: int, w):
        if w: self._super_add_edge(x, y, w)
        else:
            x_neighbors = self.neighbors[x]
            if y in x_neighbors: del x_neighbors[y]

    def add_flow(self, x: int, y: int, w):
        if not w: return
        self.add_weight(x, y, w); self.add_weight(y, x, -w)

    def add_weight(self, x: int, y: int, w):
        if not w: return

        x_neighbors = self.neighbors[x]
        if (pw := x_neighbors.get(y)):
            if (w := pw + w):
                x_neighbors[y] = w
            else:
                del x_neighbors[y]
        else:
            x_neighbors[y] = w