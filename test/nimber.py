
import unittest
from ckp.nimber import *

class TestNimberMul(unittest.TestCase):
    def test_easy(self):
        for i in range(1000):
            self.assertEqual(nimber_mul(i, 0), 0)
            self.assertEqual(nimber_mul(0, i), 0)
            self.assertEqual(nimber_mul(i, 1), i)
            self.assertEqual(nimber_mul(1, i), i)
        
    def test_mul(self):
        self.assertListEqual([nimber_mul(8, i) for i in range(16)], [0, 8, 12, 4, 11, 3, 7, 15, 13, 5, 1, 9, 6, 14, 10, 2])
        self.assertListEqual([nimber_mul(11, i) for i in range(16)], [0, 11, 13, 6, 7, 12, 10, 1, 9, 2, 4, 15, 14, 5, 3, 8])

    def test_mul_2exp(self):
        nimber_mul_2exp.cache_clear()

        self.assertEqual(nimber_mul_2exp(6, 2), 96)
        self.assertEqual(nimber_mul_2exp(7, 7), 222)
        self.assertEqual(nimber_mul_2exp(8, 8), 384)
        self.assertEqual(nimber_mul_2exp(11, 5), 49152)
        self.assertEqual(nimber_mul_2exp(15, 15), 56906)

        self.assertListEqual([nimber_mul_2exp(11, i) for i in range(16)], [2048, 3072, 2816, 3328, 32768, 49152, 45056, 53248, 2256, 3168, 2960, 3552, 32990, 49255, 45205, 53482])

class TestNimber(unittest.TestCase):
    def test_add(self):
        for i in range(100):
            for j in range(100):
                ans = i^j
                self.assertEqual(Nimber(i) + j, ans, f"{i=} {j=}")
                self.assertEqual(i + Nimber(j), ans, f"{i=} {j=}")
                self.assertEqual(Nimber(i) + Nimber(j), ans, f"{i=} {j=}")
    
    def test_mul(self):
        for i in range(100):
            for j in range(100):
                ans = nimber_mul(i, j)
                self.assertEqual(Nimber(i) * j, ans, f"{i=} {j=}")
                self.assertEqual(i * Nimber(j), ans, f"{i=} {j=}")
                self.assertEqual(Nimber(i) * Nimber(j), ans, f"{i=} {j=}")

if __name__ == '__main__':
    unittest.main()