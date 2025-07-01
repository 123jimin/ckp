import unittest
from ckp.data_structure.graph.list import *

class TestUndirectedListGraph(unittest.TestCase):
    def test_k5(self):
        graph = UndirectedListGraph(5)
        self.assertEqual(len(graph), 5)

        for i in range(4):
            for j in range(i+1, 5):
                graph.add_edge(i, j)
        
        for i in range(5):
            self.assertEqual(len(graph.neighbors[i]), 4)
            self.assertEqual(len(graph.out_neighbors(i)), 4)
            x = set(graph.out_neighbors(i))
            x.add(i)
            self.assertListEqual(sorted(x), [0, 1, 2, 3, 4])