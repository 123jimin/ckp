import unittest
from ckp.geometry.half_plane_intersection import *

import random

class TestHalfPlaneIntersection(unittest.TestCase):
    def test_empty(self):
        self.assertListEqual(half_plane_intersection([]), [])
    
    @unittest.skip
    def test_single_degenerate(self):
        for i in range(-3, 4):
            if i >= 0: self.assertListEqual(half_plane_intersection([(0, 0, i)]), [], f"Full space when {i=}.")
            else: self.assertIsNone(half_plane_intersection([(0, 0, i)]), f"Empty when {i=}.")

    @unittest.skip
    def test_single(self):
        for _ in range(100):
            while True:
                a = random.randint(-100, 100)
                b = random.randint(-100, 100)
                c = random.randint(-100, 100)
                if a or b: break

            self.assertListEqual(half_plane_intersection([(a, b, c)]), [0], f"Single plane {a=} {b=} {c=}.")
    
    @unittest.skip
    def test_two_degenerate(self):
        for _ in range(100):
            while True:
                a = random.randint(-100, 100)
                b = random.randint(-100, 100)
                c = random.randint(-100, 100)
                if a or b: break

            for i in range(-3, 4):
                result = half_plane_intersection([(a, b, c), (0, 0, i)])
                if i >= 0: self.assertListEqual(result, [0], f"Single plane {a=} {b=} {c=} with full space after it.")
                else: self.assertIsNone(result, f"Single plane {a=} {b=} {c=} with an empty space after it.")
                
                result = half_plane_intersection([(0, 0, i), (a, b, c)])
                if i >= 0: self.assertListEqual(result, [0], f"Single plane {a=} {b=} {c=} with full space before it.")
                else: self.assertIsNone(result, f"Single plane {a=} {b=} {c=} with an empty space before it.")
    
    def test_surrounding(self):
        # TODO: Create half-planes surrounding a central random point.
        pass

    def test_unique(self):
        # TODO: Create half-planes intersecting at a point.
        pass