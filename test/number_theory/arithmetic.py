import unittest
from ckp.number_theory.arithmetic import *

from collections import Counter
from ckp.number_theory import factor, divisors

class TestSumDivisors(unittest.TestCase):
    def test(self):
        for i in range(1, 10000):
            manual_sum = sum(divisors(i))
            func_sum = sum_divisors(i)
            self.assertEqual(func_sum, manual_sum, f"test for {i=}")
            func_sum = sum_divisors(i, factor(i))
            self.assertEqual(func_sum, manual_sum, f"test for {i=}, with factors provided")

class TestNumDivisors(unittest.TestCase):
    def test(self):
        for i in range(1, 10000):
            manual_len = len(list(divisors(i)))
            func_len = num_divisors(i)
            self.assertEqual(func_len, manual_len, f"test for {i=}")
            func_len = num_divisors(i, factor(i))
            self.assertEqual(func_len, manual_len, f"test for {i=}, with factors provided")

class TestEulerPhi(unittest.TestCase):
    def test(self):
        A = [
            0, 1, 1, 2, 2, 4, 2, 6, 4, 6,
            4, 10, 4, 12, 6, 8, 8, 16, 6, 18,
            8, 12, 10, 22, 8, 20, 12, 18, 12, 28,
            8, 30, 16, 20, 16, 24, 12, 36, 18, 24,
            16, 40, 12, 42, 20, 24, 22, 46, 16, 42,
            20, 32, 24, 52, 18, 40, 24, 36, 28, 58,
            16, 60, 30, 36, 32, 48, 20, 66, 32, 44,
        ]
        for i, v in enumerate(A):
            if i == 0: continue
            self.assertEqual(euler_phi(i), v, f"Incorrect euler_phi({i})")
            if i >= 2:
                self.assertEqual(euler_phi(i, factor(i)), v,  f"Incorrect euler_phi({i}) with factors provided")