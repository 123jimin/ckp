import unittest
from ckp.language.aheui import *
from ckp.language.aheui.simulate import aheui_run_strip

class TestAheuiFromText(unittest.TestCase):
    def assertIdempotent(self, text: str):
        code = aheui_from_text(text)
        output = aheui_run_strip(code)

        self.assertEqual(output, text)

    def test_simple(self):
        self.assertIdempotent("")
        self.assertIdempotent("1234 + 5678 = ?")
        self.assertIdempotent("Hello, world!\n")
        self.assertIdempotent("The quick brown fox jumps over the lazy dog.\n")
    
    def test_int(self):
        for i in range(-200, 201):
            self.assertIdempotent(str(i))

class TestAheuiFromVals(unittest.TestCase):
    def test_optimal(self):
        OPTIMAL_LEN = [
            3, 3, 1, 1, 1, 1, 1, 1, 1, 1,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 5,
            3, 3, 5, 5, 3, 3, 5, 3, 3, 5,
            3, 5, 3, 5, 5, 3, 3, 5, 5, 5,
            3, 5, 3, 5, 5, 3, 5, 5, 3, 3,
            5, 5, 5, 5, 3, 5, 3, 5, 5, 5,
            5, 5, 5, 3, 3, 5, 5, 5, 5, 5,
            5, 5, 3, 5, 5, 5, 5, 5, 5, 5,
            5, 3, 7, 5, 5, 5, 5, 5, 5, 5,
            5, 5, 7, 7, 7, 7, 5, 7, 5, 5,
            5, 7, 5, 7, 5, 5, 7, 7, 5, 7,
            7, 7, 5, 7, 7, 7, 7, 5, 7, 5,
            5, 7, 7, 7, 7, 5, 5, 7, 5, 7,
            7, 7, 7, 7, 7, 5, 5, 7, 7, 7,
            5, 7, 7, 7, 5, 7, 7, 5, 7, 7,
            5, 7, 7, 5, 7, 7, 7, 7, 7, 7,
            5, 7, 5, 7, 7, 7, 7, 7, 5, 7,
            7, 7, 7, 7, 7, 5, 7, 7, 7, 7,
            5, 7, 7, 7, 7, 7, 7, 7, 7, 5,
            7, 7, 5, 7, 7, 7, 5, 7, 7, 7,
        ]
        for i, optimal_len in enumerate(OPTIMAL_LEN):
            codes = aheui_from_vals([i])
            self.assertEqual(len(codes), 1)

            code = codes[0]
            self.assertEqual(len(code), optimal_len, f"{i=} {code=}")