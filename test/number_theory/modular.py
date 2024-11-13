import unittest
from ckp.number_theory.modular import *

import math, random
from ckp.number_theory import is_prime, factor

class TestSolveLinearMod(unittest.TestCase):
    def test(self):
        def solve_naive(a, b, m):
            if m == 1: return 0
            a %= m
            b %= m
            for x in range(m):
                if (a*x + b) % m == 0: return x
            return -1
        
        for _ in range(5_000):
            a = random.randint(-100, 100)
            b = random.randint(-100, 100)
            m = random.randint(1, 1000)
            self.assertEqual(solve_linear_mod(a, b, m), solve_naive(a, b, m), f"{a=}, {b=}, {m=}")

class TestCountZeroMod(unittest.TestCase):
    def test(self):
        def sum_naive(a, b, m, l, r):
            return sum((a*x + b)%m == 0 for x in range(l, r))
        
        for _ in range(5_000):
            a = random.randint(-100, 100)
            b = random.randint(-100, 100)
            m = random.randint(1, 100)
            l = random.randint(-1000, 1000)
            r = random.randint(-1000, 1000)

            self.assertEqual(count_zero_mod(a, b, m, l, r), sum_naive(a, b, m, l, r), f"{a=}, {b=}, {m=}, {l=}, {r=}")

class TestSumFloorLinear(unittest.TestCase):
    def test(self):
        def sum_naive(a, b, m, n):
            return sum((a*x + b) // m for x in range(n))
        
        for _ in range(5_000):
            a = random.randint(-100, 100)
            b = random.randint(-100, 100)
            while (m := random.randint(-100, 100)) == 0: pass
            n = random.randint(0, 100)

            self.assertEqual(sum_floor_linear(a, b, m, n), sum_naive(a, b, m, n), f"{a=}, {b=}, {m=}, {n=}")

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

class TestLegendreSymbol(unittest.TestCase):
    def test_small(self):
        self.assertEqual(legendre_symbol(-2, 2), 0)
        self.assertEqual(legendre_symbol(-1, 2), 1)
        self.assertEqual(legendre_symbol(0, 2), 0)
        self.assertEqual(legendre_symbol(1, 2), 1)
        self.assertEqual(legendre_symbol(2, 2), 0)
        for p in range(3, 1000, 2):
            if not is_prime(p): continue
            v = [False] * p
            for i in range(p): v[(i*i)%p] = True
            if p > 2: self.assertEqual(2*sum(v)-1, p, f"Quadratic residue array for {p=}")
            for a in range(-2*p, 2*p+1):
                expected = (1 if v[a%p] else -1) if a%p else 0
                self.assertEqual(legendre_symbol(a, p), expected, f"({a} / {p})")

class TestJacobiSymbol(unittest.TestCase):
    def test_one(self):
        for x in range(1, 100):
            self.assertEqual(jacobi_symbol(x, 1), 1)
        for x in range(1, 100, 2):
            self.assertEqual(jacobi_symbol(1, x), 1)
    
    def test_small(self):
        for n in range(3, 500, 2):
            n_factors = list(factor(n))
            for a in range(-2*n, 2*n+1):
                expected = 1
                for p in n_factors: expected *= legendre_symbol(a, p)
                self.assertEqual(jacobi_symbol(a, n), expected, f"({a} / {n})")

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

class TestZMod(unittest.TestCase):
    def test_op_zmod(self):
        a = ZMod(3, 4)
        b = ZMod(2, 4)
        
        self.assertNotEqual(a, b)
        self.assertEqual(a + b, ZMod(1, 4))
        self.assertEqual(a - b, ZMod(1, 4))
        self.assertEqual(b - a, ZMod(3, 4))
        self.assertEqual(a * b, ZMod(2, 4))

        a += b
        self.assertEqual(a, ZMod(1, 4))

        a -= b
        self.assertEqual(a, ZMod(3, 4))

        a *= b
        self.assertEqual(a, ZMod(2, 4))

    def test_op_int(self):
        a = ZMod(3, 5)

        self.assertIs(int(a), 3)
        self.assertIsNot(int(a), 8)
        self.assertEqual(a, 8)
        self.assertNotEqual(a, 2)
        self.assertEqual(a + 4, 2)
        self.assertEqual(a - 123, 0)
        self.assertEqual(a * 9, 2)
        self.assertEqual(a ** 3, 2)

    def test_list(self):
        l = [1, 2, 3, 4, 5]
        i = ZMod(3, len(l))

        self.assertEqual(l[i], 4)