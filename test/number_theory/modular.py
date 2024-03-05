import unittest
from ckp.number_theory.modular import *

import math
from ckp.number_theory import is_prime

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

class TestSqrtModPrime(unittest.TestCase):
    def test(self):
        for p in range(2, 100):
            if not is_prime(p): continue
            for a in range(0, p):
                a_sqrt = sqrt_mod_prime(a, p)
                if a == 0:
                    self.assertEqual(a_sqrt, 0)
                elif a_sqrt == 0:
                    self.assertEqual(legendre_symbol(a, p), -1, f"({a}/{p}) is not -1, but prime_mod_sqrt returned 0")
                else:
                    self.assertEqual(pow(a_sqrt, 2, p), a)

class TestSqrtModPrimePower(unittest.TestCase):
    def test(self):
        for p in range(2, 100):
            if not is_prime(p): continue
            for k in range(1, 10):
                if p**k >= 40_000: break
                quad_res = set()
                for v in range(p**k):
                    vsq = pow(v, 2, p**k)
                    if vsq in quad_res: continue
                    quad_res.add(vsq)
                    sq2 = sqrt_mod_prime_power(vsq, p, k)
                    self.assertEqual(pow(sq2, 2, p**k), vsq, f"Wrong square root {sq2} of {vsq} for mod {p}**{k}")
                for v in range(p**k):
                    if v in quad_res: continue
                    self.assertEqual(sqrt_mod_prime_power(v, p, k), 0, f"There shouldn't be any square root of {v} for mod {p}**{k}")

class TestSqrtMod(unittest.TestCase):
    def test(self):
        for n in range(2, 1000):
            n_factors = Counter(factor(n))
            quad_res = set()
            for v in range(n):
                vsq = pow(v, 2, n)
                if vsq in quad_res: continue
                quad_res.add(vsq)
                sq2 = sqrt_mod(vsq, n)
                self.assertEqual(pow(sq2, 2, n), vsq, f"Wrong square root {sq2} of {vsq} for mod {n}")
            for v in range(n):
                if v in quad_res: continue
                self.assertEqual(sqrt_mod(v, n, n_factors), 0, f"There shouldn't be any square root of {v} for mod {n}")