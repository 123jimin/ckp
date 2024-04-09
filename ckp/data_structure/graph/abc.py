import abc
from typing import Generator, Any

class AbstractGraph(abc.ABC):
    @abc.abstractmethod
    def __len__(self): pass

    @abc.abstractmethod
    def out_neighbors(self, x: int) -> Generator[int, None, None]: pass

    @abc.abstractmethod
    def add_edge(self, x: int, y: int): pass

    @abc.abstractmethod
    def has_edge(self, x: int, y: int) -> bool: pass

class AbstractWeightedGraph(AbstractGraph):
    @abc.abstractmethod
    def out_edges(self, x: int) -> Generator[tuple[int, Any], None, None]: pass

    @abc.abstractmethod
    def add_edge(self, x: int, y: int, w: Any): pass

    @abc.abstractmethod
    def get_weight(self, x: int, y: int): pass

def Undirected(GraphClass):
    has_del_edge = hasattr(GraphClass, 'del_edge')
    class UndirectedGraph(GraphClass):
        __slots__ = ('_super_add_edge', '_super_del_edge')
        def __init__(self, *args, **kwargs):
            s = super()
            s.__init__(*args, **kwargs)
            self._super_add_edge = s.add_edge
            if has_del_edge: self._super_del_edge = s.del_edge
        
        if issubclass(GraphClass, AbstractWeightedGraph):
            def add_edge(self, x: int, y: int, w: Any):
                add_edge = self._super_add_edge
                add_edge(x, y, w); add_edge(y, x, w)
        else:
            def add_edge(self, x: int, y: int):
                add_edge = self._super_add_edge
                add_edge(x, y); add_edge(y, x)

        if has_del_edge:
            def del_edge(self, x: int, y: int):
                del_edge = self._super_del_edge
                del_edge(x, y); del_edge(y, x)
                
    return UndirectedGraph