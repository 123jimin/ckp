"""
    A QuadEdge is simply a tuple: (... 4 edges, src, dst)
"""

def make_delaunay_quad_edge(src: int, dst: int):
    # Edges must be constructed before the quadedge, so temporarily set the parent to `None`.
    e0 = DelaunayEdge(None, 0, src)
    e1 = DelaunayEdge(None, 1)
    e2 = DelaunayEdge(None, 2, dst)
    e3 = DelaunayEdge(None, 3)

    t = (e0, e1, e2, e3, src, dst)
    e0.parent = e1.parent = e2.parent = e3.parent = t
    e1.next, e3.next = e3, e1

    return t

class DelaunayEdge:
    __slots__ = ('next', 'data', 'index', 'parent')

    parent: tuple
    data: int|None

    def __init__(self, parent:tuple, index:int=0, data:int|None=None):
        self.next = self
        self.parent = parent
        self.index = index
        self.data = data
    
    def __repr__(self):
        return f"DelaunayEdge(({self.parent[4]} -> {self.parent[5]}), {self.index}, {self.data})"
    
    def rot(self): return self.parent[(self.index+1)%4]
    def sym(self): return self.parent[(self.index+2)%4]
    def tor(self): return self.parent[(self.index+3)%4]

    def lnext(self): return self.parent[(self.index+3)%4].next.rot()
    def lprev(self): return self.parent[(self.index+1)%4].next.tor()

    def prev(self): return self.parent[(self.index+1)%4].next.rot()
    def rprev(self): return self.parent[(self.index+2)%4].next

    def src(self) -> int|None: return self.data
    def dst(self) -> int|None: return self.parent[(self.index+2)%4].data

    def splice_with(self, other):
        self_f: DelaunayEdge = self.next.rot()
        other_f: DelaunayEdge = other.next.rot()
        self_f.next, other_f.next = other_f.next, self_f.next
        self.next, other.next = other.next, self.next