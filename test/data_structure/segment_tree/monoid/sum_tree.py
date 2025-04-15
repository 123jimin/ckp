import unittest
from ckp.data_structure.segment_tree.monoid.sum_tree import *
from ckp.number_theory.prime_sieve import prime_sieve_init, prime_sieve_primes

import random, operator, math
from ..test_util import DataGenerator, NaiveMonoidSegmentTree

def compose_perms(a: tuple[int], b: tuple[int]) -> tuple[int]:
    return tuple(b[v] for v in a)

class TestMonoidSumSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            DataGenerator.test(self, N, 400, ['get', 'sum_range', 'sum_all', 'set', 'add_to'],
                               lambda init_values: MonoidSumSegmentTree(init_values, operator.add, 0))

    def test_permutation(self):
        for __ in range(100):
            N = random.randint(1, 128)
            M = 20
            perms = []
            for _ in range(N):
                A = list(range(M))
                random.shuffle(A)
                perms.append(tuple(A))

            e = tuple(range(M))
            tree = MonoidSumSegmentTree(perms, compose_perms, e)

            # TODO: modify DataGenerator to support custom monoids

            total_sum = e
            for p in perms: total_sum = compose_perms(total_sum, p)
            self.assertEqual(tree.sum_range(0, len(perms)), total_sum)
            self.assertEqual(tree.sum_all(), total_sum)

            for _ in range(400):
                i, j = random.randrange(len(perms)), random.randrange(len(perms))
                if i > j: i, j = j, i

                tree_sum = tree.sum_range(i, j)
                ref_sum = e
                for k in range(i, j): ref_sum = compose_perms(ref_sum, perms[k])
                self.assertEqual(tree_sum, ref_sum, f"{i=} {j=}")

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

class TestMaxSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            DataGenerator.test(self, N, 400, ['get', 'sum_range', 'sum_all', 'set'],
                               lambda init_values: MaxSegmentTree(init_values, -999),
                               lambda init_values: NaiveMonoidSegmentTree(init_values, max, -999))
            
class TestGCDSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            DataGenerator.test(self, N, 400, ['get', 'sum_range', 'sum_all', 'set', 'add_to'],
                               GCDSegmentTree,
                               lambda init_values: NaiveMonoidSegmentTree(init_values, math.gcd, 0),
                               min_value = 0, max_value = 1000)