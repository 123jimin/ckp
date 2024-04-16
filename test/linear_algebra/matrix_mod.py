import unittest
from ckp.linear_algebra.matrix_mod import *

import random

class TestMatrixMod(unittest.TestCase):
    def test_ident_mul(self):
        for _ in range(100):
            N = random.randint(1, 16)
            M = random.randint(1, 1000)
            I = matrix_id(N)
            v = [random.randint(-10, 10) for _ in range(N)]
            
            self.assertListEqual(matrix_column_mul_mod(I, v, M), [ve%M for ve in v])

    def test_random_mul(self):
        for _ in range(100):
            N = random.randint(1, 16)
            M = random.randint(1, 1000)
            A = [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]
            B = [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]
            v = [random.randint(-10, 10) for _ in range(N)]
            
            with_mul = matrix_column_mul_mod(matrix_mul_mod(A, B, M), v, M)
            without_mul = matrix_column_mul_mod(A, matrix_column_mul_mod(B, v, M), M)

            self.assertListEqual(with_mul, without_mul)