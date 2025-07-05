import unittest
from ckp.data_structure.segment_tree.offline_sorted_set import *

import random

class TestOfflineOrderedSet(unittest.TestCase):
    def test_basic(self):
        s = OfflineSortedSet(8)
        
        self.assertTrue(s.add(3))
        self.assertTrue(s.add(5))
        self.assertFalse(s.add(3))

        self.assertIn(3, s)
        self.assertNotIn(4, s)
        self.assertIn(5, s)

        self.assertIsNone(s.prev(3))
        self.assertEqual(s.next(3), 5)

        self.assertEqual(s.prev(4), 3)
        self.assertEqual(s.next(4), 5)

        self.assertEqual(s.prev(5), 3)
        self.assertIsNone(s.next(5))

        self.assertTrue(s.discard(3))

        self.assertIsNone(s.prev(4))
    
    def test_random(self):
        for _ in range(100):
            N = random.randint(1, 64)
            s = OfflineSortedSet(N)
            ref = set()
            for __ in range(200):
                match random.choice(['add', 'discard', 'prev', 'next']):
                    case 'add':
                        x = random.randrange(N)
                        self.assertEqual(s.add(x), x not in ref)
                        ref.add(x)
                    case 'discard':
                        x = random.randrange(N)
                        self.assertEqual(s.discard(x), x in ref)
                        ref.discard(x)
                    case 'prev':
                        x = random.randrange(N)
                        self.assertEqual(s.prev(x), max((y for y in ref if y < x), default=None))
                    case 'next':
                        x = random.randrange(N)
                        self.assertEqual(s.next(x), min((y for y in ref if y > x), default=None))