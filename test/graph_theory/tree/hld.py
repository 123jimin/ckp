import unittest
from ckp.graph_theory.tree.hld import *

from ckp.graph_theory.tree import Tree

class TestHLD(unittest.TestCase):
    def test_simple(self):
        tree = Tree.from_edges([(0, 1), (0, 2), (2, 3), (2, 4), (4, 5), (1, 6), (1, 7), (7, 8), (5, 9)], root=0)
        hld = TreeHLD(tree)
        self.assertEqual(len(hld.paths), 4)
        self.assertEqual(len(hld.path_index), len(tree))
        self.assertSetEqual(set("".join(str(v) for v in path) for path in hld.paths), {"02459", "178", "6", "3"})
        self.assertTrue(all(ind is not None for ind in hld.path_index))