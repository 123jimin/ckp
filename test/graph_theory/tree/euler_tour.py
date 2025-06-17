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

    def test_random(self):
        for _ in range(200):
            N = random.randrange(1, 200)
            tree = random_tree(N)
            tour = euler_tour(tree)
            self.assertEqual(tour.begin[tree.root], 0)
            self.assertListEqual([tour.visits[tour.begin[v]] for v in range(N)], list(range(N)))

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
    
    def test_random(self):
        for _ in range(200):
            N = random.randrange(1, 200)
            tree = random_tree(N)
            tour = euler_tour_sorted(tree)
            self.assertEqual(tour.begin[tree.root], 0)
            self.assertListEqual([tour.visits[tour.begin[v]] for v in range(N)], list(range(N)))

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
                self.assertEqual(tour_inds[-1], tour_inds[0] + len(path) - 1, f"HLD path {tree=} {N=} {path=} {tour_inds=}")
                self.assertListEqual(tour_inds, list(range(tour_inds[0], tour_inds[-1]+1)))