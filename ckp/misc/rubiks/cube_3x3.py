from .corner import corner_init, corner_turn
from .edge import edge_init, edge_turn

class Cube3x3:
    __slots__ = ('corner', 'edge')

    def __init__(self, corner=None, edge=None):
        assert((corner and edge) or not (corner or edge))

        self.corner = corner or corner_init()
        self.edge = edge or edge_init()
    
    def turn(self, move: int|list[int]):
        corner, edge = self.corner, self.edge
        if isinstance(move, list):
            for m in move:
                corner = corner_turn(corner, m)
                edge = edge_turn(edge, m)
            self.corner, self.edge = corner, edge
        else:
            self.corner = corner_turn(corner, move)
            self.edge = edge_turn(edge, move)