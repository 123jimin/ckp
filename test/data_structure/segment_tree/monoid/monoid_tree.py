import unittest
from ckp.data_structure.segment_tree.monoid.monoid_tree import *

import random
from ..util.data_generator import TestDataGenerator

MONOID_SEGMENT_TREE_OPS = ['set', 'add_to', 'add_to_range', 'get', 'sum_range', 'sum_all']

class TestNumberSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            TestDataGenerator.test(self, N, 400, MONOID_SEGMENT_TREE_OPS, NumberSegmentTree)

class TestSimpleNumberSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            TestDataGenerator.test(self, N, 400, MONOID_SEGMENT_TREE_OPS, SimpleNumberSegmentTree)