"""
    Algorithms based on https://github.com/mkirc/delaunay, but with minimal data structure.
"""

from .mesh import *

def delaunay_triangulation(points: list[tuple[float|int, float|int]]):
    mesh = DelaunayMesh(points)
    mesh.triangulate()

    yield from mesh