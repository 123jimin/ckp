import unittest
from ckp.graph_theory.tree.euler_tour import *

import random
from ckp.graph_theory.tree import tree_from_edges, random_tree
from ckp.graph_theory.tree.hld import tree_hld_init

class TestEulerTour(unittest.TestCase):
    def test_simple(self):
        edges = [
            (0, 1), (0, 2), (2, 3), (2, 4), (4, 5),
            (1, 6), (1, 7), (7, 8), (5, 9),
        ]
        tree = tree_from_edges(edges, 0)
        tour = euler_tour(tree)

        self.assertListEqual(tour.visits, [0, 1, 6, 7, 8, 2, 3, 4, 5, 9])
        self.assertListEqual(tour.begin,  [0, 1, 5, 6, 7, 8, 2, 3, 4, 9])
        self.assertListEqual(tour.end,    [10, 5, 10, 7, 10, 10, 3, 5, 5, 10])

    def test_subtree(self):
        for _ in range(200):
            N = random.randrange(1, 200)
            tree = random_tree(N)
            tour = euler_tour(tree)
            sizes = tree_sizes(tree.neighbors, tree.root)

            self.assertEqual(tour.begin[tree.root], 0)
            self.assertEqual(tour.end[tree.root], N)

            for i in range(N):
                self.assertEqual(tour.end[i] - tour.begin[i], sizes[i])

class TestEulerTourSorted(unittest.TestCase):
    def test_simple(self):
        edges = [
            (0, 1), (0, 2), (2, 3), (2, 4), (4, 5),
            (1, 6), (1, 7), (7, 8), (5, 9),
        ]
        tree = tree_from_edges(edges, 0)
        tour = euler_tour_sorted(tree)

        self.assertListEqual(tour.visits, [0, 2, 4, 5, 9, 3, 1, 7, 8, 6])
        self.assertListEqual(tour.begin,  [0, 6, 1, 5, 2, 3, 9, 7, 8, 4])
        self.assertListEqual(tour.end,    [10, 10, 6, 6, 5, 5, 10, 9, 9, 5])
    
    def test_subtree(self):
        for _ in range(200):
            N = random.randrange(1, 200)
            tree = random_tree(N)
            tour = euler_tour_sorted(tree)
            sizes = tree_sizes(tree.neighbors, tree.root)

            self.assertEqual(tour.begin[tree.root], 0)
            self.assertEqual(tour.end[tree.root], N)

            for i in range(N):
                self.assertEqual(tour.end[i] - tour.begin[i], sizes[i])

    def test_hld(self):
        for _ in range(200):
            N = random.randrange(1, 200)
            tree = random_tree(N)
            tour = euler_tour_sorted(tree)
            hld = tree_hld_init(tree)

            for path in hld.paths:
                if len(path) <= 1: continue
                # `tour_inds` must be continuous and ascending.

                tour_inds = [tour.begin[v] for v in path]
                self.assertEqual(tour_inds[-1], tour_inds[0] + len(path) - 1)
                self.assertListEqual(tour_inds, list(range(tour_inds[0], tour_inds[-1]+1)))