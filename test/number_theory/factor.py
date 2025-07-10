import unittest
from ckp.number_theory.factor import *

from ckp.number_theory.primality_test import is_prime

class TestFactorTrialDivision(unittest.TestCase):
    def test(self):
        self.assertEqual(len(list(factor_trial_division(-1))), 0)
        self.assertEqual(len(list(factor_trial_division(0))), 0)
        self.assertEqual(len(list(factor_trial_division(1))), 0)
        for n in range(2, 5001):
            for k in range(1, 6):
                factors = list(factor_trial_division(n**k))
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

class TestFactor(unittest.TestCase):
    def test_example(self):
        self.assertListEqual(sorted(factor(29841007892689553873)), [3250204337, 9181271329])

class TestDivisors(unittest.TestCase):
    def test_common(self):
        data = [
            (1, [1]),
            (2, [1, 2]),
            (3, [1, 3]),
            (4, [1, 2, 4]),
            (12, [1, 2, 3, 4, 6, 12]),
            (140, [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140]),
        ]

        for n, expected in data:
            actual = sorted(divisors(n))
            self.assertListEqual(actual, expected, f"divisors({n})")
    
    def test_range(self):
        for n in range(1, 2000):
            d_set = set()
            for d in divisors(n):
                self.assertTrue(1 <= d <= n, f"divisors({n}) yielded {d}, which is out of range")
                self.assertEqual(n%d, 0, f"divisors({n}) yielded {d}, which is not divisble by {n}")
                self.assertFalse(d in d_set, f"divisors({n}) returned two of {d}")
                d_set.add(d)
            self.assertTrue(1 in d_set, f"divisors({n}) did not yielded 1")
            self.assertTrue(n in d_set, f"divisors({n}) did not yielded n")