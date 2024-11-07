"""
    A quarter-edge is just an integer x. An edge and its dual(rot) shares the same integer.
    - Quad mask indices: x//2
    - Src and dst indices: x and x^1
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
        'quad_vert',
        'quad_nxt_edge',
        'quad_nxt_face',
    )

    vertices: list[tuple[float, float]]
    shuffled_indices: list[int]|None # None when vertices are not shuffled.

    _quad_mask: list[bool] # To mark deleted edges (`False`)
    quad_src: list[int] # Source vertex indices for a quarter-edge
    quad_vert: list[tuple[float, float]] # self.vertices[self.quad_src[x]], to reduce indirection.
    
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
        self.quad_vert = []

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
        
    def make_edge(self, src: int, dst: int) -> int:
        x = len(self.quad_src)
        vertices = self.vertices

        self._quad_mask.append(True)
        self.quad_src.extend((src, dst))
        self.quad_vert.extend((vertices[src], vertices[dst]))
        self.quad_nxt_edge.extend((x, x+1))
        self.quad_nxt_face.extend((x+1, x))
        
        return x
    
    def delete_edge(self, edge: int):
        assert(self._quad_mask[edge//2])
        
        nxt, nxt_face = self.quad_nxt_edge, self.quad_nxt_face

        # splice_edge(edge, oprev(edge))
        y = nxt_face[edge]^1; xf, yf = nxt[edge], nxt[y]; nxt[edge], nxt[y], nxt_face[xf], nxt_face[yf] = yf, xf, nxt_face[yf], nxt_face[xf]
        # splice_edge(edge^1, oprev(edge^1))
        x, y = edge^1, nxt_face[edge^1]^1; xf, yf = nxt[x], nxt[y]; nxt[x], nxt[y], nxt_face[xf], nxt_face[yf] = yf, xf, nxt_face[yf], nxt_face[xf]

        self._quad_mask[edge//2] = False

    def connect(self, x: int, y: int) -> int:
        """ Connect two edges sharing the same left-face by creating a new quad-edge. """
        z = self.make_edge(self.quad_src[x^1], self.quad_src[y])
        
        nxt, nxt_face = self.quad_nxt_edge, self.quad_nxt_face

        # splice_edge(z, lnext(x))
        x = nxt_face[x^1]^1; xf, yf = nxt[z], nxt[x]; nxt[z], nxt[x], nxt_face[xf], nxt_face[yf] = yf, xf, nxt_face[yf], nxt_face[xf]
        # splice_edge(z^1, y)
        x = z^1; xf, yf = nxt[x], nxt[y]; nxt[x], nxt[y], nxt_face[xf], nxt_face[yf] = yf, xf, nxt_face[yf], nxt_face[xf]

        return z

    def _triangulate(self, start: int, end: int) -> tuple[int, int]:
        assert(start < end)
        vert, src, nxt, nxt_face = self.quad_vert, self.quad_src, self.quad_nxt_edge, self.quad_nxt_face

        if start+3 >= end:
            if start+3 == end:
                # 3 vertices
                i1, i2, i3 = start, start+1, start+2
                a = self.make_edge(i1, i2)
                b = self.make_edge(i2, i3)

                # splice_edge(a^1, b)
                x = a^1; xf, yf = nxt[x], nxt[b]; nxt[x], nxt[b], nxt_face[xf], nxt_face[yf] = yf, xf, nxt_face[yf], nxt_face[xf]
                
                ori = vec2_orientation(*self.vertices[start:end])
                if ori: c = self.connect(b, a)
                return [c^1, c] if ori < 0 else [a, b^1]
            else:
                # 1 or 2 vertices
                a = self.make_edge(start, end-1)
                return [a, a^1]
        
        # 4 or more vertices
        mid = (start + end) // 2
        
        ldo, ldi = self._triangulate(start, mid)
        rdi, rdo = self._triangulate(mid, end)

        # Compute the lower common tangent of left and right halves.
        while True:
            ldi_src, rdi_src = vert[ldi], vert[rdi]
            if vec2_orientation(rdi_src, ldi_src, vert[ldi^1]) > 0: ldi = nxt_face[ldi^1]^1
            elif vec2_orientation(ldi_src, vert[rdi^1], rdi_src) > 0: rdi = nxt[rdi^1]
            else: break

        base1 = self.connect(rdi^1, ldi)
        if src[ldi] == src[ldo]: ldo = base1^1
        if src[rdi] == src[rdo]: rdo = base1

        while True:
            base1_src = vert[base1]
            base1_dst = vert[base1^1]

            lcand = nxt[base1^1]
            if vec2_orientation(base1_dst, base1_src, vert[lcand^1]) > 0:
                while is_in_circumcircle_of_triangle(base1_dst, base1_src, vert[lcand^1], vert[nxt[lcand]^1]):
                    t = nxt[lcand]
                    self.delete_edge(lcand)
                    lcand = t
            
            rcand = nxt_face[base1]^1
            if vec2_orientation(base1_dst, base1_src, vert[rcand^1]) > 0:
                while is_in_circumcircle_of_triangle(base1_dst, base1_src, vert[rcand^1], vert[nxt_face[rcand]]):
                    t = nxt_face[rcand]^1
                    self.delete_edge(rcand)
                    rcand = t

            lvalid = vec2_orientation(base1_dst, base1_src, vert[lcand^1]) > 0
            rvalid = vec2_orientation(base1_dst, base1_src, vert[rcand^1]) > 0

            if not lvalid and not rvalid: break

            if (
                not lvalid or
                rvalid and is_in_circumcircle_of_triangle(vert[lcand^1], vert[lcand], vert[rcand], vert[rcand^1])
            ): base1 = self.connect(rcand, base1^1)
            else: base1 = self.connect(base1^1, lcand^1)

        last = end-1

        while src[ldo] != start: ldo = nxt[ldo^1]
        while src[rdo] != last: rdo = nxt_face[rdo]

        return [ldo, rdo]

    def _prune(self):
        quad_mask = self._quad_mask
        self.quad_src = [x for (i, x) in enumerate(self.quad_src) if quad_mask[i//2]]
        self.quad_vert = [x for (i, x) in enumerate(self.quad_vert) if quad_mask[i//2]]
        self.quad_nxt_edge = [x for (i, x) in enumerate(self.quad_nxt_edge) if quad_mask[i//2]]
        self.quad_nxt_face = [x for (i, x) in enumerate(self.quad_nxt_face) if quad_mask[i//2]]
        self._quad_mask = [x for x in quad_mask if x]
    
    def triangulate(self):
        if len(self.vertices) > 0:
            self._triangulate(0, len(self.vertices))
            self._prune()