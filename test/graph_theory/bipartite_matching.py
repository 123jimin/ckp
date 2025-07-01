import unittest
from ckp.graph_theory.bipartite_matching import *

import random
from ckp.data_structure.graph.bipartite import bipartite_graph_from_edges

class TestBipartiteMatching(unittest.TestCase):
    def test_random(self):
        for _ in range(1000):
            U = random.randint(1, 50)
            V = random.randint(1, 50)
            p = random.random()
            edges = [(u, v) for u in range(U) for v in range(V) if random.random() < p]
            
            graph = bipartite_graph_from_edges(U, V, edges)
            matching = bipartite_matching(graph)

            assert_valid_bipartite_matching(graph, matching)
    
    def test_empty(self):
        graph = bipartite_graph_from_edges(1000, 1000)
        matching = bipartite_matching(graph)

        self.assertEqual(len(matching), 0)
        assert_valid_bipartite_matching(graph, matching)
    
    def test_simple(self):
        graph = bipartite_graph_from_edges(5, 4, [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (2, 1), (3, 0), (4, 0), (4, 2)])
        matching = bipartite_matching(graph)

        self.assertEqual(len(matching), 4)
        assert_valid_bipartite_matching(graph, matching)

    def test_wikipedia(self):
        graph = bipartite_graph_from_edges(5, 5, [(0, 0), (0, 1), (1, 0), (1, 4), (2, 2), (2, 3), (3, 0), (3, 4), (4, 0), (4, 3)])
        matching = bipartite_matching(graph)

        self.assertEqual(len(matching), 5)
        assert_valid_bipartite_matching(graph, matching)