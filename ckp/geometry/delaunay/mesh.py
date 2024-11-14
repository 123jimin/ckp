"""
    A quarter-edge is just an integer x. An edge and its dual(rot) shares the same integer.
    - Quad mask indices: x//2
    - Src and dst indices: x and x^1
    - Next indices: x
"""

from ..vector import vec2_orientation, vec2_is_ccw
from ..circumcircle import is_in_circumcircle_of_triangle

class DelaunayMeshData:
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
    quad_nxt_face: list[int] # Next face quarter-edge indices
    
    def __iter__(self):
        shuffled_indices = self.shuffled_indices
        quad_src = self.quad_src
        if shuffled_indices:
            for i in range(0, len(quad_src), 2):
                yield (shuffled_indices[quad_src[i]], shuffled_indices[quad_src[i+1]])
        else:
            for i in range(0, len(quad_src), 2):
                yield (quad_src[i], quad_src[i+1])

def delaunay_mesh_init(vertices: list[tuple[float, float]], already_sorted: bool = False):
    mesh = DelaunayMeshData()

    if already_sorted:
        mesh.shuffled_indices = None
        mesh.vertices = vertices
    else:
        mesh.shuffled_indices = list(range(len(vertices)))
        mesh.shuffled_indices.sort(key=lambda i: vertices[i])
        mesh.vertices = [vertices[i] for i in mesh.shuffled_indices]
    
    mesh._quad_mask = []
    mesh.quad_src = []
    mesh.quad_vert = []

    mesh.quad_nxt_edge = []
    mesh.quad_nxt_face = []

    return mesh

def delaunay_mesh_make_edge(mesh: DelaunayMeshData, src: int, dst: int) -> int:
    x = len(mesh.quad_src)
    vertices = mesh.vertices

    mesh._quad_mask.append(True)
    mesh.quad_src.extend((src, dst))
    mesh.quad_vert.extend((vertices[src], vertices[dst]))
    mesh.quad_nxt_edge.extend((x, x+1))
    mesh.quad_nxt_face.extend((x+1, x))
    
    return x
    
