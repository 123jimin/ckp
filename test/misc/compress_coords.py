import unittest
from ckp.misc.compress_coords import *

class TestCompressCoords(unittest.TestCase):
    def test_empty(self):
        l = compress_coords([])
        self.assertListEqual(l, [])
    
    def test_simple(self):
        l = compress_coords([5, 8, 8, 6, 8, 9, 9, 6, 7, 8])
        self.assertListEqual(l, [5, 6, 7, 8, 9])