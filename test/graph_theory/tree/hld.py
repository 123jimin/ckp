import unittest
from ckp.graph_theory.tree.hld import *

from ckp.graph_theory.tree import TreeData, tree_from_edges

class TestHLD(unittest.TestCase):
    def _test_decompose_descendant(self, tree: TreeData, hld: TreeHLDData, u: int, v: int):
        x = u
        for (pi, ps, pe) in tree_hld_decompose_descendant(hld, u, v):
            self.assertLess(pi, len(hld.paths), f"{u=} {v=} {pi=}")
            curr_path = hld.paths[pi]

            self.assertLess(ps, len(curr_path), f"{u=} {v=} {curr_path=}")
            self.assertLess(ps, pe, f"{u=} {v=} {curr_path=}")
            self.assertLessEqual(pe, len(curr_path), f"{u=} {v=} {curr_path=}")

            self.assertEqual(x, curr_path[pe-1], f"{u=} {v=} {curr_path=} {ps=} {pe=}")
            for i in reversed(range(ps, pe-1)):
                x = tree.parents[x]
                self.assertEqual(x, curr_path[i], f"{u=} {v=} {curr_path=} {ps=} {pe=} {i=}")
            
            if x != v:
                x = tree.parents[x]

        self.assertEqual(x, v)

    def test_simple(self):
        tree = tree_from_edges([(0, 1), (0, 2), (2, 3), (2, 4), (4, 5), (1, 6), (1, 7), (7, 8), (5, 9)], root=0)
        hld = tree_hld_init(tree)
        
        self.assertEqual(len(hld.paths), 4)
        self.assertEqual(len(hld.path_index), len(tree))
        
        self.assertSetEqual(set("".join(str(v) for v in path) for path in hld.paths), {"02459", "178", "6", "3"})
        self.assertTrue(all(ind is not None for ind in hld.path_index))

        for (u, v) in [(1, 0), (2, 0), (8, 0), (3, 0), (9, 4)]:
            self._test_decompose_descendant(tree, hld, u, v)