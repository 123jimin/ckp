from .edge import DelaunayEdge, make_delaunay_quad_edge
from ..vector import vec2_orientation
from ..circumcircle import is_in_circumcircle_of_triangle

class DelaunayMesh:
    __slot__ = ('vertices', 'shuffled_indices', 'quad_edges')

    vertices: list[tuple[float, float]]
    shuffled_indices: list[int]|None
    quad_edges: list[tuple[DelaunayEdge, DelaunayEdge, DelaunayEdge, DelaunayEdge, int, int]]

    def __init__(self, vertices: list[tuple[float, float]], already_sorted: bool = False):
        if already_sorted:
            self.shuffled_indices = None
            self.vertices = vertices
        else:
            self.shuffled_indices = list(range(len(vertices)))
            self.shuffled_indices.sort(key=lambda i: vertices[i])
            self.vertices = [vertices[i] for i in self.shuffled_indices]
            
        self.quad_edges = []

    def __iter__(self):
        shuffled_indices = self.shuffled_indices
        if shuffled_indices:
            for edge in self.quad_edges:
                yield (shuffled_indices[edge[-2]], shuffled_indices[edge[-1]])
        else:
            for edge in self.quad_edges:
                yield (edge[-2], edge[-1])

    def make_edge(self, src: int, dst: int) -> DelaunayEdge:
        quad_edge = make_delaunay_quad_edge(src, dst)
        self.quad_edges.append(quad_edge)
        return quad_edge[0]
    
    def delete_edge(self, edge: DelaunayEdge):
        self.quad_edges.remove(edge.parent)
    
    def connect(self, a: DelaunayEdge, b: DelaunayEdge) -> DelaunayEdge:
        """ Connect two edges sharing the same left-face by creating a new quad-edge. """
        new_edge = self.make_edge(a.dst(), b.src())
        new_edge.splice_with(a.lnext())
        new_edge.sym().splice_with(b)
        return new_edge

    def _triangulate(self, start: int, end: int) -> tuple[DelaunayEdge, DelaunayEdge]:
        assert(start < end)
        vertices = self.vertices

        if start+3 >= end:
            if start+3 == end:
                # 3 vertices
                i1, i2, i3 = start, start+1, start+2
                a = self.make_edge(i1, i2)
                b = self.make_edge(i2, i3)
                a.sym().splice_with(b)
                ori = vec2_orientation(*vertices[start:end])
                if ori < 0:
                    c = self.connect(b, a)
                    return [c.sym(), c]
                if ori > 0:
                    c = self.connect(b, a)
                return [a, b.sym()]
            else:
                # 1 or 2 vertices
                a = self.make_edge(start, end-1)
                return [a, a.sym()]
        # 4 or more vertices
        mid = (start + end) // 2
        
        ldo, ldi = self._triangulate(start, mid)
        rdi, rdo = self._triangulate(mid, end)

        # Compute the lower common tangent of left and right halves.
        while True:
            ldi_src, rdi_src = vertices[ldi.src()], vertices[rdi.src()]
            if vec2_orientation(rdi_src, ldi_src, vertices[ldi.dst()]) > 0: ldi = ldi.lnext()
            elif vec2_orientation(ldi_src, vertices[rdi.dst()], rdi_src) > 0: rdi = rdi.rprev()
            else: break

        base1 = self.connect(rdi.sym(), ldi)
        if ldi.src() == ldo.src(): ldo = base1.sym()
        if rdi.src() == rdo.src(): rdo = base1

        while True:
            base1_src = vertices[base1.src()]
            base1_dst = vertices[base1.dst()]

            lcand: DelaunayEdge = base1.rprev()
            if vec2_orientation(base1_dst, base1_src, vertices[lcand.dst()]) > 0:
                while is_in_circumcircle_of_triangle(base1_dst, base1_src, vertices[lcand.dst()], vertices[lcand.next.dst()]):
                    t = lcand.next
                    self.delete_edge(lcand)
                    lcand = t
            
            rcand: DelaunayEdge = base1.prev()
            if vec2_orientation(base1_dst, base1_src, vertices[rcand.dst()]) > 0:
                while is_in_circumcircle_of_triangle(base1_dst, base1_src, vertices[rcand.dst()], vertices[rcand.prev().dst()]):
                    t = rcand.prev()
                    self.delete_edge(rcand)
                    rcand = t

            lvalid = vec2_orientation(base1_dst, base1_src, vertices[lcand.dst()]) > 0
            rvalid = vec2_orientation(base1_dst, base1_src, vertices[rcand.dst()]) > 0

            if not lvalid and not rvalid: break

            if (
                not lvalid or
                rvalid and is_in_circumcircle_of_triangle(vertices[lcand.dst()], vertices[lcand.src()], vertices[rcand.src()], vertices[rcand.dst()])
            ): base1 = self.connect(rcand, base1.sym())
            else: base1 = self.connect(base1.sym(), lcand.sym())

        last = end-1

        while ldo.src() != start: ldo = ldo.rprev()
        while rdo.src() != last: rdo = rdo.lprev()

        return [ldo, rdo]

    def triangulate(self):
        if len(self.vertices) > 0:
            self._triangulate(0, len(self.vertices))