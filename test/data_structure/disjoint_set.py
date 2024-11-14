
import unittest
from ckp.data_structure.disjoint_set import *

class TestDisjointSet(unittest.TestCase):
    def test_simple(self):
        ds = disjoint_set_init(8)
        self.assertTrue(disjoint_set_union(ds, 1, 3))
        self.assertFalse(disjoint_set_is_same_set(ds, 1, 7))
        self.assertTrue(disjoint_set_union(ds, 7, 6))
        self.assertFalse(disjoint_set_is_same_set(ds, 7, 1))
        self.assertTrue(disjoint_set_union(ds, 3, 7))
        self.assertTrue(disjoint_set_is_same_set(ds, 1, 7))
        self.assertTrue(disjoint_set_union(ds, 4, 2))
        self.assertFalse(disjoint_set_union(ds, 1, 1))
        self.assertTrue(disjoint_set_is_same_set(ds, 1, 1))
        self.assertTrue(disjoint_set_is_same_set(ds, 1, 7))
        self.assertFalse(disjoint_set_is_same_set(ds, 1, 2))
        for i in range(8):
            self.assertEqual(disjoint_set_size(ds, i), [1,4,2,4,2,1,4,4][i])

class TestDisjointSetObject(unittest.TestCase):
    def test_simple(self):
        ds = []
        for i in range(8): ds.append(DisjointSetObject(i, f"data {i}"))
        self.assertTrue(ds[1].union(ds[3]))
        self.assertFalse(ds[1].in_same_set(ds[7]))
        self.assertTrue(ds[7].union(ds[6]))
        self.assertFalse(ds[7].in_same_set(ds[1]))
        self.assertTrue(ds[3].union(ds[7]))
        self.assertTrue(ds[1].in_same_set(ds[7]))
        self.assertTrue(ds[4].union(ds[2]))
        self.assertFalse(ds[1].union(ds[1]))
        self.assertTrue(ds[1].in_same_set(ds[1]))
        self.assertTrue(ds[1].in_same_set(ds[7]))
        self.assertFalse(ds[1].in_same_set(ds[2]))
        for i in range(8):
            self.assertEqual(ds[i].size, [1,4,2,4,2,1,4,4][i])