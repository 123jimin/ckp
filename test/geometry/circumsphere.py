
import unittest
from ckp.geometry.circumsphere import *

import math, random

class TestMinEnclosingSphereOfTriangle(unittest.TestCase):
    def test_regular_triangle(self):
        Ca, (Cx, Cy, Cz), Cr2 = min_enclosing_sphere_of_triangle((-1/2, -math.sqrt(3/4), 2), (1/2, -math.sqrt(3/4), 2), (0, 1, 2))
        self.assertAlmostEqual(Cr2, Ca*Ca)
        self.assertAlmostEqual(Cx/Ca, 0)
        self.assertAlmostEqual(Cy/Ca, 0)
        self.assertAlmostEqual(Cz/Ca, 2)

class TestCircumsphereOfTetrahedron(unittest.TestCase):
    def test_regular_tetrahedron(self):
        v1 = (math.sqrt(8/9), 0, -1/3)
        v2 = (-math.sqrt(2/9), math.sqrt(2/3), -1/3)
        v3 = (-math.sqrt(2/9), -math.sqrt(2/3), -1/3)
        v4 = (0, 0, 1)

        Ca, Cp, Cr2 = circumsphere_of_tetrahedron(v1, v2, v3, v4)
        self.assertAlmostEqual(Cr2, Ca*Ca) # R = 1
        for p in Cp:
            self.assertAlmostEqual(p, 0) # P = (0, 0, 0)
    
    def test_random(self):
        for _ in range(1000):
            P = [(random.random()*1000, random.random()*1000, random.random()*1000) for _ in range(4)]
            Ca, (Cx, Cy, Cz), Cr2 = circumsphere_of_tetrahedron(*P)
            r = math.sqrt(Cr2 / (Ca*Ca))
            Cx, Cy, Cz = Cx/Ca, Cy/Ca, Cz/Ca
            for (x, y, z) in P:
                self.assertAlmostEqual(math.hypot(x-Cx, y-Cy, z-Cz), r)

class TestMinEnclosingSphere(unittest.TestCase):
    def test_11930(self):
        Ca, (Cx, Cy, Cz), Cr2 = min_enclosing_sphere([(-5, 0, 0), (5, 0, 0), (0, 3, 4), (4, -3, 0), (2, 2, -2)])
        self.assertAlmostEqual(Cr2, Ca*Ca*25)
        self.assertAlmostEqual(Cx, 0)
        self.assertAlmostEqual(Cy, 0)
        self.assertAlmostEqual(Cz, 0)