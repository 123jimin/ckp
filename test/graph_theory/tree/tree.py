import unittest

from ckp.graph_theory.tree.tree import *

class TestTreeParentsAndDepthsFromNeighbors(unittest.TestCase):
    def test_simple(self):
        neighbors = [[2], [3], [0, 3], [1, 2, 4], [3]]
        parents, depths = tree_parents_and_depths_from_neighbors(neighbors)
        self.assertListEqual(parents, [-1, 3, 0, 2, 3])
        self.assertListEqual(depths, [0, 3, 1, 2, 3])

class TestTreeSizesFromChildren(unittest.TestCase):
    def test_simple(self):
        self.assertListEqual(tree_sizes_from_children([[]]), [1])
        self.assertListEqual(tree_sizes_from_children([[1], []], 0), [2, 1])
        self.assertListEqual(tree_sizes_from_children([[], [0]], 1), [1, 2])

        children = [[2], [], [3], [1, 4], []]
        sizes = tree_sizes_from_children(children)
        self.assertListEqual(sizes, [5, 1, 4, 3, 1])

class TestTreeCentroids(unittest.TestCase):
    def _test_from_neighbors(self, neighbors: list[list[int]], centroids: list[int]):
        tree = tree_from_neighbors(neighbors)

        self.assertListEqual(sorted(tree_centroids_from_children(tree.children, tree.root, None)), centroids)
        self.assertListEqual(sorted(tree_centroids(tree)), centroids)

    def test_simple(self):
        self._test_from_neighbors([[]], [0])
        self._test_from_neighbors([[1], [0]], [0, 1])
        self._test_from_neighbors([[1, 2], [0], [0]], [0])
        self._test_from_neighbors([[2], [3], [0, 3], [1, 2, 4], [3]], [3])
        self._test_from_neighbors([[1], [0, 2], [1, 3], [2]], [1, 2])