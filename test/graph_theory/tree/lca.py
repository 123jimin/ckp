import unittest
from ckp.graph_theory.tree.lca import *

import random
from ckp.graph_theory.tree import tree_from_edges, random_tree

def tree_lca_naive(tree: TreeData, x, y):
    dx, dy = tree.depths[x], tree.depths[y]
    while dx > dy: dx, x = dx-1, tree.parents[x]
    while dy > dx: dy, y = dy-1, tree.parents[y]

    while x != y:
        x, y = tree.parents[x], tree.parents[y]

    return x

class TestLCA(unittest.TestCase):
    def test_one(self):
        tree = tree_from_edges([])
        lca = tree_lca_init(tree)

        self.assertEqual(tree_lca_query(lca, 0, 0), 0)
    
    def test_two(self):
        for root in (0, 1):
            tree = tree_from_edges([(0, 1)], root)
            lca = tree_lca_init(tree)

            self.assertEqual(tree_lca_query(lca, 0, 0), 0)
            self.assertEqual(tree_lca_query(lca, 0, 1), root)
            self.assertEqual(tree_lca_query(lca, 1, 0), root)
            self.assertEqual(tree_lca_query(lca, 1, 1), 1)

    def test_random(self):
        for _ in range(200):
            N = random.randrange(1, 64)
            tree = random_tree(N)
            lca = tree_lca_init(tree)

            for x in range(N):
                for y in range(N):
                    p = tree_lca_naive(tree, x, y)
                    self.assertEqual(tree_lca_query(lca, x, y), p)
                    self.assertEqual(tree_lca_query(lca, y, x), p)

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