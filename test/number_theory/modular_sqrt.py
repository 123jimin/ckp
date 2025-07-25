import unittest
from ckp.number_theory.modular_sqrt import *

from ckp.number_theory import is_prime, factor

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
                    self.assertEqual(pow(a_sqrt, 2, p), a, f"sqrt_mod_prime({a}, {p}) returned {a_sqrt}, which is wrong.")

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
        for n in range(2, 500):
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