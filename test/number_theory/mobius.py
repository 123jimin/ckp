import unittest
from ckp.number_theory.mobius import *

class TestMobiusNaive(unittest.TestCase):
    def test_small(self):
        for (x, v) in enumerate([1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0, -1, 1, 1, 0, -1, 0, -1, 0], 1):
            self.assertEqual(mobius_naive(x), v, f"testing mu({x})")
    def test_zero(self):
        for x in [24, 25, 27, 28, 32, 36, 40, 44, 45, 48, 49, 50, 52, 54, 56, 60, 63]:
            self.assertEqual(mobius_naive(x), 0, f"testing mu({x})")
    def test_neg(self):
        for x in [30, 42, 66, 70, 78, 102, 105, 110, 114, 130, 138, 154, 165, 170, 174, 182, 186, 190, 195, 222]:
            self.assertEqual(mobius_naive(x), -1, f"testing mu({x})")
        for x in [2310, 2730, 3570, 3990, 4290, 4830, 5610, 6006]:
            self.assertEqual(mobius_naive(x), -1, f"testing mu({x})")