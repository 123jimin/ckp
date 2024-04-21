import unittest
from ckp.graph_theory.max_flow.push_relabel import *
from ckp.data_structure.graph.simple import DictGraph

class TestPushRelabel(unittest.TestCase):
    def test_linear(self):
        graph = DictGraph(5)
        graph.add_edge(0, 1, 3)
        graph.add_edge(1, 2, 3)
        graph.add_edge(2, 3, 5)
        graph.add_edge(3, 4, 4)
        graph.add_edge(1, 4, 6)

        pr = PushRelabel(graph, 0, 4)
        self.assertEqual(pr.max_flow, 3)
        self.assertTrue(all(pr.excess[i] == 0 for i in range(len(graph)) if i != 4), f"{pr.excess=} should be 0 for all non-sink vertices")
    
    def test_bipartite(self):
        return # TODO
        graph = DictGraph(13)
        graph.add_edge(0, 1, 1000)
        for u in [2, 3, 4, 5, 6]: graph.add_edge(0, u, 1)
        for u in [7, 8, 9, 10, 11]: graph.add_edge(u, 12, 1)
        for (u, v) in [(2, 7), (2, 8), (3, 7), (4, 8), (4, 9), (5, 9), (5, 10), (5, 11), (6, 7)]:
            graph.add_edge(u, v, 1)
        pr = PushRelabel(graph, 0, 12)
        self.assertEqual(pr.max_flow, 4)
        self.assertTrue(all(pr.excess[i] == 0 for i in range(len(graph)) if i != 12), f"{pr.excess=} should be 0 for all non-sink vertices")