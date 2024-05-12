import unittest

import random, itertools

from ckp.data_structure import DisjointSet, SimpleSegmentTree
from ckp.graph_theory.tree import Tree, DistanceTree, TreeLCA, TreeHLD

class TestBOJ13510(unittest.TestCase):
    def _create_random_edges(self, N: int, max_weight: int = 100) -> list[tuple[int, int, int]]:
        ds = DisjointSet(N)

        complete_edges = list(itertools.combinations(range(N), 2))
        random.shuffle(complete_edges)

        edges = []

        for i, j in complete_edges:
            if ds.union(i, j):
                if random.randint(1, 2) == 1: i, j = j, i
                edges.append((i, j, random.randint(1, max_weight)))

        self.assertEqual(len(edges), N-1)
        self.assertEqual(ds.size(0), N)

        return edges

    def _solve_naive(self, edges: list[tuple[int, int, int]], ops: list[tuple[int, int, int]]) -> list[int]:
        tree = Tree.from_edges([(u, v) for (u, v, _) in edges])
        parent_weight = [None] * len(tree)

        for (u, v, w) in edges:
            if tree.parents[u] == v:
                parent_weight[u] = w
            else:
                parent_weight[v] = w

        lca = TreeLCA(tree)
        ans = []

        for op in ops:
            if op[0] == 1:
                u, v, w = edges[op[1]]
                if tree.parents[u] == v:
                    parent_weight[u] = op[2]
                else:
                    parent_weight[v] = op[2]
            elif op[0] == 2:
                u, v = op[1], op[2]
                a = lca.get(u, v)
                m = 0
                while u != a:
                    m = max(m, parent_weight[u])
                    u = tree.parents[u]
                while v != a:
                    m = max(m, parent_weight[v])
                    v = tree.parents[v]
                ans.append(m)
        
        return ans

    def _solve_hld(self, edges: list[tuple[int, int, int]], ops: list[tuple[int, int, int]]) -> list[int]:
        tree = DistanceTree.from_edges(edges)
        hld = TreeHLD(tree)

        segments = list[SimpleSegmentTree]()
        for path in hld.paths: segments.append(SimpleSegmentTree([tree.parent_distances[v] for v in path], max))

        lca = TreeLCA(tree)

        def modify_edge(u: int, v: int, w: int):
            if tree.parents[v] != u: u, v = v, u
            assert(tree.parents[v] == u)

            i, j = hld.path_index[v]
            segments[i][j] = w

        def get_descendant_distance(u: int, v: int) -> int:
            if u == v: return 0

            paths = hld.paths
            d = 0
            for (pi, ps, pe) in hld.decompose_descendant(u, v):
                curr_path = paths[pi]
                curr_segment = segments[pi]
                if curr_path[ps] == u: curr_d = curr_segment.reduce_range(ps+1, pe)
                else: curr_d = curr_segment.reduce_range(ps, pe)
                
                if curr_d > d: d = curr_d

            return d

        def get_distance(u: int, v: int) -> int:
            a = lca.get(u, v)
            return max(get_descendant_distance(a, u), get_descendant_distance(a, v))

        ans = []

        for (q, x, y) in ops:
            if q == 1:
                u, v, _ = edges[x]
                modify_edge(u, v, y)
            else:
                ans.append(get_distance(x, y))
        
        return ans

    def test_example(self):
        edges = [(0, 1, 1), (1, 2, 2)]
        ops = [(2, 0, 1), (1, 0, 3), (2, 0, 1)]
        self.assertListEqual(self._solve_naive(edges, ops), [1, 3])
        self.assertListEqual(self._solve_hld(edges, ops), [1, 3])
    
    def test_past_fail(self):
        edges = [(6, 4, 46), (1, 3, 78), (0, 4, 6), (1, 6, 69), (5, 1, 49), (5, 2, 71), (5, 7, 81)]
        ops = [(2, 3, 5)]

        self.assertListEqual(self._solve_naive(edges, ops), [78])
        self.assertListEqual(self._solve_hld(edges, ops), [78])

    def test_random(self):
        for _ in range(100):
            N = random.randint(2, 100)
            M = random.randint(1, 100)
            W = 1000

            edges = self._create_random_edges(N, W)
            ops = []
            for _ in range(M):
                op = random.randint(1, 2)
                if op == 1:
                    ops.append((1, random.randrange(N-1), random.randint(1, W)))
                else:
                    u, v = random.sample(range(N), 2)
                    ops.append((2, u, v))
            
            self.assertListEqual(self._solve_naive(edges, ops), self._solve_hld(edges, ops))

if __name__ == '__main__':
    unittest.main()