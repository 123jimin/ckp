from .abc import AbstractGraph, Undirected
from itertools import repeat

class ListGraphData:
    """ Weightless directed graph, with no supports for duplicated edge checks, nor edge removals. """

    __slots__ = ('neighbors',)
    neighbors: list[list[int]]

    def __init__(self, neighbors: list[list[int]]):
        self.neighbors = neighbors
    
    def __len__(self): return len(self.neighbors)

def list_graph_from_neighbors(neighbors: list[list[int]]) -> ListGraphData:
    return ListGraphData(neighbors)

def list_graph_add_edge(graph: ListGraphData, u: int, v: int):
    graph.neighbors[u].append(v)

def list_graph_add_bidi_edge(graph: ListGraphData, u: int, v: int):
    graph.neighbors[u].append(v); graph.neighbors[v].append(u)

class ListGraph(ListGraphData, AbstractGraph):
    """ Weightless directed graph, with no supports for duplicated edge checks, nor edge removals. """
    __slots__ = ()

    def __init__(self, neighbors: list[list[int]]|int):
        if isinstance(neighbors, int):
            self.neighbors = [[] for _ in repeat(None, neighbors)]
        else:
            self.neighbors = neighbors

    def out_neighbors(self, x: int): return self.neighbors[x]
    def add_edge(self, x: int, y: int): self.neighbors[x].append(y)
    def has_edge(self, x: int, y: int): return y in self.neighbors[x]

class UndirectedListGraph(Undirected(ListGraph)): pass