import unittest
from ckp.automata.finite_automata import *

class TestDFA(unittest.TestCase):
    def test_multiple_of_3(self):
        three_mul = DFA([
            {0: 0, 1: 1},
            {0: 2, 1: 0},
            {0: 1, 1: 2},
        ], {0})

        self.assertEqual(len(three_mul), 3)

        for i in range(100):
            l = []
            x = i
            while x:
                x, m = divmod(x, 2)
                l.append(m)
            self.assertEqual(three_mul.test(reversed(l)), i%3 == 0, f"Results must be equal for {i=}")
    
    def test_multiple_of_15(self):
        three_mul = DFA([
            {0: 0, 1: 1},
            {0: 2, 1: 0},
            {0: 1, 1: 2},
        ], {0})

        five_mul = DFA([
            {0: 0, 1: 1},
            {0: 2, 1: 3},
            {0: 4, 1: 0},
            {0: 1, 1: 2},
            {0: 3, 1: 4},
        ], {0})

        fifteen_mul = three_mul & five_mul
        self.assertEqual(len(fifteen_mul), 15)

        for i in range(100):
            l = []
            x = i
            while x:
                x, m = divmod(x, 2)
                l.append(m)
            self.assertEqual(fifteen_mul.test(reversed(l)), i%15 == 0, f"Results must be equal for {i=}")

class TestNFA(unittest.TestCase):
    def test_multiple_of_3(self):
        three_mul = NFA([
            {48: {0}, 49: {1}},
            {48: {2}, 49: {0}},
            {48: {1}, 49: {2}},
        ], {0})

        self.assertEqual(len(three_mul), 3)

        for i in range(100):
            l = []
            x = i
            while x:
                x, m = divmod(x, 2)
                l.append([48, 49][m])
            self.assertEqual(three_mul.test(reversed(l)), i%3 == 0, f"Results must be equal for {i=}")

    def test_14339(self):
        def lit(s: str) -> NFA:
            return NFA.from_str([ord(c) for c in s])
        
        regex = lit('1') + (lit('56') | ((lit('7') | lit('8')).kleene_star() + lit('9')).kleene_star())
        reversed = regex.reversed()
        ps = regex.to_powerset_dfa()
        reversed_ps = NFA.from_reversed_dfa(ps)
        minimal = regex.minimize()

        self.assertEqual(len(ps), 7)
        self.assertEqual(len(minimal), 6)
        
        test_set = (1, 19, 156, 179, 189, 199)
        rev_test_set = (1, 91, 651, 971, 981, 991)

        for i in range(1, 1001):
            self.assertEqual(regex.test(map(ord, str(i))), (i in test_set), f"Unexpected result for {i=}")
            self.assertEqual(reversed.test(map(ord, str(i))), (i in rev_test_set), f"Unexpected result for {i=}")
            self.assertEqual(ps.test(map(ord, str(i))), (i in test_set), f"Unexpected result for {i=}")
            self.assertEqual(reversed_ps.test(map(ord, str(i))), (i in rev_test_set), f"Unexpected result for {i=}")
            self.assertEqual(minimal.test(map(ord, str(i))), (i in test_set), f"Unexpected result for {i=}")