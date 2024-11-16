import unittest
from ckp.data_structure.segment_tree.monoid.add_tree import *

import random
from ..test_util import DataGenerator

class TestAddSegmentTree(unittest.TestCase):
    def test_random(self):
        for __ in range(100):
            N = random.randint(1, 128)
            DataGenerator.test(self, N, 400, ['get', 'set', 'add_to', 'add_to_range'], AddSegmentTree)