import unittest

from ckp.graph_theory.tree import *

class TestTreeParentsAndDepths(unittest.TestCase):
    def test_simple(self):
        neighbors = [[2], [3], [0, 3], [1, 2, 4], [3]]
        parents, depths = tree_parents_and_depths(neighbors)
        self.assertListEqual(parents, [-1, 3, 0, 2, 3])
        self.assertListEqual(depths, [0, 3, 1, 2, 3])

class TestTreeSizes(unittest.TestCase):
    def test_simple(self):
        neighbors = [[2], [3], [0, 3], [1, 2, 4], [3]]
        sizes = tree_sizes(neighbors)
        self.assertListEqual(sizes, [5, 1, 4, 3, 1])