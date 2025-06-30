import unittest
from ckp.graph_theory.bipartite_matching import *

from ckp.data_structure.graph.bipartite import bipartite_graph_from_edges

class TestBipartiteMatching(unittest.TestCase):
    @unittest.skip
    def test(self):
        graph = bipartite_graph_from_edges([(0, 0), (0, 1), (1, 0), (1, 4), (2, 2), (2, 3), (3, 0), (3, 4), (4, 0), (4, 3)])
        matching = bipartite_matching(graph)