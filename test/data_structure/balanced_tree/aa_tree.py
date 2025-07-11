import unittest
from ckp.data_structure.balanced_tree.aa_tree import *

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
