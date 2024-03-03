import unittest
from ckp.data_structure.sorted_containers.sorted_dict import *

import random

class SortedSortedDict(unittest.TestCase):
    def test_random_insertion_and_sorted_order(self):
        d = SortedDict()

        items = [(random.randint(1, 100000), random.randint(1, 100000)) for _ in range(10000)]
        for (key, value) in items: d[key] = value

        keys = sorted(set(key for (key, _) in items))
        d_keys = [key for key in d]
            
        self.assertListEqual(keys, d_keys)