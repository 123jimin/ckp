import unittest
from ckp.data_structure.segment_tree.ring import *

import random
from ..util.data_generator import TestDataGenerator

RING_SEGMENT_TREE_OPS = ['set', 'set_range', 'add_to', 'add_to_range', 'mul_to', 'mul_to_range', 'mul_add_to', 'mul_add_to_range', 'get', 'sum_range', 'sum_all']

class TestAddSegmentTree(unittest.TestCase):
    @unittest.skip
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            TestDataGenerator.test(self, N, 400, RING_SEGMENT_TREE_OPS, NumberRingSegmentTree)