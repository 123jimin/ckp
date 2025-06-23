import unittest
from ckp.graph_theory.tree.distance_tree import *

P08872_EDGES = [
    (0, 8, 4), (8, 2, 2), (2, 7, 4),
    (5, 11, 3), (5, 1, 7), (1, 3, 1),
    (1, 9, 5), (10, 6, 3), (2, 1, 2),
    (1, 6, 2), (10, 4, 2),
]

class TestDistanceTreeConstructors(unittest.TestCase):
    def test_simple(self):
        tree = distance_tree_from_edges([])
        self.assertEqual(len(tree), 1)

        assert_valid_distance_tree(tree)
        self.assertListEqual(tree.root_distances, [0])
        self.assertListEqual(tree.parent_distances, [0])
        
        tree = distance_tree_from_edges([(0, 1, 42)])
        self.assertEqual(len(tree), 2)

        assert_valid_distance_tree(tree)
        self.assertListEqual(tree.root_distances, [0, 42])
        self.assertListEqual(tree.parent_distances, [0, 42])

    def test_08872(self):
        tree = distance_tree_from_edges(P08872_EDGES)
        self.assertEqual(len(tree), 12)

        assert_valid_distance_tree(tree)
        self.assertListEqual(tree.root_distances, [0, 8, 6, 9, 15, 15, 10, 10, 4, 13, 13, 18])
        self.assertListEqual(tree.parent_distances, [0, 2, 2, 1, 2, 7, 2, 4, 4, 5, 3, 3])

class TestDistanceTreeMaxDepths(unittest.TestCase):
    def test_simple(self):
        tree = distance_tree_from_edges([])
        max_depths = distance_tree_max_depths(tree)
        self.assertListEqual(max_depths, [0])

        tree = distance_tree_from_edges([(0, 1, 42)])
        max_depths = distance_tree_max_depths(tree)
        self.assertListEqual(max_depths, [42, 0])

    def test_08872(self):
        tree = distance_tree_from_edges(P08872_EDGES)        
        max_depths = distance_tree_max_depths(tree)
        self.assertListEqual(max_depths, [18, 10, 12, 0, 0, 3, 5, 0, 14, 0, 2, 0])