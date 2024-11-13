import unittest
from ckp.number_theory.primality_test import *

class TestIsPrimeNaive(unittest.TestCase):
    def test(self):
        self.assertFalse(is_prime_naive(-1), "-1 is not a prime number")
        self.assertFalse(is_prime_naive(0), "0 is not a prime number")
        self.assertTrue(is_prime_naive(1_000_000_009))
        
        first_200_primes = set([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199])
        for n in range(1, 200):
            self.assertEqual(n in first_200_primes, is_prime_naive(n), f"primality test for {n=}")

class TestIsPrime(unittest.TestCase):
    def test_next_googol(self):
        x = 10**100
        while not is_prime(x): x += 1
        self.assertEqual(x - 10**100, 267)
    
    def test_small(self):
        self.assertFalse(is_prime(-1), "-1 is not a prime number")
        self.assertFalse(is_prime(0), "0 is not a prime number")
        
        for n in range(1, 20000):
            self.assertEqual(is_prime(n), is_prime_naive(n), f"primality test for {n=}")

    def test_large(self):
        self.assertTrue(is_prime(1_000_000_009))
        self.assertTrue(is_prime(205119501451619))
        self.assertTrue(is_prime(492030195575149061012861329941908399488062641190249975515409950003))
        self.assertFalse(is_prime(205119501451619*492030195575149061012861329941908399488062641190249975515409950003))

    def test_miller_rabin_counterexamples(self):
        """ Counter-examples for insufficient Miller-Rabin testing. """
        for ps in [(23,89), (829,1657), (2131,4261), (2251,11251), (151,751,28351), (48781,97561), (611557,1834669), (6763,10627,29947), (1303,16927,157543), (10670053,32010157), (149491,747451,34233211), (399165290221,798330580441), (1287836182261,2575672364521)]:
            prod = 1
            for p in ps:
                self.assertTrue(is_prime(p), f"{p} is a prime number")
                prod *= p
                if prod != p:
                    self.assertFalse(is_prime(prod), f"{prod} is not a prime number")