def delaunay_mesh_delete_edge(mesh: DelaunayMeshData, edge: int):
    assert(mesh._quad_mask[edge//2])
    
    nxt, nxt_face = mesh.quad_nxt_edge, mesh.quad_nxt_face

    # splice_edge(edge, oprev(edge))
    y = nxt_face[edge]^1; xf, yf = nxt[edge], nxt[y]; nxt[edge], nxt[y], nxt_face[xf], nxt_face[yf] = yf, xf, nxt_face[yf], nxt_face[xf]
    # splice_edge(edge^1, oprev(edge^1))
    x, y = edge^1, nxt_face[edge^1]^1; xf, yf = nxt[x], nxt[y]; nxt[x], nxt[y], nxt_face[xf], nxt_face[yf] = yf, xf, nxt_face[yf], nxt_face[xf]

    mesh._quad_mask[edge//2] = False

def delaunay_mesh_connect(mesh: DelaunayMeshData, x: int, y: int) -> int:
    """ Connect two edges sharing the same left-face by creating a new quad-edge. """
    z = delaunay_mesh_make_edge(mesh, mesh.quad_src[x^1], mesh.quad_src[y])
    
    nxt, nxt_face = mesh.quad_nxt_edge, mesh.quad_nxt_face

    # splice_edge(z, lnext(x))
    x = nxt_face[x^1]^1; xf, yf = nxt[z], nxt[x]; nxt[z], nxt[x], nxt_face[xf], nxt_face[yf] = yf, xf, nxt_face[yf], nxt_face[xf]
    # splice_edge(z^1, y)
    x = z^1; xf, yf = nxt[x], nxt[y]; nxt[x], nxt[y], nxt_face[xf], nxt_face[yf] = yf, xf, nxt_face[yf], nxt_face[xf]

    return z

def _delaunay_mesh_triangulate(mesh: DelaunayMeshData, start: int, end: int) -> tuple[int, int]:
    assert(start < end)
    vert, src, nxt, nxt_face = mesh.quad_vert, mesh.quad_src, mesh.quad_nxt_edge, mesh.quad_nxt_face

    if start+3 >= end:
        if start+3 == end:
            # 3 vertices
            i1, i2, i3 = start, start+1, start+2
            a = delaunay_mesh_make_edge(mesh, i1, i2)
            b = delaunay_mesh_make_edge(mesh, i2, i3)

            # splice_edge(a^1, b)
            x = a^1; xf, yf = nxt[x], nxt[b]; nxt[x], nxt[b], nxt_face[xf], nxt_face[yf] = yf, xf, nxt_face[yf], nxt_face[xf]
            
            if (ori := vec2_orientation(*mesh.vertices[start:end])): c = delaunay_mesh_connect(mesh, b, a)
            return (c^1, c) if ori < 0 else (a, b^1)
        else:
            # 1 or 2 vertices
            a = delaunay_mesh_make_edge(mesh, start, end-1)
            return (a, a^1)
    
    # 4 or more vertices
    mid = (start + end) // 2
    
    ldo, ldi = _delaunay_mesh_triangulate(mesh, start, mid)
    rdi, rdo = _delaunay_mesh_triangulate(mesh, mid, end)

    # Compute the lower common tangent of left and right halves.
    while True:
        ldi_src, rdi_src = vert[ldi], vert[rdi]
        if vec2_is_ccw(rdi_src, ldi_src, vert[ldi^1]): ldi = nxt_face[ldi^1]^1
        elif vec2_is_ccw(ldi_src, vert[rdi^1], rdi_src): rdi = nxt[rdi^1]
        else: break

    base1 = delaunay_mesh_connect(mesh, rdi^1, ldi)
    if src[ldi] == src[ldo]: ldo = base1^1
    if src[rdi] == src[rdo]: rdo = base1

    while True:
        base1_src, base1_dst = vert[base1], vert[base1^1]

        lcand = nxt[base1^1]
        if vec2_is_ccw(base1_dst, base1_src, vert[lcand^1]):
            lcand_nxt = nxt[lcand]
            while is_in_circumcircle_of_triangle(base1_dst, base1_src, vert[lcand^1], vert[lcand_nxt^1]):
                delaunay_mesh_delete_edge(mesh, lcand); lcand_nxt = nxt[lcand := lcand_nxt]
        
        rcand = nxt_face[base1]^1
        if vec2_is_ccw(base1_dst, base1_src, vert[rcand^1]):
            rcand_nxt = nxt_face[rcand]
            while is_in_circumcircle_of_triangle(base1_dst, base1_src, vert[rcand^1], vert[rcand_nxt]):
                delaunay_mesh_delete_edge(mesh, rcand); rcand_nxt = nxt_face[rcand := rcand_nxt^1]

        lvalid = vec2_is_ccw(base1_dst, base1_src, vert[lcand^1])
        rvalid = vec2_is_ccw(base1_dst, base1_src, vert[rcand^1])

        if not lvalid and not rvalid: break

        if (
            not lvalid or
            rvalid and is_in_circumcircle_of_triangle(vert[lcand^1], vert[lcand], vert[rcand], vert[rcand^1])
        ): base1 = delaunay_mesh_connect(mesh, rcand, base1^1)
        else: base1 = delaunay_mesh_connect(mesh, base1^1, lcand^1)

    last = end-1

    while src[ldo] != start: ldo = nxt[ldo^1]
    while src[rdo] != last: rdo = nxt_face[rdo]

    return (ldo, rdo)

def _delaunay_mesh_prune(mesh: DelaunayMeshData):
    quad_mask = mesh._quad_mask
    mesh.quad_src = [x for (i, x) in enumerate(mesh.quad_src) if quad_mask[i//2]]
    mesh.quad_vert = [x for (i, x) in enumerate(mesh.quad_vert) if quad_mask[i//2]]
    mesh.quad_nxt_edge = [x for (i, x) in enumerate(mesh.quad_nxt_edge) if quad_mask[i//2]]
    mesh.quad_nxt_face = [x for (i, x) in enumerate(mesh.quad_nxt_face) if quad_mask[i//2]]
    mesh._quad_mask = [x for x in quad_mask if x]

def delaunay_mesh_triangulate(mesh: DelaunayMeshData):
    if len(mesh.vertices) > 0:
        _delaunay_mesh_triangulate(mesh, 0, len(mesh.vertices))
        _delaunay_mesh_prune(mesh)