import unittest
from ckp.data_structure.wavelet_tree import *

class TestLinkedWaveletTree(unittest.TestCase):    
    def _assert_tree(self, node: LinkedWaveletTreeData, arr: list[int]):
        self.assertEqual(node._min, min(arr))
        self.assertEqual(node._max, max(arr))
        self.assertListEqual(node._arr, arr)

        if node._min == node._max:
            self.assertIsNone(node._left)
            self.assertIsNone(node._right)
            return
    
        self.assertIsNotNone(node._left)
        self.assertIsNotNone(node._right)

        self.assertEqual(node._left._min, node._min)
        self.assertEqual(node._left._max + 1, node._right._min)
        self.assertEqual(node._right._max, node._max)

        self._assert_tree(node._left, [x for x in arr if node._left._min <= x <= node._left._max])
        self._assert_tree(node._right, [x for x in arr if node._right._min <= x <= node._right._max])

    def test_paper(self):
        arr = [3, 3, 9, 1, 2, 1, 7, 6, 4, 8, 9, 4, 3, 7, 5, 9, 2, 7, 3, 5, 1, 3]
        tree = linked_wavelet_tree_init(arr)
        self._assert_tree(tree, arr)