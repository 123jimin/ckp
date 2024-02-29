
import unittest
from ckp.fourier.complex import *

class TestComplexNaiveDFT(unittest.TestCase):
    def test_correlation(self):
        x = [23, 4, 95, 20, 17, 94, 63, 44, 13, 96] * 2
        y = [87, 54, 13, 18, 61, 24, 17, 94, 53, 2][::-1]

        fft = ComplexNaiveDFT(len(x))
        self.assertEqual(len(fft), len(x))
        fx = fft(x)
        self.assertEqual(len(fx), len(fft))
        fy = fft(y)
        self.assertEqual(len(fy), len(fft))
        for i in range(len(fft)): fx[i] *= fy[i]
        z = fft(fx, fy, inverse=True)
        self.assertIs(z, fy)
        
        self.assertEqual(max(round(abs(x)) for x in z), 28886)

class TestComplexCooleyTukeyFFT(unittest.TestCase):
    def test_correlation(self):
        x = [23, 4, 95, 20, 17, 94, 63, 44, 13, 96] * 2
        y = [87, 54, 13, 18, 61, 24, 17, 94, 53, 2][::-1]

        fft = ComplexCooleyTukeyFFT.get_common_fft(x, y)
        self.assertEqual(len(fft), 32)
        fx = fft(x)
        self.assertEqual(len(fx), 32)
        fy = fft(y)
        self.assertEqual(len(fy), 32)
        for i in range(len(fft)): fx[i] *= fy[i]
        z = fft(fx, fy, inverse=True)
        self.assertIs(z, fy)
        
        self.assertEqual(max(round(abs(x)) for x in z), 28886)