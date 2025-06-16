import unittest
from ckp.data_structure.segment_tree.ring import *

import random
from ckp.data_structure.segment_tree.naive import NaiveRingSegmentTree
from ..util.data_generator import TestDataGenerator

RING_SEGMENT_TREE_OPS = ['set', 'set_range', 'add_to', 'add_to_range', 'mul_to', 'mul_to_range', 'mul_add_to', 'mul_add_to_range', 'get', 'sum_range', 'sum_all']

class TestNumberRingSegmentTree(unittest.TestCase):
    def test_random(self):
        for _ in range(100):
            N = random.randint(1, 128)
            TestDataGenerator.test(self, N, 400, RING_SEGMENT_TREE_OPS, NumberRingSegmentTree)

class TestZModRingSegmentTree(unittest.TestCase):
    def test_random(self):
        for _ in range(100):
            N = random.randint(1, 128)
            M = random.randint(2, 10000)
            TestDataGenerator.test(
                self, N, 400, RING_SEGMENT_TREE_OPS, lambda init_values: ZModRingSegmentTree(M, init_values),
                ref_tree_maker=lambda init_values: NaiveRingSegmentTree(
                    init_values, lambda a, b: (a + b) % M, lambda a, b: (a * b) % M, 0, 1,
                ),
                value_generator=lambda: random.randrange(M),
            )