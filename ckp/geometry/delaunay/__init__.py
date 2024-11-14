"""
    Algorithms based on https://github.com/mkirc/delaunay, but with minimal data structure.
"""

from .mesh import delaunay_mesh_init, delaunay_mesh_triangulate

def delaunay_triangulation(points: list[tuple[float|int, float|int]]):
    mesh = delaunay_mesh_init(points)
    delaunay_mesh_triangulate(mesh)
    
    yield from mesh