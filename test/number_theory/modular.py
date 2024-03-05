import unittest
from ckp.number_theory.modular import *

import math

class TestCombModPrime(unittest.TestCase):
    def test_common(self):
        self.assertEqual(comb_mod_prime(5, 2, 3), 1)
        self.assertEqual(comb_mod_prime(30, 10, 3), 0)
        self.assertEqual(comb_mod_prime(30, 3, 3), 1)
        self.assertEqual(comb_mod_prime(100, 45, 7), 0)
        self.assertEqual(comb_mod_prime(100, 45, 13), 2)

    def test_small(self):
        for p in (2, 3, 5, 7, 11, 13):
            for n in range(100):
                for k in range(n+1):
                    nCk = math.comb(n, k)

                    self.assertEqual(comb_mod_prime(n, k, p), nCk % p, f"C({n}, {k}) % {p}")

class TestChineseMod(unittest.TestCase):
    def test_common(self):
        self.assertEqual(chinese_mod((2, 7)), 2)
        self.assertEqual(chinese_mod((2, 3), (3, 5), (2, 7)), 23)