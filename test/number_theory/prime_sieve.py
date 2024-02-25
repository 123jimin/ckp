import unittest
from ckp.number_theory.prime_sieve import *

from ckp.number_theory import is_prime_naive

class TestPrimeSieve(unittest.TestCase):
    def test_single_alloc(self):
        sieve = PrimeSieve(100000)
        for n in range(10001): self.assertEqual(is_prime_naive(n), sieve.is_prime(n), f"primality test for {n=}")

    def test_list_primes(self):
        sieve = PrimeSieve(100000)
        for p in sieve.primes():
            self.assertTrue(sieve.is_prime(p), f"dismatch between primes() and is_prime() for {p=}")
            self.assertTrue(is_prime_naive(p), f"{p} is not a prime number")
    
    def test_multi_extend(self):
        sieve = PrimeSieve(100)
        sieve.extend(151)
        sieve.extend(500)
        sieve.extend(5000000)

        for n in range(100001): self.assertEqual(is_prime_naive(n), sieve.is_prime(n), f"primality test for {n=}")
