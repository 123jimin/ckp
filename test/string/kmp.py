import unittest
from ckp.string.kmp import *

class TestKMPBuild(unittest.TestCase):
    def test_simple(self):
        self.assertListEqual(kmp_build("X"), [-1, 0])
        self.assertListEqual(kmp_build("ABCDABD"), [-1, 0, 0, 0, -1, 0, 2, 0])
        self.assertListEqual(kmp_build([4, 3, 2, 1, 4, 3, 1]), [-1, 0, 0, 0, -1, 0, 2, 0])
        self.assertListEqual(kmp_build("ABACABABC"), [-1, 0, -1, 1, -1, 0, -1, 3, 2, 0])
        self.assertListEqual(kmp_build("ABACABABA"), [-1, 0, -1, 1, -1, 0, -1, 3, -1, 3])
        self.assertListEqual(kmp_build("ABRACADABRA"), [-1, 0, 0, -1, 1, -1, 1, -1, 0, 0, -1, 4])

class TestKMPSearch(unittest.TestCase):
    def test_simple(self):
        self.assertListEqual(list(kmp_search("Hello, world!", "word")), [])
        self.assertListEqual(list(kmp_search("A"*100, "A")), list(range(100)))
        self.assertListEqual(list(kmp_search("ABC ABCDAB ABCDABCDABDE", "ABCDABD")), [15])
        self.assertListEqual(list(kmp_search("ABCBABCBABCBA", "ABCBA")), [0, 4, 8])