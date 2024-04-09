from .abc import AbstractGraph, Undirected

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