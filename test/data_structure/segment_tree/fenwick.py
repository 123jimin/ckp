import unittest
from ckp.data_structure.segment_tree.fenwick import *

import random
from .util.data_generator import TestDataGenerator

FENWICK_TREE_OPS = ['set', 'add_to', 'get', 'sum_range', 'sum_all']

class TestFenwickTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            TestDataGenerator.test(self, N, 400, FENWICK_TREE_OPS, FenwickTree)