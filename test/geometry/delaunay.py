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
    
    def test_07890(self):
        example_1 = [
            (17, 41),
            (0, 34),
            (24, 19),
            (8, 28),
            (14, 12),
            (45, 5),
            (27, 31),
            (41, 11),
            (42, 45),
            (36, 27),
        ]

        self.assertDelaunayTriangulation(example_1, [
            (0, 1), (0, 3), (0, 6), (0, 8),
            (1, 3), (1, 4),
            (2, 3), (2, 4), (2, 6), (2, 7), (2, 9),
            (3, 4), (3, 6),
            (4, 5), (4, 7),
            (5, 7), (5, 8),
            (6, 8), (6, 9),
            (7, 8), (7, 9),
            (8, 9),
        ])