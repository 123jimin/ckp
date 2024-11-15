import unittest
from ckp.data_structure.segment_tree.monoid.sum_tree import *
from ckp.number_theory.prime_sieve import prime_sieve_init, prime_sieve_primes

import random, operator
from ..test_util import DataGenerator

class TestMonoidSumSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            DataGenerator.test(self, N, 400, ['get', 'sum_range', 'sum_all', 'set', 'add_to'],
                               lambda init_values: MonoidSumSegmentTree(init_values, operator.add, 0))

    def test_example(self):
        sieve = prime_sieve_init(10_000_000)
        tree = MonoidSumSegmentTree(list(prime_sieve_primes(sieve)), monoid_op=lambda x,y: (x*y)%1_000_000, monoid_zero=1)
        self.assertEqual(len(tree), 664579)
        self.assertEqual(tree.sum_all(), 668970)
        self.assertEqual(tree.sum_range(12345, 67890), 830967)
        tree[20000] = 100
        self.assertEqual(tree.sum_range(12345, 67890), 596900)

class TestSumSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            DataGenerator.test(self, N, 400, ['get', 'sum_range', 'sum_all', 'set', 'add_to'], SumSegmentTree)
