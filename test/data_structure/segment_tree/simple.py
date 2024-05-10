import unittest
from ckp.data_structure.segment_tree.simple import *
from ckp.number_theory import PrimeSieve

import random
from .data_generator import DataGenerator

class TestSimpleSegmentTree(unittest.TestCase):
    def test_sum_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            g = DataGenerator(N)

            arr = g.list()
            tree = SimpleSegmentTree(arr)

            self.assertEqual(len(tree), N)

            for _ in range(100):
                i, j = g.index(), g.index()

                if i >= j:
                    self.assertEqual(tree.reduce_range(i, j), 0, f"summing on an empty range [{i}, {j})")
                else:
                    s = sum(arr[i:j])
                    self.assertEqual(tree.reduce_range(i, j), s, f"summing on the range [{i}, {j})")
    
    def test_example(self):
        tree = SimpleSegmentTree(list(PrimeSieve(10_000_000).primes()), op=lambda x,y: (x*y)%1_000_000, e=1)
        self.assertEqual(len(tree), 664579)
        self.assertEqual(tree.reduce(), 668970)
        self.assertEqual(tree.reduce_range(12345, 67890), 830967)
        tree[20000] = 100
        self.assertEqual(tree.reduce_range(12345, 67890), 596900)

class TestSimpleSumSegmentTree(unittest.TestCase):
    def test_sum_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            g = DataGenerator(N)

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
            g = DataGenerator(N, ['get', 'set', 'reduce', 'reduce_all'])

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
                    case ('reduce', i, j):
                        s = sum(arr[i:j])
                        self.assertEqual(tree.reduce_range(i, j), s, f"summing on the range [{i}, {j})")
                    case ('reduce_all',):
                        s = sum(arr)
                        self.assertEqual(tree.reduce(), s, f"sum of whole")

                        