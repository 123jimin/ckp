import unittest
from ckp.geometry.delaunay import *

def normalize_delaunay_triangulation(vertices):
    return sorted((min(v, w), max(v, w)) for (v, w) in delaunay_triangulation(vertices))

class TestDelaunay(unittest.TestCase):
    def assertDelaunayTriangulation(self, vertices, expected, msg = None):
        self.assertListEqual(normalize_delaunay_triangulation(vertices), expected, msg)

    def test_simple(self):
        self.assertDelaunayTriangulation([(0, 0), (0, 1), (1, 0)], [(0, 1), (0, 2), (1, 2)])
        self.assertDelaunayTriangulation([(0, 0), (2, 0), (1.4, 0.75), (1.4, -0.75)], [(0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
        self.assertDelaunayTriangulation([(0, 0), (2, 0), (1.8, 0.75), (1.8, -0.75)], [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])