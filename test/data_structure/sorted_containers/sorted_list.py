import unittest
from ckp.data_structure.sorted_containers.sorted_list import *

import random

class TestSortedList(unittest.TestCase):
    def test_random_insertion_and_sorted_order(self):
        l = SortedList()

        keys = [random.randint(1, 100000) for _ in range(10000)]
        for key in keys: l.add(key)

        sorted_keys = sorted(keys)
        self.assertListEqual(sorted_keys, list(l))
    
    def test_random_insertion_and_deletion(self):
        l = SortedList()
        reference_dict = dict()

        for _ in range(100000):
            key = random.randint(1, 100000)
            action = random.randint(1, 2)

            if action == 1:
                value = random.randint(1, 100000)
                l.add(value)

                if value in reference_dict:
                    reference_dict[value] += 1
                else:
                    reference_dict[value] = 1
            else:
                if key in reference_dict:
                    self.assertTrue(key in l)
                    reference_dict[key] -= 1
                    l.remove(key)
                    if reference_dict[key] == 0:
                        del reference_dict[key]
                else:
                    self.assertTrue(key not in l)
        
        self.assertEqual(len(l), sum(reference_dict.values()))