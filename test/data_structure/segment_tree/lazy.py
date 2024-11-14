import unittest
from ckp.data_structure.segment_tree.lazy import *

import random
from .test_util import DataGenerator

class TestLazyOpSegmentTree(unittest.TestCase):    
    def test_random_ops(self):
        for __ in range(400):
            N = random.randint(1, 128)
            g = DataGenerator(N, ['add_to_range', 'get'])

            arr = g.list()
            tree = LazyOpSegmentTree(arr)

            self.assertEqual(len(tree), N)

            for _ in range(400):
                match g.op():
                    case ('add_to_range', i, j, v):
                        for k in range(i, j): arr[k] += v
                        tree.add_to_range(i, j, v)
                    case ('get', i):
                        self.assertEqual(tree[i], arr[i], f"getting {i=}")

class TestLazySumSegmentTree(unittest.TestCase):
    def test_sum_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            g = DataGenerator(N, [])

            arr = g.list()
            tree = LazySumSegmentTree(arr)

            self.assertEqual(len(tree), N)

            for _ in range(100):
                i, j = g.index(), g.index()

                if i >= j:
                    self.assertEqual(tree.reduce_range(i, j), 0, f"summing on an empty range [{i}, {j})")
                else:
                    s = sum(arr[i:j])
                    self.assertEqual(tree.reduce_range(i, j), s, f"summing on the range [{i}, {j})")
    
    def test_random_ops(self):
        for __ in range(400):
            N = random.randint(1, 128)
            g = DataGenerator(N, ['add_to_range', 'get', 'set', 'reduce_range'])

            arr = g.list()
            tree = LazySumSegmentTree(arr)

            self.assertEqual(len(tree), N)

            for _ in range(400):
                match g.op():
                    case ('add_to_range', i, j, v):
                        for k in range(i, j): arr[k] += v
                        tree.add_to_range(i, j, v)
                    case ('get', i):
                        self.assertEqual(tree[i], arr[i], f"getting {i=}")
                    case ('set', i, v):
                        arr[i] = v
                        tree[i] = v
                    case ('reduce_range', i, j):
                        s = sum(arr[i:j])
                        self.assertEqual(tree.reduce_range(i, j), s, f"summing on the range [{i}, {j})")
