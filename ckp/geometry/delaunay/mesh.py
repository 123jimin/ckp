"""
    A quarter-edge is just an integer x.
    - Quad mask indices: x//4
    - Src and dst indices: x//2
    - Next indices: x
"""

from ..vector import vec2_orientation
from ..circumcircle import is_in_circumcircle_of_triangle

class DelaunayMesh:
    __slot__ = (
        'vertices',
        'shuffled_indices',
        '_quad_mask',
        'quad_src',
        'quad_dst',
        'quad_nxt',
        'quad_nxt_edge',
        'quad_nxt_face',
    )

    vertices: list[tuple[float, float]]
    shuffled_indices: list[int]|None # None when vertices are not shuffled.

    _quad_mask: list[bool] # To mark deleted edges (`False`)
    quad_src: list[int] # Source vertex indices for a quarter-edge
    quad_dst: list[int] # Destination vertex indices for a quarter-edge
    quad_nxt: list[int] # Next quarter-edge indices
    
    # TODO
    quad_nxt_edge: list[int] # Next edge quarter-edge indices
    quad_nxt_face: list[int] # Next facequarter-edge indices

    def __init__(self, vertices: list[tuple[float, float]], already_sorted: bool = False):
        if already_sorted:
            self.shuffled_indices = None
            self.vertices = vertices
        else:
            self.shuffled_indices = list(range(len(vertices)))
            self.shuffled_indices.sort(key=lambda i: vertices[i])
            self.vertices = [vertices[i] for i in self.shuffled_indices]
        
        self._quad_mask = []
        self.quad_src = []
        self.quad_dst = []
        self.quad_nxt = []

        self.quad_nxt_edge = []
        self.quad_nxt_face = []

    def __iter__(self):
        shuffled_indices = self.shuffled_indices
        quad_src = self.quad_src
        if shuffled_indices:
            for i in range(0, len(quad_src), 2):
                yield (shuffled_indices[quad_src[i]], shuffled_indices[quad_src[i+1]])
        else:
            for i in range(0, len(quad_src), 2):
                yield (quad_src[i], quad_src[i+1])
    
    def _lnext(self, x: int) -> int:
        x = self.quad_nxt[x^((x^(x+3))&3)]
        return x^((x^(x+1))&3)
    
    def _lprev(self, x: int) -> int:
        x = self.quad_nxt[x^((x^(x+1))&3)]
        return x^((x^(x+3))&3)
    
    def _oprev(self, x: int) -> int:
        x = self.quad_nxt[x^((x^(x+1))&3)]
        return x^((x^(x+1))&3)
    
    def make_edge(self, src: int, dst: int) -> int:
        self._quad_mask.append(True)
        self.quad_src.extend((src, dst))
        self.quad_dst.extend((dst, src))
        
        x = len(self.quad_nxt)
        self.quad_nxt.extend((x, x+3, x+2, x+1))

        return x
    
    def splice_edge(self, x: int, y: int):
        quad_nxt = self.quad_nxt
        xf = quad_nxt[x]; xf = xf^((xf^(xf+1))&3)
        yf = quad_nxt[y]; yf = yf^((yf^(yf+1))&3)
        quad_nxt[xf], quad_nxt[yf] = quad_nxt[yf], quad_nxt[xf]
        quad_nxt[x], quad_nxt[y] = quad_nxt[y], quad_nxt[x]
    
    def delete_edge(self, edge: int):
        assert(self._quad_mask[edge//4])

        self.splice_edge(edge, self._oprev(edge))
        self.splice_edge(edge^2, self._oprev(edge^2))
        self._quad_mask[edge//4] = False

    def connect(self, x: int, y: int) -> int:
        """ Connect two edges sharing the same left-face by creating a new quad-edge. """
        z = self.make_edge(self.quad_dst[x//2], self.quad_src[y//2])
        self.splice_edge(z, self._lnext(x))
        self.splice_edge(z^2, y)
        return z
    
    def _triangulate(self, start: int, end: int) -> tuple[int, int]:
        assert(start < end)
        vertices = self.vertices

        if start+3 >= end:
            if start+3 == end:
                # 3 vertices
                i1, i2, i3 = start, start+1, start+2
                a = self.make_edge(i1, i2)
                b = self.make_edge(i2, i3)
                self.splice_edge(a^2, b)
                ori = vec2_orientation(*vertices[start:end])
                if ori < 0:
                    c = self.connect(b, a)
                    return [c^2, c]
                if ori > 0:
                    c = self.connect(b, a)
                return [a, b^2]
            else:
                # 1 or 2 vertices
                a = self.make_edge(start, end-1)
                return [a, a^2]
        
        # 4 or more vertices
        src, dst, nxt = self.quad_src, self.quad_dst, self.quad_nxt
        mid = (start + end) // 2
        
        ldo, ldi = self._triangulate(start, mid)
        rdi, rdo = self._triangulate(mid, end)

        # Compute the lower common tangent of left and right halves.
        while True:
            ldi_src, rdi_src = vertices[src[ldi//2]], vertices[src[rdi//2]]
            if vec2_orientation(rdi_src, ldi_src, vertices[dst[ldi//2]]) > 0: ldi = self._lnext(ldi)
            elif vec2_orientation(ldi_src, vertices[dst[rdi//2]], rdi_src) > 0: rdi = nxt[rdi^2]
            else: break

        base1 = self.connect(rdi^2, ldi)
        if src[ldi//2] == src[ldo//2]: ldo = base1^2
        if src[rdi//2] == src[rdo//2]: rdo = base1

        while True:
            base1_src = vertices[src[base1//2]]
            base1_dst = vertices[dst[base1//2]]

            lcand = nxt[base1^2]
            if vec2_orientation(base1_dst, base1_src, vertices[dst[lcand//2]]) > 0:
                while is_in_circumcircle_of_triangle(base1_dst, base1_src, vertices[dst[lcand//2]], vertices[dst[nxt[lcand]//2]]):
                    t = nxt[lcand]
                    self.delete_edge(lcand)
                    lcand = t
            
            rcand = self._oprev(base1)
            if vec2_orientation(base1_dst, base1_src, vertices[dst[rcand//2]]) > 0:
                while is_in_circumcircle_of_triangle(base1_dst, base1_src, vertices[dst[rcand//2]], vertices[dst[self._oprev(rcand)//2]]):
                    t = self._oprev(rcand)
                    self.delete_edge(rcand)
                    rcand = t

            lvalid = vec2_orientation(base1_dst, base1_src, vertices[dst[lcand//2]]) > 0
            rvalid = vec2_orientation(base1_dst, base1_src, vertices[dst[rcand//2]]) > 0

            if not lvalid and not rvalid: break

            if (
                not lvalid or
                rvalid and is_in_circumcircle_of_triangle(vertices[dst[lcand//2]], vertices[src[lcand//2]], vertices[src[rcand//2]], vertices[dst[rcand//2]])
            ): base1 = self.connect(rcand, base1^2)
            else: base1 = self.connect(base1^2, lcand^2)

        last = end-1

        while src[ldo//2] != start: ldo = nxt[ldo^2]
        while src[rdo//2] != last: rdo = self._lprev(rdo)

        return [ldo, rdo]

    def _prune(self):
        quad_mask = self._quad_mask
        self.quad_src = [x for (i, x) in enumerate(self.quad_src) if quad_mask[i//2]]
        self.quad_dst = [x for (i, x) in enumerate(self.quad_dst) if quad_mask[i//2]]
        self.quad_nxt = [x for (i, x) in enumerate(self.quad_nxt) if quad_mask[i//4]]
        self._quad_mask = [x for x in quad_mask if x]
    
    def triangulate(self):
        if len(self.vertices) > 0:
            self._triangulate(0, len(self.vertices))
            self._prune()