
import unittest
from ckp.data_structure.graph.simple import *

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

class TestUndirectedSetGraph(unittest.TestCase):
    def test_k5(self):
        graph = UndirectedSetGraph(5)
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
    
    def test_peterson(self):
        graph = UndirectedSetGraph(10)
        self.assertEqual(len(graph), 10)

        for i in range(5):
            graph.add_edge(i, i+5)
            graph.add_edge(i, (i+1)%5)
            graph.add_edge(i+5, (i+2)%5+5)
        
        for i in range(10):
            self.assertEqual(len(graph.neighbors[i]), 3)
            self.assertEqual(len(graph.out_neighbors(i)), 3)

            if i < 5:
                self.assertEqual(sorted(graph.out_neighbors(i)), sorted([(i-1)%5, (i+1)%5, i+5]))
            else:
                j = i-5
                self.assertEqual(sorted(graph.out_neighbors(i)), sorted([(j-2)%5+5, (j+2)%5+5, j]))