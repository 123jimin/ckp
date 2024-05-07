
import unittest
from ckp.geometry.delaunay import *

class TestDelaunay(unittest.TestCase):
    @unittest.skip
    def test_simple(self):
        delaunay_triangulation([(0, 0), (2, 0), (1.4, 0.75), (1.4, -0.75)])