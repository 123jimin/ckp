
import unittest
from ckp.geometry.circumcircle import *

import math

class TestCircumcircle(unittest.TestCase):
    def test_02389(self):
        a, (acx, acy), ar2 = min_enclosing_circle([(1, 1), (2, 2), (3, 3)])
        self.assertEqual(acx, a*2) # cx == 2
        self.assertEqual(acy, a*2) # cy == 2
        self.assertEqual(ar2, 2*a*a) # r == sqrt(2)

    def test_21182(self):
        for points, ans in [
            ([(1, 0), (-1, 0), (0, 1)], 2),
            ([(1, 1.4), (-1, -1.4), (0, -0.2)], math.hypot(2, 2.8)),
            ([(0, 1.4), (0, -1.4), (1.0, -0.2)], 2.8),
            (
                [(435.249, -539.356), (455.823, -539.257), (423.394, -538.858), (446.507, -539.37), (434.266, -560.631), (445.059, -537.501), (449.65, -513.778), (456.05, -561.329)],
                49.9998293198
            )
        ]:
            a, _, ar2 = min_enclosing_circle(points)
            self.assertAlmostEqual(math.sqrt(ar2)/abs(a), ans/2, places=9, msg=f"{points=}")