
import unittest
from ckp.graph_theory.scc import *

from ckp.data_structure.graph.list import ListGraph

class TestStronglyConnectedComponents(unittest.TestCase):
    def test_02150(self):
        G = ListGraph(7)
        for (u, v) in [
            (1, 4), (4, 5), (5, 1), (1, 6), (6, 7), (2, 7), (7, 3), (3, 7), (7, 2)
        ]: G.add_edge(u-1, v-1)

        sccs = sorted((sorted(scc) for scc in strongly_connected_components(G)), key=lambda v: v[0])
        
        self.assertEqual(len(sccs), 3)
        self.assertListEqual(sccs[0], [0, 3, 4])
        self.assertListEqual(sccs[1], [1, 2, 6])
        self.assertListEqual(sccs[2], [5])