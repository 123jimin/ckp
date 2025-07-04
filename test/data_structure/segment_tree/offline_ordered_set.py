import unittest
from ckp.data_structure.segment_tree.offline_ordered_set import *

class TestOfflineOrderedSet(unittest.TestCase):
    @unittest.skip
    def test_basic(self):
        s = OfflineOrderedSet(8)
        
        self.assertTrue(s.add(3))
        self.assertTrue(s.add(5))
        self.assertFalse(s.add(3))

        self.assertIn(3, s)
        self.assertNotIn(4, s)
        self.assertIn(5, s)

        self.assertIsNone(s.prev(3))
        self.assertEqual(s.next(3), 5)

        self.assertEqual(s.prev(4), 3)
        self.assertEqual(s.prev(4), 5)

        self.assertEqual(s.prev(5), 3)
        self.assertIsNone(s.next(5))

        self.assertTrue(s.discard(3))

        self.assertIsNone(s.prev(4))