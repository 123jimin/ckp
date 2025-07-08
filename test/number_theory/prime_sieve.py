import unittest
from ckp.number_theory.prime_sieve import *

from collections import Counter
from ckp.number_theory.primality_test import is_prime, is_prime_naive

class TestPrimeSieve(unittest.TestCase):
    def test_single_alloc(self):
        sieve = PrimeSieve(100000)
        for n in range(10001): self.assertEqual(is_prime_naive(n), sieve.is_prime(n), f"primality test for {n=}")

    def test_list_primes(self):
        sieve = PrimeSieve(100000)
        for p in sieve.primes():
            self.assertTrue(sieve.is_prime(p), f"mismatch between primes() and is_prime() for {p=}")
            self.assertTrue(is_prime_naive(p), f"{p} is not a prime number")
    
    def test_multi_extend(self):
        sieve = PrimeSieve(100)
        sieve.extend(151)
        sieve.extend(500)
        sieve.extend(5000000)

        for n in range(100001): self.assertEqual(is_prime_naive(n), sieve.is_prime(n), f"primality test for {n=}")

    def test_is_prime_large(self):
        sieve = PrimeSieve(1_000_000)
        for n in range(3, 1_000_001, 2): self.assertEqual(is_prime(n), sieve.is_prime(n), f"primality test for {n=}")

    @unittest.skip("stress test")
    def test_is_prime_large(self):
        sieve = PrimeSieve(10_000_000)
        for n in range(3, 10_000_001, 2): self.assertEqual(is_prime(n), sieve.is_prime(n), f"primality test for {n=}")

    def test_factor(self):
        sieve = PrimeSieve(100000)
        self.assertEqual(Counter(sieve.factor(42)), Counter([2, 3, 7]))
        self.assertEqual(Counter(sieve.factor(16384)), Counter([2]*14))
    
    def test_example(self):
        sieve = PrimeSieve(10**6)
        self.assertEqual(len(list(sieve.primes())), 78498)
        
        self.assertTrue(sieve.is_prime(999983))
        self.assertFalse(sieve.is_prime(999991))
        self.assertEqual(len(list(sieve.primes())), 78498)

        self.assertTrue(sieve.is_prime(1010129))
        self.assertEqual(len(list(sieve.primes())), 79257)

    @unittest.skip("stress test")
    def test_example_large(self):
        sieve = PrimeSieve(10**7)
        self.assertEqual(len(list(sieve.primes())), 664579)
        self.assertEqual(sum(sieve.primes()), 3203324994356)

        self.assertTrue(sieve.is_prime(9999991))
        self.assertFalse(sieve.is_prime(9999997))
        self.assertEqual(len(list(sieve.primes())), 664579)

        self.assertTrue(sieve.is_prime(10000019))
        self.assertEqual(len(list(sieve.primes())), 664580)