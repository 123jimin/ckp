import unittest
from ckp.data_structure.segment_tree.monoid.sum_tree import *
from ckp.number_theory.prime_sieve import prime_sieve_init, prime_sieve_primes

import random, operator, math
from ..util.data_generator import TestDataGenerator
from ckp.data_structure.segment_tree.naive import NaiveMonoidSegmentTree

def compose_perms(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(b[v] for v in a)

SUM_SEGMENT_TREE_OPS = ['set', 'add_to', 'get', 'sum_range', 'sum_all']

class TestMonoidSumSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            TestDataGenerator.test(self, N, 400, SUM_SEGMENT_TREE_OPS, lambda init_values: MonoidSumSegmentTree(init_values, operator.add, 0))

    def test_permutation(self):
        for __ in range(100):
            N = random.randint(1, 64)
            M = 12
            e = tuple(range(M))
            TestDataGenerator.test(self, N, 400, SUM_SEGMENT_TREE_OPS,
                lambda init_values: MonoidSumSegmentTree(init_values, compose_perms, e),
                lambda init_values: NaiveMonoidSegmentTree(init_values, compose_perms, e),
                value_generator = lambda: tuple(random.sample(range(M), M)))
    
    def test_permutation_simple(self):
        init_values = [(1, 0, 2)] + [(0, 1, 2)]*3 + [(0, 2, 1)]
        tree = MonoidSumSegmentTree(init_values, compose_perms, (0, 1, 2))
        self.assertEqual(tree.sum_all(), (2, 0, 1))

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
            TestDataGenerator.test(self, N, 400, SUM_SEGMENT_TREE_OPS, SumSegmentTree)

class TestMaxSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            TestDataGenerator.test(self, N, 400, SUM_SEGMENT_TREE_OPS,
                               lambda init_values: MaxSegmentTree(init_values, -999),
                               lambda init_values: NaiveMonoidSegmentTree(init_values, max, -999))
            
class TestGCDSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            TestDataGenerator.test(self, N, 400, SUM_SEGMENT_TREE_OPS,
                GCDSegmentTree,
                lambda init_values: NaiveMonoidSegmentTree(init_values, math.gcd, 0),
                value_generator = lambda: random.randint(0, 10000))