
import unittest
from ckp.geometry.circumsphere import *

import math, random

class TestCircumsphereOfTetrahedron(unittest.TestCase):
    def test_regular_tetrahedron(self):
        v1 = (math.sqrt(8/9), 0, -1/3)
        v2 = (-math.sqrt(2/9), math.sqrt(2/3), -1/3)
        v3 = (-math.sqrt(2/9), -math.sqrt(2/3), -1/3)
        v4 = (0, 0, 1)

        Ca, Cp, Cr2 = circumsphere_of_tetrahedron(v1, v2, v3, v4)
        self.assertAlmostEqual(Ca*Ca, Cr2) # R = 1
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