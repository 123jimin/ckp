import unittest
from ckp.data_structure.balanced_tree.aa_tree import *

import random
class TestAATree(unittest.TestCase):
    def test_insert_sequential(self):
        root = None
        for i in range(10):
            root = aa_tree_insert(root, i, f"Data:{i}")
            self.assertEqual(aa_tree_size(root), i+1)
            assert_valid_aa_tree(root)

        for i in range(10):
            self.assertEqual(aa_tree_query(root, i), f"Data:{i}")
        
        self.assertIsNone(aa_tree_query(root, -1))
        self.assertIsNone(aa_tree_query(root, 10))

        root = None
        for i in reversed(range(10)):
            root = aa_tree_insert(root, i, f"Data:{i}")
            self.assertEqual(aa_tree_size(root), 10-i)
            assert_valid_aa_tree(root)
        
        for i in range(10):
            self.assertEqual(aa_tree_query(root, i), f"Data:{i}")
        
        self.assertIsNone(aa_tree_query(root, -1))
        self.assertIsNone(aa_tree_query(root, 10))

    @unittest.skip("incomplete")
    def test_random(self):
        for _ in range(200):
            node = None
            ref = {}
            for __ in range(100):
                match random.randrange(2):
                    case 0:
                        key = random.randint(-100, 100)
                        value = random.randint(-100, 100)
                        node = aa_tree_insert(node, key, value)
                        ref[key] = value
                    case 1:
                        key = random.randint(-100, 100)
                        node = aa_tree_delete(node, key)
                        ref.pop(key, None)
                assert_valid_aa_tree(node)