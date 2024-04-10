
import unittest
from ckp.misc.matrix_chain_ordering.naive import *

class TestMatrixChainOrderingNaive(unittest.TestCase):
    def test(self):
        self.assertEqual(matrix_chain_min_cost_naive([5, 3, 2, 6]), 90)
        self.assertEqual(matrix_chain_min_cost_naive([10, 30, 5, 60]), 4500)
        self.assertEqual(matrix_chain_min_cost_naive([30, 35, 15, 5, 10, 20, 25]), 15125)