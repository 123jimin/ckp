import unittest
from ckp.number_theory.misc import *

import random, math

class TestIterateIdiv(unittest.TestCase):
    def test_common(self):
        data = [
            (1, [(1, 1, 2)]),
            (2, [(2, 1, 2), (1, 2, 3)]),
            (3, [(3, 1, 2), (1, 2, 4)]),
            (4, [(4, 1, 2), (2, 2, 3), (1, 3, 5)]),
        ]
        for (n, expected) in data:
            res = list(iterate_idiv(n))
            self.assertListEqual(res, expected, f"iterate_idiv({n})")

    def test_range(self):
        for n in range(2, 1_000):
            prev_a = None
            prev_c = None
            for (a, b, c) in iterate_idiv(n):
                self.assertLess(b, c, f"the range must be non-empty for {a=} {n=}")
                if prev_a is None:
                    self.assertEqual(a, n, f"first a of iterate_idiv({n}")
                    self.assertEqual(b, 1, f"first b of iterate_idiv({n})")
                    self.assertEqual(c, 2, f"first c of iterate_idiv({n})")
                else:
                    self.assertLess(a, prev_a, f"a should be decreasing for {n=}")
                    self.assertEqual(prev_c, b, f"the range must be touching for {a=} {n=}")

                prev_a, prev_c = a, c
            self.assertEqual(prev_a, 1, f"last a of iterate_idiv({n})")
            self.assertEqual(prev_c, n+1, f"last c of iterate_idiv({n})")

class TestExtendedGCD(unittest.TestCase):
    def test_gcd(self):
        for _ in range(10000):
            x, y = random.randint(1, 100000), random.randint(1, 100000)
            g, a, b = extended_gcd(x, y)
            real_g = math.gcd(x, y)
            self.assertEqual(g, real_g, f"{x=} {y=}")
            self.assertEqual(a*x + b*y, g, f"{x=} {y=}")
            if g != x and g != y:
                self.assertLessEqual(abs(a), y // (2*g), f"{x=} {y=}")
                self.assertLessEqual(abs(b), x // (2*g), f"{x=} {y=}")