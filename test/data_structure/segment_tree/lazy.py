import unittest
from ckp.data_structure.segment_tree.lazy import *

import random

class TestLazySumSegmentTree(unittest.TestCase):
    def test_sum_random(self):
        for __ in range(100):
            N = random.randint(1, 128)

            arr = [random.randint(-100, 100) for _ in range(N)]
            tree = LazySumSegmentTree(arr)

            self.assertEqual(len(tree), N)

            for _ in range(100):
                i = random.randrange(0, N)
                j = random.randrange(0, N)

                if i >= j:
                    self.assertEqual(tree.reduce_range(i, j), 0, f"summing on an empty range [{i}, {j})")
                else:
                    s = sum(arr[i:j])
                    self.assertEqual(tree.reduce_range(i, j), s, f"summing on the range [{i}, {j})")
    
    def test_add_to_random(self):
        for __ in range(100):
            N = random.randint(1, 128)

            arr = [random.randint(-100, 100) for _ in range(N)]
            tree = LazySumSegmentTree(arr)

            self.assertEqual(len(tree), N)

            for _ in range(100):
                op = random.choice(['add_to', 'get', 'set' 'reduce'])

                match op:
                    case 'add_to':
                        i = random.randrange(0, N)
                        j = random.randrange(0, N)
                        k = random.randint(-100, 100)

                        for v in range(i, j): arr[v] += k
                        tree.add_to_range(i, j, k)
                    case 'get':
                        i = random.randrange(0, N)
                        self.assertEqual(tree[i], arr[i], f"getting {i=}")
                    case 'set':
                        i = random.randrange(0, N)
                        v = random.randint(-100, 100)
                        arr[i] = v
                        tree[i] = v
                    case 'reduce':
                        i = random.randrange(0, N-1)
                        j = random.randrange(i+1, N)
                        
                        s = sum(arr[i:j])
                        self.assertEqual(tree.reduce_range(i, j), s, f"summing on the range [{i}, {j})")