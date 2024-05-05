import unittest
from ckp.misc.lis import *

import random

class TestLIS(unittest.TestCase):
    def test_simple(self):
        self.assertListEqual(lis([]), [])
        self.assertListEqual(lis([42]), [0])
        self.assertListEqual(lis([1, 2, 3, 4, 5]), [0, 1, 2, 3, 4])
        self.assertEqual(len(lis([5, 4, 3, 2, 1])), 1)
        self.assertEqual(len(lis([10, 20, 30, 40, 50, 60, 70, 110, 80, 100, 120, 0, 90])), 10)
    
    def test_random_increasing(self):
        for _ in range(2000):
            N = random.randint(2, 200)
            A = [random.randint(-1000, 1000) for _ in range(N)]
            B = lis(A)
            self.assertTrue(1 <= len(B) <= N)
            self.assertTrue(all(0 <= i < N for i in B))
            for i in range(len(B)-1):
                self.assertLess(B[i], B[i+1])
                self.assertLessEqual(A[B[i]], A[B[i+1]])
    
    def test_random_at_least(self):
        for _ in range(3000):
            N = random.randint(1, 10)
            M = random.randint(0, 10)

            A = [random.randint(-1000, 1000) for _ in range(N+M)]
            S = sorted(random.sample(range(len(A)), N))
            B = sorted(A[i] for i in S)
            for i, b in enumerate(B): A[S[i]] = b
            C = lis(A)

            self.assertGreaterEqual(len(C), N)