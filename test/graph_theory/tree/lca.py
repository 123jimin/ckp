import unittest

from ckp.graph_theory.tree.lca import *
from ckp.graph_theory.tree import tree_from_edges

class TestLCA(unittest.TestCase):
    def test_11438(self):
        tree = tree_from_edges([(0, 1), (0, 2), (1, 3), (2, 6), (5, 1), (2, 7), (3, 8), (1, 4), (4, 10), (6, 12), (9, 3), (10, 14), (11, 4), (13, 6)])
        lca = tree_lca_init(tree)
        
        self.assertEqual(tree_lca_query(lca, 5, 10), 1)
        self.assertEqual(tree_lca_query(lca, 9, 8), 3)
        self.assertEqual(tree_lca_query(lca, 1, 5), 1)
        self.assertEqual(tree_lca_query(lca, 6, 5), 0)
        self.assertEqual(tree_lca_query(lca, 7, 12), 2)
        self.assertEqual(tree_lca_query(lca, 7, 14), 0)

        for v in range(len(tree)):
            self.assertEqual(tree_lca_query(lca, 0, v), 0)