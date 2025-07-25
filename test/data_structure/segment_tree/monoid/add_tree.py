import unittest
from ckp.data_structure.segment_tree.monoid.add_tree import *

import random
from ..util.data_generator import TestDataGenerator

ADD_SEGMENT_TREE_OPS = ['set', 'add_to', 'add_to_range', 'get']

class TestAddSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            TestDataGenerator.test(self, N, 400, ADD_SEGMENT_TREE_OPS, AddSegmentTree)