import unittest
from ckp.geometry.convex_hull import *

TEST_CASES = [
    (
        [],
        [],
    ),
    (
        [(0, 0)],
        [0],
    ),
    (
        [(0, 0), (1, 1)],
        [0, 1],
    ),
    (
        [(-7, 10), (-3, -7), (5, 3), (2, 5), (9, 4)],
        [0, 1, 4],
    ),
    (
        [(0, 0), (1, 1), (3, 1), (2, 3), (4, 4), (0, 4), (4, 0)],
        [0, 6, 4, 5],
    ),
    (
        [(6, 2), (-9, 7), (-4, -3), (10, -2), (-1, 10), (9, -1), (-7, -4), (1, -7)],
        [1, 6, 7, 3, 4],
    ),
    (
        [(1, 2), (2, 3), (3, 1), (5, 3), (4, 4), (0, 0), (3, 3), (2, 1), (1, 4)],
        [5, 2, 3, 4, 8],
    ),
]


class TestConvexHull(unittest.TestCase):
    def _assert_same_hull(self, a: list[int], b: list[int], message: str):
        message = f"testing hull {a=} and {b=}, {message}"

        self.assertEqual(len(a), len(b), message)
        self.assertSetEqual(set(a), set(b), message)

        if not a: return

        for i in range(len(a)):
            if a[i] == b[0]:
                self.assertListEqual(a[i:] + a[:i], b, message)
                return
        
        self.fail(f"{message}")

    def _test_function(self, f, name: str):
        for points, expected in TEST_CASES:
            hull = f(points)
            self._assert_same_hull(hull, expected, f"{points=}")

    def test_default(self):
        self._test_function(convex_hull, "convex_hull")
        
    def test_andrew(self):
        self._test_function(convex_hull_andrew, "convex_hull_andrew")