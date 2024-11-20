import unittest
from ckp.numeric.combinatorics import *

import math

class TestLogComb(unittest.TestCase):
    def test_small(self):
        self.assertEqual(log_comb(0, 0), 1)
        for n in range(1, 20):
            for k in range(n+1):
                self.assertAlmostEqual(log_comb(n, k), math.log(math.comb(n, k)), places=10)
                
class TestNormalizedLogComb(unittest.TestCase):
    def test_small(self):
        self.assertEqual(normalized_log_comb(0, 0), 1)
        for n in range(1, 20):
            for k in range(n+1):
                self.assertAlmostEqual(normalized_log_comb(n, k), math.log(math.comb(n, k))/n, places=10)

class TestHarmonicSeries(unittest.TestCase):
    def test_small(self):
        self.assertEqual(harmonic_series(0), 0)
        self.assertEqual(harmonic_series(1), 1)
        self.assertEqual(harmonic_series(2), 1.5)
        self.assertAlmostEqual(harmonic_series(3), 1.5 + 1/3)