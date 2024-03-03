import unittest
from ckp.data_structure.segment_tree.simple import *

import random

class TestSimpleSegmentTree(unittest.TestCase):
    def test_sum_random(self):
        for __ in range(100):
            N = random.randint(1, 128)

            arr = [random.randint(-100, 100) for _ in range(N)]
            tree = SimpleSegmentTree(arr)

            self.assertEqual(len(tree), N)

            for _ in range(100):
                i = random.randrange(0, N)
                j = random.randrange(0, N)

                if i >= j:
                    self.assertEqual(tree.reduce_range(i, j), 0, f"summing on an empty range [{i}, {j})")
                else:
                    s = sum(arr[i:j])
                    self.assertEqual(tree.reduce_range(i, j), s, f"summing on the range [{i}, {j})")