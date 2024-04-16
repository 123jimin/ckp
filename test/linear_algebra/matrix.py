import unittest
from ckp.linear_algebra.matrix import *

import random

class TestMatrix(unittest.TestCase):
    def test_ident_mul(self):
        for _ in range(100):
            N = random.randint(1, 16)
            I = matrix_id(N)
            v = [random.randint(-10, 10) for _ in range(N)]
            
            self.assertListEqual(matrix_column_mul(I, v), v)
            self.assertListEqual(Matrix(I)(v), v)

    def test_random_mul(self):
        for _ in range(100):
            N = random.randint(1, 16)
            A = [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]
            B = [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]
            v = [random.randint(-10, 10) for _ in range(N)]
            
            with_mul = matrix_column_mul(matrix_mul(A, B), v)
            without_mul = matrix_column_mul(A, matrix_column_mul(B, v))

            self.assertListEqual(with_mul, without_mul)

            A = Matrix(A)
            B = Matrix(B)

            with_class_mul = (A*B)(v)
            without_class_mul = A(B(v))

            self.assertListEqual(with_class_mul, without_class_mul)
            self.assertListEqual(with_class_mul, with_mul)

            v = column_vec(v)

            with_class_mul = ((A*B)*v)
            without_class_mul = (A*(B*v))

            self.assertEqual(with_class_mul.size(), (N, 1))
            self.assertEqual(without_class_mul.size(), (N, 1))

            with_class_mul = [row[0] for row in with_class_mul.rows]
            without_class_mul = [row[0] for row in without_class_mul.rows]
            
            self.assertListEqual(with_class_mul, without_class_mul)
            self.assertListEqual(with_class_mul, with_mul)
