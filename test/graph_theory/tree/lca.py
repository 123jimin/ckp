import unittest

from ckp.graph_theory.tree.lca import *
from ckp.graph_theory.tree import Tree

class TestLCA(unittest.TestCase):
    def test_11438(self):
        tree = Tree.from_edges([(0, 1), (0, 2), (1, 3), (2, 6), (5, 1), (2, 7), (3, 8), (1, 4), (4, 10), (6, 12), (9, 3), (10, 14), (11, 4), (13, 6)])
        lca = TreeLCA(tree)
        
        self.assertEqual(lca.get(5, 10), 1)
        self.assertEqual(lca.get(9, 8), 3)
        self.assertEqual(lca.get(1, 5), 1)
        self.assertEqual(lca.get(6, 5), 0)
        self.assertEqual(lca.get(7, 12), 2)
        self.assertEqual(lca.get(7, 14), 0)

        for v in range(len(tree)):
            self.assertEqual(lca.get(0, v), 0)