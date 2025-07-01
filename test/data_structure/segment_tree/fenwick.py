import unittest
from ckp.data_structure.segment_tree.fenwick import *

import random
from .util.data_generator import TestDataGenerator

FENWICK_TREE_OPS = ['set', 'add_to', 'get', 'sum_range', 'sum_all']

class TestFenwickTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            TestDataGenerator.test(self, N, 400, FENWICK_TREE_OPS, FenwickTree)

class TestOffline2DFenwickTree(unittest.TestCase):
    def test_simple(self):
        tree = Offline2DFenwickTree([(1, 1), (2, 4), (3, 3)])
        self.assertEqual(tree.sum_rect(0, 4, 0, 5), 3)
    
    def test_random_small(self):
        for __ in range(100):
            N = random.randint(1, 64)
            P = [(random.randint(-100, 100), random.randint(-100, 100)) for _ in range(N)]
            tree = Offline2DFenwickTree(P)

            for _ in range(400):
                x1, x2 = sorted(random.sample(range(-100, 101), 2))
                y1, y2 = sorted(random.sample(range(-100, 101), 2))
                true_value = sum(x1 <= x < x2 and y1 <= y < y2 for x, y in P)
                self.assertEqual(tree.sum_rect(x1, x2, y1, y2), true_value)

if __name__ == "__main__":
    unittest.main()