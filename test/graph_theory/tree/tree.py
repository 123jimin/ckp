import unittest
from ckp.graph_theory.tree.tree import *

import random
from ckp.graph_theory.tree.random import random_tree, random_tree_edges

class TestTreeWithRoot(unittest.TestCase):
    def test_simple(self):
        neighbors = [[1], [0, 2, 3], [1], [1]]
        t1 = tree_from_neighbors(neighbors, 0)
        assert_valid_tree(t1)

        t2 = tree_with_root(t1, 2)
        assert_valid_tree(t2)

        self.assertEqual(t1.root, 0)
        self.assertEqual(t2.root, 2)

class TestTreeConstructors(unittest.TestCase):
    def test_random_tree(self):
        for _ in range(1000):
            N = random.randint(1, 1000)
            tree = random_tree(N)
            assert_valid_tree(tree)

    def test_random_edges(self):
        for _ in range(1000):
            N = random.randint(1, 1000)
            edges = random_tree_edges(N)
            tree = tree_from_edges(edges, random.randrange(N))
            assert_valid_tree(tree)

            for (u, v) in edges:
                self.assertTrue(tree.parents[u] == v or tree.parents[v] == u)

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
    
    def test_random(self):
        for _ in range(500):
            N = random.randint(1, 500)
            tree = random_tree(N)
            tree_sizes(tree)
            assert_valid_tree(tree)

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