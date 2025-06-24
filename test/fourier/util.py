
import unittest
from ckp.fourier.util import *

class TestMinCommonConvolutionSizePowerOf2(unittest.TestCase):
    def test(self):
        self.assertEqual(min_convolution_size_power(13, 21), 6)
        self.assertEqual(min_convolution_size_power(64, 1), 6)
        self.assertEqual(min_convolution_size_power(512, 513), 10)

class TestBitReverseTable(unittest.TestCase):
    def test_small(self):
        bit_reverse_table.cache_clear()

        self.assertEqual(bit_reverse_table(0), [0])
        self.assertEqual(bit_reverse_table(1), [0, 1])
        self.assertEqual(bit_reverse_table(2), [0, 2, 1, 3])
        self.assertEqual(bit_reverse_table(3), [0, 4, 2, 6, 1, 5, 3, 7])
    
    def test_check_reversal(self):
        for L in range(10, 15):
            bit_reverse_table.cache_clear()
            table = bit_reverse_table(L)
            self.assertEqual(len(table), (1 << L), f"len(table) for {L=}")

            for i in range(1 << L):
                ti = table[i]
                self.assertEqual(table[ti], i, f"convolution for {L=}, {i=}")

                j = 0
                for _ in range(L):
                    j = j*2 + ti%2
                    ti //= 2
                
                self.assertEqual(j, i, f"double reversal for {L=}, {i=}")