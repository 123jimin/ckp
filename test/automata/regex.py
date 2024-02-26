import unittest
from ckp.automata.regex import *

class TestRegexAST(unittest.TestCase):
    def test_14339(self):
        regex = RegexAST.parse("1(56|(((7|8))*9)*)")
        self.assertTrue(repr(regex), "1(56|(7|8)*9*)")
        self.assertTrue(repr(regex.children[0]), "1")
        self.assertTrue(repr(regex.children[1]), "56|(7|8)*9*")
        self.assertTrue(repr(regex.children[1].children[0]), "56")
        self.assertTrue(repr(regex.children[1].children[1]), "(7|8)*9*")