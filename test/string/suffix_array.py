import unittest
from ckp.string.suffix_array import *

def suffix_array_bruteforce(s: str) -> list[int]:
    return sorted(range(len(s)), key=lambda i: s[i:])

class SuffixArrayDivideConquerTest(unittest.TestCase):
    def test_simple(self):
        self.assertListEqual(suffix_array_divide_conquer(""), [])
        self.assertListEqual(suffix_array_divide_conquer("a"), [0])
        self.assertListEqual(suffix_array_divide_conquer("ab"), [0, 1])
        self.assertListEqual(suffix_array_divide_conquer("abaab"), [2, 3, 0, 4, 1])
        self.assertListEqual(suffix_array_divide_conquer("abracadabra"), [10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2])