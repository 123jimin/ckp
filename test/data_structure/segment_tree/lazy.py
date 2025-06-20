import unittest
from ckp.data_structure.segment_tree.lazy import *

import random
from .util.data_generator import TestDataGenerator

class TestLazyOpSegmentTree(unittest.TestCase):    
    def test_random_ops(self):
        for __ in range(400):
            N = random.randint(1, 128)
            g = TestDataGenerator(N, ['add_to_range', 'get'], lambda: random.randint(-100, 100))

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
