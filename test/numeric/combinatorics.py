import unittest
from ckp.numeric.combinatorics import *

import math

def assertAlmostEqualFunc(testcase: unittest.TestCase, actual: float, expected: float, message=None):
    delta = abs(expected * 1e-9)
    if delta == 0: delta = abs(expected)

    testcase.assertGreaterEqual(actual, expected - delta, message)
    testcase.assertLessEqual(actual, expected + delta, message)

class TestLogFallingFactorial(unittest.TestCase):
    assertAlmostEqual = assertAlmostEqualFunc

    def test_small(self):
        self.assertEqual(log_falling_factorial(0, 0), 0)
        for n in range(1, 50):
            for k in range(n+1):
                self.assertAlmostEqual(log_falling_factorial(n, k), math.log(math.factorial(n)) - math.log(math.factorial(n-k)), f"log_falling_factorial({n}, {k})")

    def test_small_k(self):
        for i in range(10, 110, 10):
            n = 10 ** i
            self.assertAlmostEqual(log_falling_factorial(n, 0), 0, f"log_falling_factorial(10**{i}, 0)")

            p = 0
            for j in range(100):
                p += math.log(n - j)
                self.assertAlmostEqual(log_falling_factorial(n, j+1), p, f"log_falling_factorial(10**{i}, {j+1})")

class TestLogComb(unittest.TestCase):
    assertAlmostEqual = assertAlmostEqualFunc

    def test_small(self):
        self.assertEqual(log_comb(0, 0), 0)
        for n in range(1, 50):
            for k in range(n+1):
                self.assertAlmostEqual(log_comb(n, k), math.log(math.comb(n, k)), f"log_comb({n}, {k})")
    
    def test_small_k(self):
        for i in range(10, 110, 10):
            n = 10 ** i
            self.assertAlmostEqual(log_comb(n, 0), 0, f"log_comb(10**{i}, 0)")

            p = 0
            for j in range(100):
                p += math.log(n - j) - math.log(j+1)
                self.assertAlmostEqual(log_comb(n, j+1), p, f"log_comb(10**{i}, {j+1})")
        
    def test_large(self):
        data_10_9 = [
            20.723265836946411156,
            192.12824575138859612,
            1708.5872031890774613,
            14811.137158958081390,
            125123.68053748311561,
            1021022.3616788467501,
            7907247.2860384416653,
            56001525.3818861413608,
        ]

        for i, value in enumerate(data_10_9):
            self.assertAlmostEqual(log_comb(10**9, 10**i), value, f"log_comb(10**9, 10**{i})")

class TestHarmonicNumber(unittest.TestCase):
    assertAlmostEqual = assertAlmostEqualFunc

    def test_exact(self):
        self.assertEqual(harmonic_number(0), 0)
        self.assertEqual(harmonic_number(1), 1)
        self.assertEqual(harmonic_number(2), 1.5)

    def test_small(self):
        s = 0
        for n in range(1, 1001):
            s += 1/n
            self.assertAlmostEqual(harmonic_number(n), s, f"H({n})")

    def test_large(self):
        self.assertAlmostEqual(harmonic_number(10**8), 18.99789641385389832441711039)
        self.assertAlmostEqual(harmonic_number(10**10), 23.6030665948919897007855933)
        self.assertAlmostEqual(harmonic_number(10**50), 115.706470314603817061506084)