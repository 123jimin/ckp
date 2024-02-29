
import unittest
from ckp.fourier.util import *

class TestMinCommonConvolutionSizePowerOf2(unittest.TestCase):
    def test(self):
        self.assertEqual(min_convolution_size_power(13, 21), 6)
        self.assertEqual(min_convolution_size_power(64, 1), 6)
        self.assertEqual(min_convolution_size_power(512, 513), 10)