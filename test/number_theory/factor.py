import unittest
from ckp.number_theory.factor import *

from ckp.number_theory.primality_test import is_prime

class TestFactorNaive(unittest.TestCase):
    def test(self):
        self.assertEqual(len(list(factor_naive(-1))), 0)
        self.assertEqual(len(list(factor_naive(0))), 0)
        self.assertEqual(len(list(factor_naive(1))), 0)
        for n in range(2, 5001):
            for k in range(1, 6):
                factors = list(factor_naive(n**k))
                if len(factors) == 1:
                    self.assertTrue(is_prime(n), f"{n} is not a prime number")
                    self.assertEqual(factors[0], n)
                    self.assertEqual(k, 1)
                prod = 1
                for p in factors:
                    self.assertTrue(is_prime(p), f"{p} is not a prime factor of {n}")
                    prod *= p
                self.assertEqual(prod, n**k)

class TestFactorPollardRho(unittest.TestCase):
    def test(self):
        self.assertEqual(len(list(factor_pollard_rho(-1))), 0)
        self.assertEqual(len(list(factor_pollard_rho(0))), 0)
        self.assertEqual(len(list(factor_pollard_rho(1))), 0)
        for n in range(2, 5001):
            for k in range(1, 6):
                factors = list(factor_pollard_rho(n**k))
                if len(factors) == 1:
                    self.assertTrue(is_prime(n), f"{n} is not a prime number")
                    self.assertEqual(factors[0], n)
                    self.assertEqual(k, 1)
                prod = 1
                for p in factors:
                    self.assertTrue(is_prime(p), f"{p} is not a prime factor of {n}")
                    prod *= p
                self.assertEqual(prod, n**k)