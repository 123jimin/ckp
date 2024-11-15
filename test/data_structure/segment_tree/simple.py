import unittest
from ckp.data_structure.segment_tree.simple import *
from ckp.number_theory import PrimeSieve

import random
from .test_util import DataGenerator

class TestSimpleSumSegmentTree(unittest.TestCase):
    def test_sum_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            g = DataGenerator(N, [])

            arr = g.list()
            tree = SimpleSumSegmentTree(arr)

            self.assertEqual(len(tree), N)

            for _ in range(100):
                i, j = g.index(), g.index()

                if i >= j:
                    self.assertEqual(tree.reduce_range(i, j), 0, f"summing on an empty range [{i}, {j})")
                else:
                    s = sum(arr[i:j])
                    self.assertEqual(tree.reduce_range(i, j), s, f"summing on the range [{i}, {j})")

    def test_ops(self):
        for __ in range(400):
            N = random.randint(1, 128)
            g = DataGenerator(N, ['get', 'set', 'sum_range', 'sum_all'])

            arr = g.list()
            tree = SimpleSumSegmentTree(arr)

            self.assertEqual(len(tree), N)

            for _ in range(400):
                match g.op():
                    case ('get', i):
                        self.assertEqual(tree[i], arr[i], f"getting {i=}")
                    case ('set', i, v):
                        arr[i] = v
                        tree[i] = v
                    case ('sum_range', i, j):
                        s = sum(arr[i:j])
                        self.assertEqual(tree.reduce_range(i, j), s, f"summing on the range [{i}, {j})")
                    case ('sum_all',):
                        s = sum(arr)
                        self.assertEqual(tree.reduce(), s, f"sum of whole")

                        