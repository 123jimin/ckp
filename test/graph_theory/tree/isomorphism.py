import unittest

from ckp.graph_theory.tree.isomorphism import *
from ckp.graph_theory.tree.tree import tree_from_neighbors

class TestTreeIsIsomorphicTo(unittest.TestCase):
    def test_simple(self):
        self.assertTrue(tree_is_isomorphic_to(
            tree_from_neighbors([[1], [0, 2], [1]]),
            tree_from_neighbors([[1, 2], [0], [0]]),
        ))

        self.assertTrue(tree_is_isomorphic_to(
            tree_from_neighbors([[1], [0, 2, 4], [1, 3], [2], [1, 5, 6], [4], [4, 7], [6]]),
            tree_from_neighbors([[2], [3], [0, 4], [1, 5], [2, 5, 6], [3, 4, 7], [4], [5]]),
        ))